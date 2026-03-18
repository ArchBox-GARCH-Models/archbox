"""Engle-Sheppard (2001) CCC vs DCC Test.

Tests H0: constant conditional correlation (CCC) vs
H1: dynamic conditional correlation (DCC).

References
----------
- Engle, R.F. & Sheppard, K. (2001). Theoretical and Empirical Properties
  of Dynamic Conditional Correlation Multivariate GARCH.
  NBER Working Paper 8554.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class EngleSheppardResult:
    """Container for Engle-Sheppard test result.

    Attributes
    ----------
    statistic : float
        LM test statistic (T * R^2).
    pvalue : float
        p-value from chi2(q).
    lags : int
        Number of lags q used.
    test_name : str
        Name of the test.
    """

    statistic: float
    pvalue: float
    lags: int
    test_name: str = "Engle-Sheppard CCC vs DCC"

    def __repr__(self) -> str:
        """Return string representation of the test result."""
        return (
            f"{self.test_name}(lags={self.lags}): "
            f"statistic={self.statistic:.4f}, pvalue={self.pvalue:.4f}"
        )


def engle_sheppard_test(
    std_resids: object,
    lags: int = 1,
) -> EngleSheppardResult:
    """Engle-Sheppard (2001) test for constant conditional correlation.

    Tests H0: CCC (constant correlation) vs H1: DCC (dynamic correlation).

    Parameters
    ----------
    std_resids : array-like
        Matrix of standardized residuals, shape (T, k).
        z_{i,t} = eps_{i,t} / sigma_{i,t} from univariate GARCH fits.
    lags : int
        Number of lags q for the LM test. Default is 1.

    Returns
    -------
    EngleSheppardResult
        LM statistic and p-value.

    Notes
    -----
    For each pair (i, j):
        1. Compute z_{ij,t} = z_{i,t} * z_{j,t} - rho_{ij}
        2. Regress z_{ij,t} on z_{ij,t-1}, ..., z_{ij,t-q}
        3. LM = T * R^2 ~ chi2(q)

    The overall test combines all pairs.
    """
    resids = np.asarray(std_resids, dtype=np.float64)
    if resids.ndim != 2:
        msg = f"std_resids must be 2D (T x k), got {resids.ndim}D"
        raise ValueError(msg)

    n_obs, k = resids.shape

    if k < 2:
        msg = f"Need at least 2 series, got {k}"
        raise ValueError(msg)

    # Sample correlation matrix
    r_corr = np.corrcoef(resids.T)

    # Collect LM statistics across all pairs
    total_lm = 0.0
    n_pairs = 0

    for i in range(k):
        for j in range(i + 1, k):
            # z_{ij,t} = z_i * z_j - rho_ij
            z_ij = resids[:, i] * resids[:, j] - r_corr[i, j]

            # Dependent variable
            y = z_ij[lags:]
            n = len(y)

            # Regressors: intercept + lagged z_ij
            x_reg = np.ones((n, lags + 1))
            for lag in range(1, lags + 1):
                x_reg[:, lag] = z_ij[lags - lag : n_obs - lag]

            # OLS
            beta = np.linalg.lstsq(x_reg, y, rcond=None)[0]
            y_hat = x_reg @ beta
            ss_res = np.sum((y - y_hat) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)

            r2 = 1 - ss_res / ss_tot if ss_tot > 1e-20 else 0.0

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )
