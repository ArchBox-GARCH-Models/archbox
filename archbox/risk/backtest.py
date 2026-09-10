"""VaR Backtesting: Kupiec, Christoffersen, Basel Traffic Light.

References
----------
- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk
  Measurement Models. Journal of Derivatives, 3(2), 73-84.
- Christoffersen, P.F. (1998). Evaluating Interval Forecasts.
  International Economic Review, 39(4), 841-862.
- Basel Committee on Banking Supervision (1996). Supervisory Framework for
  the Use of "Backtesting" in Conjunction with the Internal Models Approach
  to Market Risk Capital Requirements.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

#: Cumulative binomial probability at which the Basel yellow zone starts.
BASEL_YELLOW_LEVEL: float = 0.95
#: Cumulative binomial probability at which the Basel red zone starts.
BASEL_RED_LEVEL: float = 0.9999


def _binomial_zone_threshold(n: int, alpha: float, level: float) -> int:
    """Smallest violation count whose cumulative binomial probability >= level.

    Parameters
    ----------
    n : int
        Number of observations in the backtest window.
    alpha : float
        VaR tail probability (the exception probability under H0).
    level : float
        Cumulative probability at which the next zone starts (0.95 for the
        Basel yellow zone, 0.9999 for the red zone).

    Returns
    -------
    int
        The zone threshold ``x``, clipped to ``[0, n + 1]``. ``n + 1`` means
        "unreachable with this sample size".
    """
    if n <= 0:
        return 1
    x = int(stats.binom.ppf(level, n, alpha))
    x = int(np.clip(x, 0, n + 1))
    # ``ppf`` can land one step off at the boundary because of floating point:
    # walk to the exact smallest x with cdf(x) >= level.
    while x > 0 and float(stats.binom.cdf(x - 1, n, alpha)) >= level:
        x -= 1
    while x <= n and float(stats.binom.cdf(x, n, alpha)) < level:
        x += 1
    return x


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

    #: Not a pytest test class (the name only looks like one).
    __test__ = False

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
        valid = np.isfinite(self.returns) & np.isfinite(self.var)
        if not np.any(valid):
            msg = (
                "no valid (returns, var_series) pairs to backtest: every observation "
                "is NaN or infinite. Historical VaR leaves the first `window` values "
                "NaN - align the series or use a longer sample."
            )
            raise ValueError(msg)

        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def _require_observations(self) -> None:
        """Ensure the hit sequence is non-empty.

        Raises
        ------
        ValueError
            If there is no valid observation to compute a rate from (which
            would make every ``x / n`` a division by zero).
        """
        if len(self.hits) == 0:
            msg = (
                "no valid observations in the backtest sample: cannot compute a "
                "violation rate. Check that returns and var_series overlap and "
                "are not all NaN."
            )
            raise ValueError(msg)

    def kupiec_test(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Raises
        ------
        ValueError
            If the backtest sample holds no valid observation.

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        self._require_observations()
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

    def basel_zones(self, window: int = 250) -> tuple[int, int, int]:
        """Basel traffic-light zone boundaries for this alpha and window.

        The zones follow the Basel (1996) construction: under H0 the number of
        exceptions is Binomial(n, alpha), the yellow zone starts at the first
        count whose cumulative probability reaches 95%, and the red zone at the
        first count whose cumulative probability reaches 99.99%. For the
        supervisory case (n = 250, alpha = 1%) this reproduces the published
        table exactly: green 0-4, yellow 5-9, red 10+.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250. The effective sample
            size is ``min(window, number of valid observations)``.

        Returns
        -------
        tuple[int, int, int]
            ``(n, yellow_min, red_min)``: the effective sample size, the
            smallest violation count in the yellow zone and the smallest
            violation count in the red zone.

        Raises
        ------
        ValueError
            If ``window`` is not a positive integer.
        """
        window = int(window)
        if window < 1:
            msg = f"window must be a positive integer, got {window}"
            raise ValueError(msg)

        n = min(window, len(self.hits))
        yellow_min = _binomial_zone_threshold(n, self.alpha, BASEL_YELLOW_LEVEL)
        red_min = _binomial_zone_threshold(n, self.alpha, BASEL_RED_LEVEL)
        return n, yellow_min, red_min

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
        The zone boundaries are derived from the Binomial(n, alpha)
        distribution for the *actual* ``alpha`` of this backtest and the
        *actual* number of observations used (see :meth:`basel_zones`), not
        hardcoded for the 250-day/1% supervisory case.
        """
        self._require_observations()
        n, yellow_min, red_min = self.basel_zones(window)

        hits_window = self.hits[-n:]
        n_violations = int(np.sum(hits_window))

        if n_violations >= red_min:
            return "red"
        if n_violations >= yellow_min:
            return "yellow"
        return "green"

    def violation_ratio(self) -> float:
        """Compute the violation ratio.

        Returns
        -------
        float
            Observed violation rate / expected violation rate (alpha).
            A ratio of 1.0 indicates perfect calibration.
        """
        self._require_observations()
        observed_rate = float(np.mean(self.hits))
        return float(observed_rate / self.alpha)

    def summary(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        self._require_observations()
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        zone_n, yellow_min, red_min = self.basel_zones()
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
            (
                f"    (n={zone_n}, alpha={self.alpha:.4f}: green < {yellow_min}"
                f" <= yellow < {red_min} <= red)"
            ),
            "=" * 60,
        ]

        return "\n".join(lines)
