"""Ljung-Box test on squared residuals.

Tests for remaining ARCH effects in standardized squared residuals.

References
----------
- Ljung, G.M. & Box, G.E.P. (1978). On a Measure of Lack of Fit
  in Time Series Models. Biometrika, 65(2), 297-303.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class LjungBoxResult:
    """Container for Ljung-Box test result.

    Attributes
    ----------
    statistic : float
        Q(m) test statistic.
    pvalue : float
        p-value from chi2(m).
    lags : int
        Number of lags m.
    test_name : str
        Name of the test.
    """

    statistic: float
    pvalue: float
    lags: int
    test_name: str = "Ljung-Box (z^2)"

    def __repr__(self) -> str:
        """Return string representation of the test result."""
        return (
            f"{self.test_name}(lags={self.lags}): "
            f"statistic={self.statistic:.4f}, pvalue={self.pvalue:.4f}"
        )


def ljung_box_squared(std_resids: object, lags: int = 10) -> LjungBoxResult:
    """Ljung-Box test on squared standardized residuals.

    Tests H0: no autocorrelation in z^2_t (no remaining ARCH effects).

    Parameters
    ----------
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t.
    lags : int
        Number of lags m. Default is 10.

    Returns
    -------
    LjungBoxResult
        Q(m) statistic and p-value from chi2(m).

    Notes
    -----
    Q(m) = T * (T+2) * sum_{k=1}^{m} rho^2_k(z^2) / (T-k) ~ chi2(m)

    Where rho_k(z^2) is the sample autocorrelation of z^2_t at lag k.
    """
    z = np.asarray(std_resids, dtype=np.float64).ravel()
    z2 = z**2
    nobs = len(z2)

    if lags >= nobs:
        msg = f"lags ({lags}) must be less than T ({nobs})"
        raise ValueError(msg)

    # Compute autocorrelations of z^2
    z2_demeaned = z2 - np.mean(z2)
    gamma_0 = np.sum(z2_demeaned**2) / nobs

    if gamma_0 < 1e-20:
        return LjungBoxResult(statistic=0.0, pvalue=1.0, lags=lags)

    q_stat = 0.0
    for k in range(1, lags + 1):
        gamma_k = np.sum(z2_demeaned[k:] * z2_demeaned[:-k]) / nobs
        rho_k = gamma_k / gamma_0
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )
