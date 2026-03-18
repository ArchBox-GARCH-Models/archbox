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

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated, ClassVar

import numpy as np
from scipy import stats

MutantDict = Annotated[dict[str, Callable], "Mutant"]  # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):  # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os  # type: ignore

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]  # type: ignore
    if mutant_under_test == "fail":  # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException  # type: ignore

        raise MutmutProgrammaticFailException("Failed programmatically")  # type: ignore
    elif mutant_under_test == "stats":  # type: ignore
        from mutmut.__main__ import record_trampoline_hit  # type: ignore

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)  # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"  # type: ignore
    if not mutant_under_test.startswith(prefix):  # type: ignore
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    mutant_name = mutant_under_test.rpartition(".")[-1]  # type: ignore
    if self_arg is not None:  # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)  # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)  # type: ignore
    return result  # type: ignore


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
    args = [std_resids, lags]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_engle_sheppard_test__mutmut_orig,
        x_engle_sheppard_test__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_engle_sheppard_test__mutmut_orig(
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


def x_engle_sheppard_test__mutmut_1(
    std_resids: object,
    lags: int = 2,
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


def x_engle_sheppard_test__mutmut_2(
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
    resids = None
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


def x_engle_sheppard_test__mutmut_3(
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
    resids = np.asarray(None, dtype=np.float64)
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


def x_engle_sheppard_test__mutmut_4(
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
    resids = np.asarray(std_resids, dtype=None)
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


def x_engle_sheppard_test__mutmut_5(
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
    resids = np.asarray(dtype=np.float64)
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


def x_engle_sheppard_test__mutmut_6(
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
    resids = np.asarray(
        std_resids,
    )
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


def x_engle_sheppard_test__mutmut_7(
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
    if resids.ndim == 2:
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


def x_engle_sheppard_test__mutmut_8(
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
    if resids.ndim != 3:
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


def x_engle_sheppard_test__mutmut_9(
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
        msg = None
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


def x_engle_sheppard_test__mutmut_10(
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
        raise ValueError(None)

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


def x_engle_sheppard_test__mutmut_11(
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

    n_obs, k = None

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


def x_engle_sheppard_test__mutmut_12(
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

    if k <= 2:
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


def x_engle_sheppard_test__mutmut_13(
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

    if k < 3:
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


def x_engle_sheppard_test__mutmut_14(
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
        msg = None
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


def x_engle_sheppard_test__mutmut_15(
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
        raise ValueError(None)

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


def x_engle_sheppard_test__mutmut_16(
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
    r_corr = None

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


def x_engle_sheppard_test__mutmut_17(
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
    r_corr = np.corrcoef(None)

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


def x_engle_sheppard_test__mutmut_18(
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
    total_lm = None
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


def x_engle_sheppard_test__mutmut_19(
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
    total_lm = 1.0
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


def x_engle_sheppard_test__mutmut_20(
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
    n_pairs = None

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


def x_engle_sheppard_test__mutmut_21(
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
    n_pairs = 1

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


def x_engle_sheppard_test__mutmut_22(
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

    for i in range(None):
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


def x_engle_sheppard_test__mutmut_23(
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
        for j in range(None, k):
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


def x_engle_sheppard_test__mutmut_24(
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
        for j in range(i + 1, None):
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


def x_engle_sheppard_test__mutmut_25(
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
        for j in range(k):
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


def x_engle_sheppard_test__mutmut_26(
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
        for j in range(
            i + 1,
        ):
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


def x_engle_sheppard_test__mutmut_27(
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
        for j in range(i - 1, k):
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


def x_engle_sheppard_test__mutmut_28(
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
        for j in range(i + 2, k):
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


def x_engle_sheppard_test__mutmut_29(
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
            z_ij = None

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


def x_engle_sheppard_test__mutmut_30(
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
            z_ij = resids[:, i] * resids[:, j] + r_corr[i, j]

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


def x_engle_sheppard_test__mutmut_31(
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
            z_ij = resids[:, i] / resids[:, j] - r_corr[i, j]

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


def x_engle_sheppard_test__mutmut_32(
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
            y = None
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


def x_engle_sheppard_test__mutmut_33(
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
            n = None

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


def x_engle_sheppard_test__mutmut_34(
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
            x_reg = None
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


def x_engle_sheppard_test__mutmut_35(
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
            x_reg = np.ones(None)
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


def x_engle_sheppard_test__mutmut_36(
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
            x_reg = np.ones((n, lags - 1))
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


def x_engle_sheppard_test__mutmut_37(
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
            x_reg = np.ones((n, lags + 2))
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


def x_engle_sheppard_test__mutmut_38(
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
            for lag in range(None, lags + 1):
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


def x_engle_sheppard_test__mutmut_39(
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
            for lag in range(1, None):
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


def x_engle_sheppard_test__mutmut_40(
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
            for lag in range(lags + 1):
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


def x_engle_sheppard_test__mutmut_41(
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
            for lag in range(
                1,
            ):
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


def x_engle_sheppard_test__mutmut_42(
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
            for lag in range(2, lags + 1):
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


def x_engle_sheppard_test__mutmut_43(
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
            for lag in range(1, lags - 1):
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


def x_engle_sheppard_test__mutmut_44(
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
            for lag in range(1, lags + 2):
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


def x_engle_sheppard_test__mutmut_45(
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
                x_reg[:, lag] = None

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


def x_engle_sheppard_test__mutmut_46(
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
                x_reg[:, lag] = z_ij[lags + lag : n_obs - lag]

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


def x_engle_sheppard_test__mutmut_47(
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
                x_reg[:, lag] = z_ij[lags - lag : n_obs + lag]

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


def x_engle_sheppard_test__mutmut_48(
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
            beta = None
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


def x_engle_sheppard_test__mutmut_49(
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
            beta = np.linalg.lstsq(None, y, rcond=None)[0]
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


def x_engle_sheppard_test__mutmut_50(
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
            beta = np.linalg.lstsq(x_reg, None, rcond=None)[0]
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


def x_engle_sheppard_test__mutmut_51(
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
            beta = np.linalg.lstsq(y, rcond=None)[0]
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


def x_engle_sheppard_test__mutmut_52(
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
            beta = np.linalg.lstsq(x_reg, rcond=None)[0]
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


def x_engle_sheppard_test__mutmut_53(
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
            beta = np.linalg.lstsq(
                x_reg,
                y,
            )[0]
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


def x_engle_sheppard_test__mutmut_54(
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
            beta = np.linalg.lstsq(x_reg, y, rcond=None)[1]
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


def x_engle_sheppard_test__mutmut_55(
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
            y_hat = None
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


def x_engle_sheppard_test__mutmut_56(
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
            ss_res = None
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


def x_engle_sheppard_test__mutmut_57(
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
            ss_res = np.sum(None)
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


def x_engle_sheppard_test__mutmut_58(
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
            ss_res = np.sum((y - y_hat) * 2)
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


def x_engle_sheppard_test__mutmut_59(
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
            ss_res = np.sum((y + y_hat) ** 2)
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


def x_engle_sheppard_test__mutmut_60(
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
            ss_res = np.sum((y - y_hat) ** 3)
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


def x_engle_sheppard_test__mutmut_61(
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
            ss_tot = None

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


def x_engle_sheppard_test__mutmut_62(
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
            ss_tot = np.sum(None)

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


def x_engle_sheppard_test__mutmut_63(
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
            ss_tot = np.sum((y - np.mean(y)) * 2)

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


def x_engle_sheppard_test__mutmut_64(
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
            ss_tot = np.sum((y + np.mean(y)) ** 2)

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


def x_engle_sheppard_test__mutmut_65(
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
            ss_tot = np.sum((y - np.mean(None)) ** 2)

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


def x_engle_sheppard_test__mutmut_66(
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
            ss_tot = np.sum((y - np.mean(y)) ** 3)

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


def x_engle_sheppard_test__mutmut_67(
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

            r2 = None

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_68(
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

            r2 = 1 + ss_res / ss_tot if ss_tot > 1e-20 else 0.0

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_69(
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

            r2 = 2 - ss_res / ss_tot if ss_tot > 1e-20 else 0.0

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_70(
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

            r2 = 1 - ss_res * ss_tot if ss_tot > 1e-20 else 0.0

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_71(
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

            r2 = 1 - ss_res / ss_tot if ss_tot >= 1e-20 else 0.0

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_72(
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

            r2 = 1 - ss_res / ss_tot if ss_tot > 1.0 else 0.0

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_73(
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

            r2 = 1 - ss_res / ss_tot if ss_tot > 1e-20 else 1.0

            total_lm += n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_74(
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

            total_lm = n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_75(
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

            total_lm -= n * r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_76(
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

            total_lm += n / r2
            n_pairs += 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_77(
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
            n_pairs = 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_78(
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
            n_pairs -= 1

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_79(
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
            n_pairs += 2

    avg_lm = total_lm / max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_80(
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

    avg_lm = None

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_81(
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

    avg_lm = total_lm * max(n_pairs, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_82(
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

    avg_lm = total_lm / max(None, 1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_83(
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

    avg_lm = total_lm / max(n_pairs, None)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_84(
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

    avg_lm = total_lm / max(1)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_85(
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

    avg_lm = total_lm / max(
        n_pairs,
    )

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_86(
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

    avg_lm = total_lm / max(n_pairs, 2)

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_87(
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

    pvalue = None

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_88(
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

    pvalue = float(None)

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_89(
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

    pvalue = float(1 + stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_90(
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

    pvalue = float(2 - stats.chi2.cdf(avg_lm, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_91(
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

    pvalue = float(1 - stats.chi2.cdf(None, df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_92(
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

    pvalue = float(1 - stats.chi2.cdf(avg_lm, df=None))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_93(
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

    pvalue = float(1 - stats.chi2.cdf(df=lags))

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_94(
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

    pvalue = float(
        1
        - stats.chi2.cdf(
            avg_lm,
        )
    )

    return EngleSheppardResult(
        statistic=float(avg_lm),
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_95(
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
        statistic=None,
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_96(
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
        pvalue=None,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_97(
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
        lags=None,
    )


def x_engle_sheppard_test__mutmut_98(
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
        pvalue=pvalue,
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_99(
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
        lags=lags,
    )


def x_engle_sheppard_test__mutmut_100(
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
    )


def x_engle_sheppard_test__mutmut_101(
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
        statistic=float(None),
        pvalue=pvalue,
        lags=lags,
    )


x_engle_sheppard_test__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_engle_sheppard_test__mutmut_1": x_engle_sheppard_test__mutmut_1,
    "x_engle_sheppard_test__mutmut_2": x_engle_sheppard_test__mutmut_2,
    "x_engle_sheppard_test__mutmut_3": x_engle_sheppard_test__mutmut_3,
    "x_engle_sheppard_test__mutmut_4": x_engle_sheppard_test__mutmut_4,
    "x_engle_sheppard_test__mutmut_5": x_engle_sheppard_test__mutmut_5,
    "x_engle_sheppard_test__mutmut_6": x_engle_sheppard_test__mutmut_6,
    "x_engle_sheppard_test__mutmut_7": x_engle_sheppard_test__mutmut_7,
    "x_engle_sheppard_test__mutmut_8": x_engle_sheppard_test__mutmut_8,
    "x_engle_sheppard_test__mutmut_9": x_engle_sheppard_test__mutmut_9,
    "x_engle_sheppard_test__mutmut_10": x_engle_sheppard_test__mutmut_10,
    "x_engle_sheppard_test__mutmut_11": x_engle_sheppard_test__mutmut_11,
    "x_engle_sheppard_test__mutmut_12": x_engle_sheppard_test__mutmut_12,
    "x_engle_sheppard_test__mutmut_13": x_engle_sheppard_test__mutmut_13,
    "x_engle_sheppard_test__mutmut_14": x_engle_sheppard_test__mutmut_14,
    "x_engle_sheppard_test__mutmut_15": x_engle_sheppard_test__mutmut_15,
    "x_engle_sheppard_test__mutmut_16": x_engle_sheppard_test__mutmut_16,
    "x_engle_sheppard_test__mutmut_17": x_engle_sheppard_test__mutmut_17,
    "x_engle_sheppard_test__mutmut_18": x_engle_sheppard_test__mutmut_18,
    "x_engle_sheppard_test__mutmut_19": x_engle_sheppard_test__mutmut_19,
    "x_engle_sheppard_test__mutmut_20": x_engle_sheppard_test__mutmut_20,
    "x_engle_sheppard_test__mutmut_21": x_engle_sheppard_test__mutmut_21,
    "x_engle_sheppard_test__mutmut_22": x_engle_sheppard_test__mutmut_22,
    "x_engle_sheppard_test__mutmut_23": x_engle_sheppard_test__mutmut_23,
    "x_engle_sheppard_test__mutmut_24": x_engle_sheppard_test__mutmut_24,
    "x_engle_sheppard_test__mutmut_25": x_engle_sheppard_test__mutmut_25,
    "x_engle_sheppard_test__mutmut_26": x_engle_sheppard_test__mutmut_26,
    "x_engle_sheppard_test__mutmut_27": x_engle_sheppard_test__mutmut_27,
    "x_engle_sheppard_test__mutmut_28": x_engle_sheppard_test__mutmut_28,
    "x_engle_sheppard_test__mutmut_29": x_engle_sheppard_test__mutmut_29,
    "x_engle_sheppard_test__mutmut_30": x_engle_sheppard_test__mutmut_30,
    "x_engle_sheppard_test__mutmut_31": x_engle_sheppard_test__mutmut_31,
    "x_engle_sheppard_test__mutmut_32": x_engle_sheppard_test__mutmut_32,
    "x_engle_sheppard_test__mutmut_33": x_engle_sheppard_test__mutmut_33,
    "x_engle_sheppard_test__mutmut_34": x_engle_sheppard_test__mutmut_34,
    "x_engle_sheppard_test__mutmut_35": x_engle_sheppard_test__mutmut_35,
    "x_engle_sheppard_test__mutmut_36": x_engle_sheppard_test__mutmut_36,
    "x_engle_sheppard_test__mutmut_37": x_engle_sheppard_test__mutmut_37,
    "x_engle_sheppard_test__mutmut_38": x_engle_sheppard_test__mutmut_38,
    "x_engle_sheppard_test__mutmut_39": x_engle_sheppard_test__mutmut_39,
    "x_engle_sheppard_test__mutmut_40": x_engle_sheppard_test__mutmut_40,
    "x_engle_sheppard_test__mutmut_41": x_engle_sheppard_test__mutmut_41,
    "x_engle_sheppard_test__mutmut_42": x_engle_sheppard_test__mutmut_42,
    "x_engle_sheppard_test__mutmut_43": x_engle_sheppard_test__mutmut_43,
    "x_engle_sheppard_test__mutmut_44": x_engle_sheppard_test__mutmut_44,
    "x_engle_sheppard_test__mutmut_45": x_engle_sheppard_test__mutmut_45,
    "x_engle_sheppard_test__mutmut_46": x_engle_sheppard_test__mutmut_46,
    "x_engle_sheppard_test__mutmut_47": x_engle_sheppard_test__mutmut_47,
    "x_engle_sheppard_test__mutmut_48": x_engle_sheppard_test__mutmut_48,
    "x_engle_sheppard_test__mutmut_49": x_engle_sheppard_test__mutmut_49,
    "x_engle_sheppard_test__mutmut_50": x_engle_sheppard_test__mutmut_50,
    "x_engle_sheppard_test__mutmut_51": x_engle_sheppard_test__mutmut_51,
    "x_engle_sheppard_test__mutmut_52": x_engle_sheppard_test__mutmut_52,
    "x_engle_sheppard_test__mutmut_53": x_engle_sheppard_test__mutmut_53,
    "x_engle_sheppard_test__mutmut_54": x_engle_sheppard_test__mutmut_54,
    "x_engle_sheppard_test__mutmut_55": x_engle_sheppard_test__mutmut_55,
    "x_engle_sheppard_test__mutmut_56": x_engle_sheppard_test__mutmut_56,
    "x_engle_sheppard_test__mutmut_57": x_engle_sheppard_test__mutmut_57,
    "x_engle_sheppard_test__mutmut_58": x_engle_sheppard_test__mutmut_58,
    "x_engle_sheppard_test__mutmut_59": x_engle_sheppard_test__mutmut_59,
    "x_engle_sheppard_test__mutmut_60": x_engle_sheppard_test__mutmut_60,
    "x_engle_sheppard_test__mutmut_61": x_engle_sheppard_test__mutmut_61,
    "x_engle_sheppard_test__mutmut_62": x_engle_sheppard_test__mutmut_62,
    "x_engle_sheppard_test__mutmut_63": x_engle_sheppard_test__mutmut_63,
    "x_engle_sheppard_test__mutmut_64": x_engle_sheppard_test__mutmut_64,
    "x_engle_sheppard_test__mutmut_65": x_engle_sheppard_test__mutmut_65,
    "x_engle_sheppard_test__mutmut_66": x_engle_sheppard_test__mutmut_66,
    "x_engle_sheppard_test__mutmut_67": x_engle_sheppard_test__mutmut_67,
    "x_engle_sheppard_test__mutmut_68": x_engle_sheppard_test__mutmut_68,
    "x_engle_sheppard_test__mutmut_69": x_engle_sheppard_test__mutmut_69,
    "x_engle_sheppard_test__mutmut_70": x_engle_sheppard_test__mutmut_70,
    "x_engle_sheppard_test__mutmut_71": x_engle_sheppard_test__mutmut_71,
    "x_engle_sheppard_test__mutmut_72": x_engle_sheppard_test__mutmut_72,
    "x_engle_sheppard_test__mutmut_73": x_engle_sheppard_test__mutmut_73,
    "x_engle_sheppard_test__mutmut_74": x_engle_sheppard_test__mutmut_74,
    "x_engle_sheppard_test__mutmut_75": x_engle_sheppard_test__mutmut_75,
    "x_engle_sheppard_test__mutmut_76": x_engle_sheppard_test__mutmut_76,
    "x_engle_sheppard_test__mutmut_77": x_engle_sheppard_test__mutmut_77,
    "x_engle_sheppard_test__mutmut_78": x_engle_sheppard_test__mutmut_78,
    "x_engle_sheppard_test__mutmut_79": x_engle_sheppard_test__mutmut_79,
    "x_engle_sheppard_test__mutmut_80": x_engle_sheppard_test__mutmut_80,
    "x_engle_sheppard_test__mutmut_81": x_engle_sheppard_test__mutmut_81,
    "x_engle_sheppard_test__mutmut_82": x_engle_sheppard_test__mutmut_82,
    "x_engle_sheppard_test__mutmut_83": x_engle_sheppard_test__mutmut_83,
    "x_engle_sheppard_test__mutmut_84": x_engle_sheppard_test__mutmut_84,
    "x_engle_sheppard_test__mutmut_85": x_engle_sheppard_test__mutmut_85,
    "x_engle_sheppard_test__mutmut_86": x_engle_sheppard_test__mutmut_86,
    "x_engle_sheppard_test__mutmut_87": x_engle_sheppard_test__mutmut_87,
    "x_engle_sheppard_test__mutmut_88": x_engle_sheppard_test__mutmut_88,
    "x_engle_sheppard_test__mutmut_89": x_engle_sheppard_test__mutmut_89,
    "x_engle_sheppard_test__mutmut_90": x_engle_sheppard_test__mutmut_90,
    "x_engle_sheppard_test__mutmut_91": x_engle_sheppard_test__mutmut_91,
    "x_engle_sheppard_test__mutmut_92": x_engle_sheppard_test__mutmut_92,
    "x_engle_sheppard_test__mutmut_93": x_engle_sheppard_test__mutmut_93,
    "x_engle_sheppard_test__mutmut_94": x_engle_sheppard_test__mutmut_94,
    "x_engle_sheppard_test__mutmut_95": x_engle_sheppard_test__mutmut_95,
    "x_engle_sheppard_test__mutmut_96": x_engle_sheppard_test__mutmut_96,
    "x_engle_sheppard_test__mutmut_97": x_engle_sheppard_test__mutmut_97,
    "x_engle_sheppard_test__mutmut_98": x_engle_sheppard_test__mutmut_98,
    "x_engle_sheppard_test__mutmut_99": x_engle_sheppard_test__mutmut_99,
    "x_engle_sheppard_test__mutmut_100": x_engle_sheppard_test__mutmut_100,
    "x_engle_sheppard_test__mutmut_101": x_engle_sheppard_test__mutmut_101,
}
x_engle_sheppard_test__mutmut_orig.__name__ = "x_engle_sheppard_test"
