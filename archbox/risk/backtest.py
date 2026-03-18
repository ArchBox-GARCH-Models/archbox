"""VaR Backtesting: Kupiec, Christoffersen, Basel Traffic Light.

References
----------
- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk
  Measurement Models. Journal of Derivatives, 3(2), 73-84.
- Christoffersen, P.F. (1998). Evaluating Interval Forecasts.
  International Economic Review, 39(4), 841-862.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class TestResult:
    """Container for a statistical test result.

    Attributes
    ----------
    statistic : float
        Test statistic value.
    pvalue : float
        p-value of the test.
    test_name : str
        Name of the test.
    df : int
        Degrees of freedom.
    """

    statistic: float
    pvalue: float
    test_name: str
    df: int = 1

    def __repr__(self) -> str:
        """Return string representation of the test result."""
        return (
            f"{self.test_name}: statistic={self.statistic:.4f}, "
            f"pvalue={self.pvalue:.4f}, df={self.df}"
        )


class VaRBacktest:
    """VaR Backtesting framework.

    Parameters
    ----------
    returns : array-like
        Realized return series.
    var_series : array-like
        VaR forecast series (must be negative for losses).
    alpha : float
        Significance level of the VaR. Default is 0.05.

    Attributes
    ----------
    returns : NDArray[np.float64]
        Realized returns.
    var : NDArray[np.float64]
        VaR forecasts.
    alpha : float
        Significance level.
    hits : NDArray[np.int64]
        Hit sequence: 1 if r_t < VaR_t, 0 otherwise.
    """

    def __init__(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def kupiec_test(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def christoffersen_test(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def basel_traffic_light(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def violation_ratio(self) -> float:
        """Compute the violation ratio.

        Returns
        -------
        float
            Observed violation rate / expected violation rate (alpha).
            A ratio of 1.0 indicates perfect calibration.
        """
        observed_rate = self.hits.mean()
        return float(observed_rate / self.alpha)

    def summary(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)
