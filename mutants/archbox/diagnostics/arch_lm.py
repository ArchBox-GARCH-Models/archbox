"""ARCH-LM Test (Engle, 1982).

Tests H0: no ARCH effects (homoscedasticity) in the residuals.

References
----------
- Engle, R.F. (1982). Autoregressive Conditional Heteroscedasticity with
  Estimates of the Variance of United Kingdom Inflation. Econometrica,
  50(4), 987-1007.
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
    args = [resids, lags]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_arch_lm_test__mutmut_orig, x_arch_lm_test__mutmut_mutants, args, kwargs, None
    )


def x_arch_lm_test__mutmut_orig(resids: object, lags: int = 5) -> TestResult:
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


def x_arch_lm_test__mutmut_1(resids: object, lags: int = 6) -> TestResult:
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


def x_arch_lm_test__mutmut_2(resids: object, lags: int = 5) -> TestResult:
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
    e = None
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


def x_arch_lm_test__mutmut_3(resids: object, lags: int = 5) -> TestResult:
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
    e = np.asarray(None, dtype=np.float64).ravel()
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


def x_arch_lm_test__mutmut_4(resids: object, lags: int = 5) -> TestResult:
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
    e = np.asarray(resids, dtype=None).ravel()
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


def x_arch_lm_test__mutmut_5(resids: object, lags: int = 5) -> TestResult:
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
    e = np.asarray(dtype=np.float64).ravel()
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


def x_arch_lm_test__mutmut_6(resids: object, lags: int = 5) -> TestResult:
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
    e = np.asarray(
        resids,
    ).ravel()
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


def x_arch_lm_test__mutmut_7(resids: object, lags: int = 5) -> TestResult:
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
    e2 = None
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


def x_arch_lm_test__mutmut_8(resids: object, lags: int = 5) -> TestResult:
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
    e2 = e * 2
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


def x_arch_lm_test__mutmut_9(resids: object, lags: int = 5) -> TestResult:
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
    e2 = e**3
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


def x_arch_lm_test__mutmut_10(resids: object, lags: int = 5) -> TestResult:
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
    nobs = None

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


def x_arch_lm_test__mutmut_11(resids: object, lags: int = 5) -> TestResult:
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

    if lags > nobs - 1:
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


def x_arch_lm_test__mutmut_12(resids: object, lags: int = 5) -> TestResult:
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

    if lags >= nobs + 1:
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


def x_arch_lm_test__mutmut_13(resids: object, lags: int = 5) -> TestResult:
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

    if lags >= nobs - 2:
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


def x_arch_lm_test__mutmut_14(resids: object, lags: int = 5) -> TestResult:
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
        msg = None
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


def x_arch_lm_test__mutmut_15(resids: object, lags: int = 5) -> TestResult:
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
        msg = f"lags ({lags}) must be less than T-1 ({nobs + 1})"
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


def x_arch_lm_test__mutmut_16(resids: object, lags: int = 5) -> TestResult:
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
        msg = f"lags ({lags}) must be less than T-1 ({nobs - 2})"
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


def x_arch_lm_test__mutmut_17(resids: object, lags: int = 5) -> TestResult:
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
        raise ValueError(None)

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


def x_arch_lm_test__mutmut_18(resids: object, lags: int = 5) -> TestResult:
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
    y = None
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


def x_arch_lm_test__mutmut_19(resids: object, lags: int = 5) -> TestResult:
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
    n = None

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


def x_arch_lm_test__mutmut_20(resids: object, lags: int = 5) -> TestResult:
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
    x_reg = None
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


def x_arch_lm_test__mutmut_21(resids: object, lags: int = 5) -> TestResult:
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
    x_reg = np.ones(None)
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


def x_arch_lm_test__mutmut_22(resids: object, lags: int = 5) -> TestResult:
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
    x_reg = np.ones((n, lags - 1))
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


def x_arch_lm_test__mutmut_23(resids: object, lags: int = 5) -> TestResult:
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
    x_reg = np.ones((n, lags + 2))
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


def x_arch_lm_test__mutmut_24(resids: object, lags: int = 5) -> TestResult:
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
    for j in range(None, lags + 1):
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


def x_arch_lm_test__mutmut_25(resids: object, lags: int = 5) -> TestResult:
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
    for j in range(1, None):
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


def x_arch_lm_test__mutmut_26(resids: object, lags: int = 5) -> TestResult:
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
    for j in range(lags + 1):
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


def x_arch_lm_test__mutmut_27(resids: object, lags: int = 5) -> TestResult:
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
    for j in range(
        1,
    ):
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


def x_arch_lm_test__mutmut_28(resids: object, lags: int = 5) -> TestResult:
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
    for j in range(2, lags + 1):
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


def x_arch_lm_test__mutmut_29(resids: object, lags: int = 5) -> TestResult:
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
    for j in range(1, lags - 1):
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


def x_arch_lm_test__mutmut_30(resids: object, lags: int = 5) -> TestResult:
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
    for j in range(1, lags + 2):
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


def x_arch_lm_test__mutmut_31(resids: object, lags: int = 5) -> TestResult:
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
        x_reg[:, j] = None

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


def x_arch_lm_test__mutmut_32(resids: object, lags: int = 5) -> TestResult:
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
        x_reg[:, j] = e2[lags + j : nobs - j]

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


def x_arch_lm_test__mutmut_33(resids: object, lags: int = 5) -> TestResult:
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
        x_reg[:, j] = e2[lags - j : nobs + j]

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


def x_arch_lm_test__mutmut_34(resids: object, lags: int = 5) -> TestResult:
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
    beta = None
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


def x_arch_lm_test__mutmut_35(resids: object, lags: int = 5) -> TestResult:
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
    beta = np.linalg.lstsq(None, y, rcond=None)[0]
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


def x_arch_lm_test__mutmut_36(resids: object, lags: int = 5) -> TestResult:
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
    beta = np.linalg.lstsq(x_reg, None, rcond=None)[0]
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


def x_arch_lm_test__mutmut_37(resids: object, lags: int = 5) -> TestResult:
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
    beta = np.linalg.lstsq(y, rcond=None)[0]
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


def x_arch_lm_test__mutmut_38(resids: object, lags: int = 5) -> TestResult:
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
    beta = np.linalg.lstsq(x_reg, rcond=None)[0]
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


def x_arch_lm_test__mutmut_39(resids: object, lags: int = 5) -> TestResult:
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
    beta = np.linalg.lstsq(
        x_reg,
        y,
    )[0]
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


def x_arch_lm_test__mutmut_40(resids: object, lags: int = 5) -> TestResult:
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
    beta = np.linalg.lstsq(x_reg, y, rcond=None)[1]
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


def x_arch_lm_test__mutmut_41(resids: object, lags: int = 5) -> TestResult:
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
    y_hat = None
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


def x_arch_lm_test__mutmut_42(resids: object, lags: int = 5) -> TestResult:
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
    ss_res = None
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


def x_arch_lm_test__mutmut_43(resids: object, lags: int = 5) -> TestResult:
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
    ss_res = np.sum(None)
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


def x_arch_lm_test__mutmut_44(resids: object, lags: int = 5) -> TestResult:
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
    ss_res = np.sum((y - y_hat) * 2)
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


def x_arch_lm_test__mutmut_45(resids: object, lags: int = 5) -> TestResult:
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
    ss_res = np.sum((y + y_hat) ** 2)
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


def x_arch_lm_test__mutmut_46(resids: object, lags: int = 5) -> TestResult:
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
    ss_res = np.sum((y - y_hat) ** 3)
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


def x_arch_lm_test__mutmut_47(resids: object, lags: int = 5) -> TestResult:
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
    ss_tot = None

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_48(resids: object, lags: int = 5) -> TestResult:
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
    ss_tot = np.sum(None)

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_49(resids: object, lags: int = 5) -> TestResult:
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
    ss_tot = np.sum((y - np.mean(y)) * 2)

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_50(resids: object, lags: int = 5) -> TestResult:
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
    ss_tot = np.sum((y + np.mean(y)) ** 2)

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_51(resids: object, lags: int = 5) -> TestResult:
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
    ss_tot = np.sum((y - np.mean(None)) ** 2)

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_52(resids: object, lags: int = 5) -> TestResult:
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
    ss_tot = np.sum((y - np.mean(y)) ** 3)

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_53(resids: object, lags: int = 5) -> TestResult:
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

    r_squared = None

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_54(resids: object, lags: int = 5) -> TestResult:
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

    r_squared = 1.0 if ss_tot < 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_55(resids: object, lags: int = 5) -> TestResult:
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

    r_squared = 0.0 if ss_tot <= 1e-20 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_56(resids: object, lags: int = 5) -> TestResult:
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

    r_squared = 0.0 if ss_tot < 1.0 else 1 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_57(resids: object, lags: int = 5) -> TestResult:
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

    r_squared = 0.0 if ss_tot < 1e-20 else 1 + ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_58(resids: object, lags: int = 5) -> TestResult:
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

    r_squared = 0.0 if ss_tot < 1e-20 else 2 - ss_res / ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_59(resids: object, lags: int = 5) -> TestResult:
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

    r_squared = 0.0 if ss_tot < 1e-20 else 1 - ss_res * ss_tot

    lm_stat = n * r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_60(resids: object, lags: int = 5) -> TestResult:
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

    lm_stat = None
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_61(resids: object, lags: int = 5) -> TestResult:
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

    lm_stat = n / r_squared
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_62(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = None

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_63(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = float(None)

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_64(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = float(1 + stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_65(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = float(2 - stats.chi2.cdf(lm_stat, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_66(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = float(1 - stats.chi2.cdf(None, df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_67(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = float(1 - stats.chi2.cdf(lm_stat, df=None))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_68(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = float(1 - stats.chi2.cdf(df=lags))

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_69(resids: object, lags: int = 5) -> TestResult:
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
    pvalue = float(
        1
        - stats.chi2.cdf(
            lm_stat,
        )
    )

    return TestResult(
        statistic=float(lm_stat),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_70(resids: object, lags: int = 5) -> TestResult:
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
        statistic=None,
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_71(resids: object, lags: int = 5) -> TestResult:
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
        pvalue=None,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_72(resids: object, lags: int = 5) -> TestResult:
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
        test_name=None,
        lags=lags,
    )


def x_arch_lm_test__mutmut_73(resids: object, lags: int = 5) -> TestResult:
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
        lags=None,
    )


def x_arch_lm_test__mutmut_74(resids: object, lags: int = 5) -> TestResult:
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
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_75(resids: object, lags: int = 5) -> TestResult:
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
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_76(resids: object, lags: int = 5) -> TestResult:
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
        lags=lags,
    )


def x_arch_lm_test__mutmut_77(resids: object, lags: int = 5) -> TestResult:
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
    )


def x_arch_lm_test__mutmut_78(resids: object, lags: int = 5) -> TestResult:
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
        statistic=float(None),
        pvalue=pvalue,
        test_name="ARCH-LM",
        lags=lags,
    )


def x_arch_lm_test__mutmut_79(resids: object, lags: int = 5) -> TestResult:
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
        test_name="XXARCH-LMXX",
        lags=lags,
    )


def x_arch_lm_test__mutmut_80(resids: object, lags: int = 5) -> TestResult:
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
        test_name="arch-lm",
        lags=lags,
    )


x_arch_lm_test__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_arch_lm_test__mutmut_1": x_arch_lm_test__mutmut_1,
    "x_arch_lm_test__mutmut_2": x_arch_lm_test__mutmut_2,
    "x_arch_lm_test__mutmut_3": x_arch_lm_test__mutmut_3,
    "x_arch_lm_test__mutmut_4": x_arch_lm_test__mutmut_4,
    "x_arch_lm_test__mutmut_5": x_arch_lm_test__mutmut_5,
    "x_arch_lm_test__mutmut_6": x_arch_lm_test__mutmut_6,
    "x_arch_lm_test__mutmut_7": x_arch_lm_test__mutmut_7,
    "x_arch_lm_test__mutmut_8": x_arch_lm_test__mutmut_8,
    "x_arch_lm_test__mutmut_9": x_arch_lm_test__mutmut_9,
    "x_arch_lm_test__mutmut_10": x_arch_lm_test__mutmut_10,
    "x_arch_lm_test__mutmut_11": x_arch_lm_test__mutmut_11,
    "x_arch_lm_test__mutmut_12": x_arch_lm_test__mutmut_12,
    "x_arch_lm_test__mutmut_13": x_arch_lm_test__mutmut_13,
    "x_arch_lm_test__mutmut_14": x_arch_lm_test__mutmut_14,
    "x_arch_lm_test__mutmut_15": x_arch_lm_test__mutmut_15,
    "x_arch_lm_test__mutmut_16": x_arch_lm_test__mutmut_16,
    "x_arch_lm_test__mutmut_17": x_arch_lm_test__mutmut_17,
    "x_arch_lm_test__mutmut_18": x_arch_lm_test__mutmut_18,
    "x_arch_lm_test__mutmut_19": x_arch_lm_test__mutmut_19,
    "x_arch_lm_test__mutmut_20": x_arch_lm_test__mutmut_20,
    "x_arch_lm_test__mutmut_21": x_arch_lm_test__mutmut_21,
    "x_arch_lm_test__mutmut_22": x_arch_lm_test__mutmut_22,
    "x_arch_lm_test__mutmut_23": x_arch_lm_test__mutmut_23,
    "x_arch_lm_test__mutmut_24": x_arch_lm_test__mutmut_24,
    "x_arch_lm_test__mutmut_25": x_arch_lm_test__mutmut_25,
    "x_arch_lm_test__mutmut_26": x_arch_lm_test__mutmut_26,
    "x_arch_lm_test__mutmut_27": x_arch_lm_test__mutmut_27,
    "x_arch_lm_test__mutmut_28": x_arch_lm_test__mutmut_28,
    "x_arch_lm_test__mutmut_29": x_arch_lm_test__mutmut_29,
    "x_arch_lm_test__mutmut_30": x_arch_lm_test__mutmut_30,
    "x_arch_lm_test__mutmut_31": x_arch_lm_test__mutmut_31,
    "x_arch_lm_test__mutmut_32": x_arch_lm_test__mutmut_32,
    "x_arch_lm_test__mutmut_33": x_arch_lm_test__mutmut_33,
    "x_arch_lm_test__mutmut_34": x_arch_lm_test__mutmut_34,
    "x_arch_lm_test__mutmut_35": x_arch_lm_test__mutmut_35,
    "x_arch_lm_test__mutmut_36": x_arch_lm_test__mutmut_36,
    "x_arch_lm_test__mutmut_37": x_arch_lm_test__mutmut_37,
    "x_arch_lm_test__mutmut_38": x_arch_lm_test__mutmut_38,
    "x_arch_lm_test__mutmut_39": x_arch_lm_test__mutmut_39,
    "x_arch_lm_test__mutmut_40": x_arch_lm_test__mutmut_40,
    "x_arch_lm_test__mutmut_41": x_arch_lm_test__mutmut_41,
    "x_arch_lm_test__mutmut_42": x_arch_lm_test__mutmut_42,
    "x_arch_lm_test__mutmut_43": x_arch_lm_test__mutmut_43,
    "x_arch_lm_test__mutmut_44": x_arch_lm_test__mutmut_44,
    "x_arch_lm_test__mutmut_45": x_arch_lm_test__mutmut_45,
    "x_arch_lm_test__mutmut_46": x_arch_lm_test__mutmut_46,
    "x_arch_lm_test__mutmut_47": x_arch_lm_test__mutmut_47,
    "x_arch_lm_test__mutmut_48": x_arch_lm_test__mutmut_48,
    "x_arch_lm_test__mutmut_49": x_arch_lm_test__mutmut_49,
    "x_arch_lm_test__mutmut_50": x_arch_lm_test__mutmut_50,
    "x_arch_lm_test__mutmut_51": x_arch_lm_test__mutmut_51,
    "x_arch_lm_test__mutmut_52": x_arch_lm_test__mutmut_52,
    "x_arch_lm_test__mutmut_53": x_arch_lm_test__mutmut_53,
    "x_arch_lm_test__mutmut_54": x_arch_lm_test__mutmut_54,
    "x_arch_lm_test__mutmut_55": x_arch_lm_test__mutmut_55,
    "x_arch_lm_test__mutmut_56": x_arch_lm_test__mutmut_56,
    "x_arch_lm_test__mutmut_57": x_arch_lm_test__mutmut_57,
    "x_arch_lm_test__mutmut_58": x_arch_lm_test__mutmut_58,
    "x_arch_lm_test__mutmut_59": x_arch_lm_test__mutmut_59,
    "x_arch_lm_test__mutmut_60": x_arch_lm_test__mutmut_60,
    "x_arch_lm_test__mutmut_61": x_arch_lm_test__mutmut_61,
    "x_arch_lm_test__mutmut_62": x_arch_lm_test__mutmut_62,
    "x_arch_lm_test__mutmut_63": x_arch_lm_test__mutmut_63,
    "x_arch_lm_test__mutmut_64": x_arch_lm_test__mutmut_64,
    "x_arch_lm_test__mutmut_65": x_arch_lm_test__mutmut_65,
    "x_arch_lm_test__mutmut_66": x_arch_lm_test__mutmut_66,
    "x_arch_lm_test__mutmut_67": x_arch_lm_test__mutmut_67,
    "x_arch_lm_test__mutmut_68": x_arch_lm_test__mutmut_68,
    "x_arch_lm_test__mutmut_69": x_arch_lm_test__mutmut_69,
    "x_arch_lm_test__mutmut_70": x_arch_lm_test__mutmut_70,
    "x_arch_lm_test__mutmut_71": x_arch_lm_test__mutmut_71,
    "x_arch_lm_test__mutmut_72": x_arch_lm_test__mutmut_72,
    "x_arch_lm_test__mutmut_73": x_arch_lm_test__mutmut_73,
    "x_arch_lm_test__mutmut_74": x_arch_lm_test__mutmut_74,
    "x_arch_lm_test__mutmut_75": x_arch_lm_test__mutmut_75,
    "x_arch_lm_test__mutmut_76": x_arch_lm_test__mutmut_76,
    "x_arch_lm_test__mutmut_77": x_arch_lm_test__mutmut_77,
    "x_arch_lm_test__mutmut_78": x_arch_lm_test__mutmut_78,
    "x_arch_lm_test__mutmut_79": x_arch_lm_test__mutmut_79,
    "x_arch_lm_test__mutmut_80": x_arch_lm_test__mutmut_80,
}
x_arch_lm_test__mutmut_orig.__name__ = "x_arch_lm_test"
