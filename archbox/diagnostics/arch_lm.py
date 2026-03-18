"""ARCH-LM Test (Engle, 1982).

Tests H0: no ARCH effects (homoscedasticity) in the residuals.

References
----------
- Engle, R.F. (1982). Autoregressive Conditional Heteroscedasticity with
  Estimates of the Variance of United Kingdom Inflation. Econometrica,
  50(4), 987-1007.
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
    lags : int
        Number of lags used.
    """

    statistic: float
    pvalue: float
    test_name: str
    lags: int = 0

    def __repr__(self) -> str:
        """Return string representation of the test result."""
        return (
            f"{self.test_name}(lags={self.lags}): "
            f"statistic={self.statistic:.4f}, pvalue={self.pvalue:.4f}"
        )


def arch_lm_test(resids: object, lags: int = 5) -> TestResult:
    """ARCH-LM test for heteroscedasticity (Engle, 1982).

    Tests H0: no ARCH effects in the residual series.

    Parameters
    ----------
    resids : array-like
        Residual series (raw or standardized).
    lags : int
        Number of lags q for the auxiliary regression. Default is 5.

    Returns
    -------
    TestResult
        Test statistic (T*R^2) and p-value from chi2(q).

    Notes
    -----
    Procedure:
        1. Compute e^2_t = resids^2
        2. Regress e^2_t on e^2_{t-1}, ..., e^2_{t-q} (with intercept)
        3. LM = T * R^2 ~ chi2(q)
    """
    e = np.asarray(resids, dtype=np.float64).ravel()
    e2 = e**2
    nobs = len(e2)

    if lags >= nobs - 1:
        msg = f"lags ({lags}) must be less than T-1 ({nobs - 1})"
        raise ValueError(msg)

    # Build regression matrices
    # Dependent variable: e^2_t for t = lags, ..., T-1
    y = e2[lags:]
    n = len(y)

    # Regressors: intercept + e^2_{t-1}, ..., e^2_{t-q}
    x_reg = np.ones((n, lags + 1))
    for j in range(1, lags + 1):
        x_reg[:, j] = e2[lags - j : nobs - j]

    # OLS regression
    beta = np.linalg.lstsq(x_reg, y, rcond=None)[0]
    y_hat = x_reg @ beta
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )
