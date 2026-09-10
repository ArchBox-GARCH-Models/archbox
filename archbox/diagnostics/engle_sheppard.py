"""Engle-Sheppard (2001) CCC vs DCC Test.

Tests H0: constant conditional correlation (CCC) vs
H1: dynamic conditional correlation (DCC).

References
----------
- Engle, R.F. & Sheppard, K. (2001). Theoretical and Empirical Properties
  of Dynamic Conditional Correlation Multivariate GARCH.
  NBER Working Paper 8554, section 4.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy import stats


@dataclass
class EngleSheppardResult:
    """Container for Engle-Sheppard test result.

    Attributes
    ----------
    statistic : float
        Wald statistic delta' X'X delta / sigma^2 of the pooled artificial
        regression.
    pvalue : float
        p-value from chi2(q + 1).
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


def _inverse_sqrt(mat: NDArray[np.float64]) -> NDArray[np.float64]:
    """Symmetric inverse square root of a positive definite matrix."""
    eigvals, eigvecs = np.linalg.eigh(mat)
    if np.min(eigvals) <= 0:
        msg = "R_bar is not positive definite; cannot standardize the residuals"
        raise ValueError(msg)
    return (eigvecs * (1.0 / np.sqrt(eigvals))) @ eigvecs.T


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
        Number of lags s for the artificial regression. Default is 1.

    Returns
    -------
    EngleSheppardResult
        Wald statistic and p-value from chi2(s + 1).

    Notes
    -----
    Following Engle & Sheppard (2001, section 4):

    1. Estimate R_bar, the second-moment matrix of the standardized
       residuals (their footnote 7 recommends the covariance rather than
       the correlation matrix, so that the test is not also sensitive to
       the univariate variances differing from unity).
    2. Jointly standardize with the symmetric square root: u_t = R_bar^{-1/2} z_t.
       Under H0 the u_t are iid with covariance I_k.
    3. Form Y_t = vech_u(u_t u_t' - I_k), where vech_u selects only the
       elements strictly above the diagonal (k(k-1)/2 series).
    4. Stack the k(k-1)/2 regressands and run the pooled artificial regression

           Y_t = alpha + beta_1 Y_{t-1} + ... + beta_s Y_{t-s} + eta_t

       Under H0 the constant and every lag coefficient is zero, so the Wald
       statistic delta' X'X delta / sigma^2 is asymptotically chi2(s+1).

    The test is mildly conservative in finite samples: because R_bar is
    estimated from the same sample, ``Y_t`` has (numerically) zero sample
    mean, so the intercept carries almost no information and the statistic
    behaves closer to a chi2(s) draw.  Monte-Carlo size at the 5% level is
    roughly 3% for k = 3, T = 500 (it was identically 0% before the pooled
    regression replaced an average of per-pair T*R^2 statistics).
    """
    resids = np.asarray(std_resids, dtype=np.float64)
    if resids.ndim != 2:
        msg = f"std_resids must be 2D (T x k), got {resids.ndim}D"
        raise ValueError(msg)

    n_obs, k = resids.shape

    if k < 2:
        msg = f"Need at least 2 series, got {k}"
        raise ValueError(msg)
    if lags < 1:
        msg = f"lags must be >= 1, got {lags}"
        raise ValueError(msg)
    if lags >= n_obs - 1:
        msg = f"lags ({lags}) must be less than T-1 ({n_obs - 1})"
        raise ValueError(msg)

    # 1-2. Joint standardization by R_bar^{-1/2}.
    r_bar = resids.T @ resids / n_obs
    u = resids @ _inverse_sqrt(r_bar)

    # 3. Y_t = vech_u(u_t u_t' - I_k): the off-diagonal outer products.
    rows, cols = np.triu_indices(k, k=1)
    y = u[:, rows] * u[:, cols]  # (T, m) with m = k(k-1)/2
    n_pairs = y.shape[1]

    # 4. Pooled ("stacked") artificial regression on a constant and s lags.
    n = n_obs - lags
    regressand = y[lags:].T.reshape(-1)  # pair-major stacking, length m*n
    x_reg = np.ones((n_pairs * n, lags + 1))
    for pair in range(n_pairs):
        block = slice(pair * n, (pair + 1) * n)
        for lag in range(1, lags + 1):
            x_reg[block, lag] = y[lags - lag : n_obs - lag, pair]

    beta = np.linalg.lstsq(x_reg, regressand, rcond=None)[0]
    errors = regressand - x_reg @ beta
    n_stacked = regressand.size
    sigma2 = float(errors @ errors) / (n_stacked - (lags + 1))

    if sigma2 < 1e-20:
        return EngleSheppardResult(statistic=0.0, pvalue=1.0, lags=lags)

    xtx = x_reg.T @ x_reg
    stat = float(beta @ xtx @ beta) / sigma2
    stat = max(stat, 0.0)
    pvalue = float(stats.chi2.sf(stat, df=lags + 1))

    return EngleSheppardResult(
        statistic=stat,
        pvalue=pvalue,
        lags=lags,
    )
