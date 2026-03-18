"""Ljung-Box test on squared residuals.

Tests for remaining ARCH effects in standardized squared residuals.

References
----------
- Ljung, G.M. & Box, G.E.P. (1978). On a Measure of Lack of Fit
  in Time Series Models. Biometrika, 65(2), 297-303.
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
    args = [std_resids, lags]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_ljung_box_squared__mutmut_orig, x_ljung_box_squared__mutmut_mutants, args, kwargs, None
    )


def x_ljung_box_squared__mutmut_orig(std_resids: object, lags: int = 10) -> LjungBoxResult:
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


def x_ljung_box_squared__mutmut_1(std_resids: object, lags: int = 11) -> LjungBoxResult:
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


def x_ljung_box_squared__mutmut_2(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z = None
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


def x_ljung_box_squared__mutmut_3(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z = np.asarray(None, dtype=np.float64).ravel()
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


def x_ljung_box_squared__mutmut_4(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z = np.asarray(std_resids, dtype=None).ravel()
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


def x_ljung_box_squared__mutmut_5(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z = np.asarray(dtype=np.float64).ravel()
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


def x_ljung_box_squared__mutmut_6(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z = np.asarray(
        std_resids,
    ).ravel()
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


def x_ljung_box_squared__mutmut_7(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z2 = None
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


def x_ljung_box_squared__mutmut_8(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z2 = z * 2
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


def x_ljung_box_squared__mutmut_9(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z2 = z**3
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


def x_ljung_box_squared__mutmut_10(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    nobs = None

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


def x_ljung_box_squared__mutmut_11(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    if lags > nobs:
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


def x_ljung_box_squared__mutmut_12(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        msg = None
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


def x_ljung_box_squared__mutmut_13(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        raise ValueError(None)

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


def x_ljung_box_squared__mutmut_14(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z2_demeaned = None
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


def x_ljung_box_squared__mutmut_15(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z2_demeaned = z2 + np.mean(z2)
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


def x_ljung_box_squared__mutmut_16(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    z2_demeaned = z2 - np.mean(None)
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


def x_ljung_box_squared__mutmut_17(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    gamma_0 = None

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


def x_ljung_box_squared__mutmut_18(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    gamma_0 = np.sum(z2_demeaned**2) * nobs

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


def x_ljung_box_squared__mutmut_19(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    gamma_0 = np.sum(None) / nobs

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


def x_ljung_box_squared__mutmut_20(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    gamma_0 = np.sum(z2_demeaned * 2) / nobs

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


def x_ljung_box_squared__mutmut_21(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    gamma_0 = np.sum(z2_demeaned**3) / nobs

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


def x_ljung_box_squared__mutmut_22(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    if gamma_0 <= 1e-20:
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


def x_ljung_box_squared__mutmut_23(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    if gamma_0 < 1.0:
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


def x_ljung_box_squared__mutmut_24(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(statistic=None, pvalue=1.0, lags=lags)

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


def x_ljung_box_squared__mutmut_25(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(statistic=0.0, pvalue=None, lags=lags)

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


def x_ljung_box_squared__mutmut_26(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(statistic=0.0, pvalue=1.0, lags=None)

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


def x_ljung_box_squared__mutmut_27(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(pvalue=1.0, lags=lags)

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


def x_ljung_box_squared__mutmut_28(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(statistic=0.0, lags=lags)

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


def x_ljung_box_squared__mutmut_29(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(
            statistic=0.0,
            pvalue=1.0,
        )

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


def x_ljung_box_squared__mutmut_30(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(statistic=1.0, pvalue=1.0, lags=lags)

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


def x_ljung_box_squared__mutmut_31(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        return LjungBoxResult(statistic=0.0, pvalue=2.0, lags=lags)

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


def x_ljung_box_squared__mutmut_32(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    q_stat = None
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


def x_ljung_box_squared__mutmut_33(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    q_stat = 1.0
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


def x_ljung_box_squared__mutmut_34(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    for k in range(None, lags + 1):
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


def x_ljung_box_squared__mutmut_35(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    for k in range(1, None):
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


def x_ljung_box_squared__mutmut_36(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    for k in range(lags + 1):
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


def x_ljung_box_squared__mutmut_37(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    for k in range(
        1,
    ):
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


def x_ljung_box_squared__mutmut_38(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    for k in range(2, lags + 1):
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


def x_ljung_box_squared__mutmut_39(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    for k in range(1, lags - 1):
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


def x_ljung_box_squared__mutmut_40(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    for k in range(1, lags + 2):
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


def x_ljung_box_squared__mutmut_41(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        gamma_k = None
        rho_k = gamma_k / gamma_0
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_42(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        gamma_k = np.sum(z2_demeaned[k:] * z2_demeaned[:-k]) * nobs
        rho_k = gamma_k / gamma_0
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_43(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        gamma_k = np.sum(None) / nobs
        rho_k = gamma_k / gamma_0
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_44(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        gamma_k = np.sum(z2_demeaned[k:] / z2_demeaned[:-k]) / nobs
        rho_k = gamma_k / gamma_0
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_45(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        gamma_k = np.sum(z2_demeaned[k:] * z2_demeaned[:+k]) / nobs
        rho_k = gamma_k / gamma_0
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_46(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        rho_k = None
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_47(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        rho_k = gamma_k * gamma_0
        q_stat += rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_48(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        q_stat = rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_49(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        q_stat -= rho_k**2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_50(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        q_stat += rho_k**2 * (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_51(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        q_stat += rho_k * 2 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_52(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        q_stat += rho_k**3 / (nobs - k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_53(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        q_stat += rho_k**2 / (nobs + k)

    q_stat = nobs * (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_54(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    q_stat = None
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_55(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    q_stat = nobs * (nobs + 2) / q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_56(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    q_stat = nobs / (nobs + 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_57(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    q_stat = nobs * (nobs - 2) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_58(std_resids: object, lags: int = 10) -> LjungBoxResult:
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

    q_stat = nobs * (nobs + 3) * q_stat
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_59(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = None

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_60(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = float(None)

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_61(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = float(1 + stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_62(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = float(2 - stats.chi2.cdf(q_stat, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_63(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = float(1 - stats.chi2.cdf(None, df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_64(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = float(1 - stats.chi2.cdf(q_stat, df=None))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_65(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = float(1 - stats.chi2.cdf(df=lags))

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_66(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    pvalue = float(
        1
        - stats.chi2.cdf(
            q_stat,
        )
    )

    return LjungBoxResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_67(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        statistic=None,
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_68(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        pvalue=None,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_69(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        lags=None,
    )


def x_ljung_box_squared__mutmut_70(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        pvalue=pvalue,
        lags=lags,
    )


def x_ljung_box_squared__mutmut_71(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        lags=lags,
    )


def x_ljung_box_squared__mutmut_72(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
    )


def x_ljung_box_squared__mutmut_73(std_resids: object, lags: int = 10) -> LjungBoxResult:
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
        statistic=float(None),
        pvalue=pvalue,
        lags=lags,
    )


x_ljung_box_squared__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_ljung_box_squared__mutmut_1": x_ljung_box_squared__mutmut_1,
    "x_ljung_box_squared__mutmut_2": x_ljung_box_squared__mutmut_2,
    "x_ljung_box_squared__mutmut_3": x_ljung_box_squared__mutmut_3,
    "x_ljung_box_squared__mutmut_4": x_ljung_box_squared__mutmut_4,
    "x_ljung_box_squared__mutmut_5": x_ljung_box_squared__mutmut_5,
    "x_ljung_box_squared__mutmut_6": x_ljung_box_squared__mutmut_6,
    "x_ljung_box_squared__mutmut_7": x_ljung_box_squared__mutmut_7,
    "x_ljung_box_squared__mutmut_8": x_ljung_box_squared__mutmut_8,
    "x_ljung_box_squared__mutmut_9": x_ljung_box_squared__mutmut_9,
    "x_ljung_box_squared__mutmut_10": x_ljung_box_squared__mutmut_10,
    "x_ljung_box_squared__mutmut_11": x_ljung_box_squared__mutmut_11,
    "x_ljung_box_squared__mutmut_12": x_ljung_box_squared__mutmut_12,
    "x_ljung_box_squared__mutmut_13": x_ljung_box_squared__mutmut_13,
    "x_ljung_box_squared__mutmut_14": x_ljung_box_squared__mutmut_14,
    "x_ljung_box_squared__mutmut_15": x_ljung_box_squared__mutmut_15,
    "x_ljung_box_squared__mutmut_16": x_ljung_box_squared__mutmut_16,
    "x_ljung_box_squared__mutmut_17": x_ljung_box_squared__mutmut_17,
    "x_ljung_box_squared__mutmut_18": x_ljung_box_squared__mutmut_18,
    "x_ljung_box_squared__mutmut_19": x_ljung_box_squared__mutmut_19,
    "x_ljung_box_squared__mutmut_20": x_ljung_box_squared__mutmut_20,
    "x_ljung_box_squared__mutmut_21": x_ljung_box_squared__mutmut_21,
    "x_ljung_box_squared__mutmut_22": x_ljung_box_squared__mutmut_22,
    "x_ljung_box_squared__mutmut_23": x_ljung_box_squared__mutmut_23,
    "x_ljung_box_squared__mutmut_24": x_ljung_box_squared__mutmut_24,
    "x_ljung_box_squared__mutmut_25": x_ljung_box_squared__mutmut_25,
    "x_ljung_box_squared__mutmut_26": x_ljung_box_squared__mutmut_26,
    "x_ljung_box_squared__mutmut_27": x_ljung_box_squared__mutmut_27,
    "x_ljung_box_squared__mutmut_28": x_ljung_box_squared__mutmut_28,
    "x_ljung_box_squared__mutmut_29": x_ljung_box_squared__mutmut_29,
    "x_ljung_box_squared__mutmut_30": x_ljung_box_squared__mutmut_30,
    "x_ljung_box_squared__mutmut_31": x_ljung_box_squared__mutmut_31,
    "x_ljung_box_squared__mutmut_32": x_ljung_box_squared__mutmut_32,
    "x_ljung_box_squared__mutmut_33": x_ljung_box_squared__mutmut_33,
    "x_ljung_box_squared__mutmut_34": x_ljung_box_squared__mutmut_34,
    "x_ljung_box_squared__mutmut_35": x_ljung_box_squared__mutmut_35,
    "x_ljung_box_squared__mutmut_36": x_ljung_box_squared__mutmut_36,
    "x_ljung_box_squared__mutmut_37": x_ljung_box_squared__mutmut_37,
    "x_ljung_box_squared__mutmut_38": x_ljung_box_squared__mutmut_38,
    "x_ljung_box_squared__mutmut_39": x_ljung_box_squared__mutmut_39,
    "x_ljung_box_squared__mutmut_40": x_ljung_box_squared__mutmut_40,
    "x_ljung_box_squared__mutmut_41": x_ljung_box_squared__mutmut_41,
    "x_ljung_box_squared__mutmut_42": x_ljung_box_squared__mutmut_42,
    "x_ljung_box_squared__mutmut_43": x_ljung_box_squared__mutmut_43,
    "x_ljung_box_squared__mutmut_44": x_ljung_box_squared__mutmut_44,
    "x_ljung_box_squared__mutmut_45": x_ljung_box_squared__mutmut_45,
    "x_ljung_box_squared__mutmut_46": x_ljung_box_squared__mutmut_46,
    "x_ljung_box_squared__mutmut_47": x_ljung_box_squared__mutmut_47,
    "x_ljung_box_squared__mutmut_48": x_ljung_box_squared__mutmut_48,
    "x_ljung_box_squared__mutmut_49": x_ljung_box_squared__mutmut_49,
    "x_ljung_box_squared__mutmut_50": x_ljung_box_squared__mutmut_50,
    "x_ljung_box_squared__mutmut_51": x_ljung_box_squared__mutmut_51,
    "x_ljung_box_squared__mutmut_52": x_ljung_box_squared__mutmut_52,
    "x_ljung_box_squared__mutmut_53": x_ljung_box_squared__mutmut_53,
    "x_ljung_box_squared__mutmut_54": x_ljung_box_squared__mutmut_54,
    "x_ljung_box_squared__mutmut_55": x_ljung_box_squared__mutmut_55,
    "x_ljung_box_squared__mutmut_56": x_ljung_box_squared__mutmut_56,
    "x_ljung_box_squared__mutmut_57": x_ljung_box_squared__mutmut_57,
    "x_ljung_box_squared__mutmut_58": x_ljung_box_squared__mutmut_58,
    "x_ljung_box_squared__mutmut_59": x_ljung_box_squared__mutmut_59,
    "x_ljung_box_squared__mutmut_60": x_ljung_box_squared__mutmut_60,
    "x_ljung_box_squared__mutmut_61": x_ljung_box_squared__mutmut_61,
    "x_ljung_box_squared__mutmut_62": x_ljung_box_squared__mutmut_62,
    "x_ljung_box_squared__mutmut_63": x_ljung_box_squared__mutmut_63,
    "x_ljung_box_squared__mutmut_64": x_ljung_box_squared__mutmut_64,
    "x_ljung_box_squared__mutmut_65": x_ljung_box_squared__mutmut_65,
    "x_ljung_box_squared__mutmut_66": x_ljung_box_squared__mutmut_66,
    "x_ljung_box_squared__mutmut_67": x_ljung_box_squared__mutmut_67,
    "x_ljung_box_squared__mutmut_68": x_ljung_box_squared__mutmut_68,
    "x_ljung_box_squared__mutmut_69": x_ljung_box_squared__mutmut_69,
    "x_ljung_box_squared__mutmut_70": x_ljung_box_squared__mutmut_70,
    "x_ljung_box_squared__mutmut_71": x_ljung_box_squared__mutmut_71,
    "x_ljung_box_squared__mutmut_72": x_ljung_box_squared__mutmut_72,
    "x_ljung_box_squared__mutmut_73": x_ljung_box_squared__mutmut_73,
}
x_ljung_box_squared__mutmut_orig.__name__ = "x_ljung_box_squared"
