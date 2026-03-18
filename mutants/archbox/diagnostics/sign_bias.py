"""Sign Bias Test (Engle & Ng, 1993).

Tests whether positive and negative shocks have different impacts
on conditional volatility.

References
----------
- Engle, R.F. & Ng, V.K. (1993). Measuring and Testing the Impact
  of News on Volatility. Journal of Finance, 48(5), 1749-1778.
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
class SignBiasResult:
    """Container for Sign Bias test results.

    Attributes
    ----------
    sign_bias : tuple[float, float]
        (t-statistic, p-value) for the sign bias test.
    neg_sign_bias : tuple[float, float]
        (t-statistic, p-value) for the negative size bias test.
    pos_sign_bias : tuple[float, float]
        (t-statistic, p-value) for the positive size bias test.
    joint : tuple[float, float]
        (F-statistic, p-value) for the joint test.
    """

    sign_bias: tuple[float, float]
    neg_sign_bias: tuple[float, float]
    pos_sign_bias: tuple[float, float]
    joint: tuple[float, float]

    def __repr__(self) -> str:
        """Return string representation of the sign bias test results."""
        lines = [
            "Sign Bias Test (Engle & Ng, 1993)",
            f"  Sign Bias:     t={self.sign_bias[0]:.4f}, p={self.sign_bias[1]:.4f}",
            f"  Neg Size Bias: t={self.neg_sign_bias[0]:.4f}, p={self.neg_sign_bias[1]:.4f}",
            f"  Pos Size Bias: t={self.pos_sign_bias[0]:.4f}, p={self.pos_sign_bias[1]:.4f}",
            f"  Joint Test:    F={self.joint[0]:.4f}, p={self.joint[1]:.4f}",
        ]
        return "\n".join(lines)


def sign_bias_test(resids: object, std_resids: object) -> SignBiasResult:
    args = [resids, std_resids]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_sign_bias_test__mutmut_orig, x_sign_bias_test__mutmut_mutants, args, kwargs, None
    )


def x_sign_bias_test__mutmut_orig(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_1(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = None
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_2(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(None, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_3(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=None).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_4(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_5(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(
        resids,
    ).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_6(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = None

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_7(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(None, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_8(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=None).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_9(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_10(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(
        std_resids,
    ).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_11(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) == len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_12(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = None
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_13(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(None)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_14(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = None
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_15(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] * 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_16(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[2:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_17(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 3
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_18(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = None

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_19(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = None
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_20(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:+1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_21(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-2]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_22(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = None
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_23(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(None)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_24(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag <= 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_25(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 1).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_26(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = None

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_27(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(None)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_28(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag > 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_29(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 1).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_30(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = None

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_31(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(None)

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_32(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(None),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_33(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg / eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_34(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos / eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_35(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = None
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_36(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(None, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_37(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, None, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_38(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_39(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_40(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(
        x_reg,
        z2,
    )[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_41(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[1]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_42(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = None

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_43(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 + x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_44(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = None
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_45(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) * (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_46(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(None) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_47(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals * 2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_48(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**3) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_49(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n + 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_50(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 5)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_51(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = None
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_52(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(None)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_53(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = None

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_54(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat / xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_55(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = None
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_56(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(None)
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_57(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(None))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_58(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = None

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_59(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta * se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_60(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = None
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_61(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(None)
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_62(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[2])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_63(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = None

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_64(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(None)

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_65(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 / (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_66(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(3 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_67(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 + stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_68(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (2 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_69(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(None, df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_70(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=None)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_71(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_72(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(
        2
        * (
            1
            - stats.t.cdf(
                abs(t_stats[1]),
            )
        )
    )

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_73(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(None), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_74(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_75(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n + 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_76(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 5)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_77(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = None
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_78(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(None)
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_79(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[3])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_80(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = None

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_81(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(None)

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_82(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 / (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_83(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(3 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_84(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 + stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_85(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (2 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_86(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(None, df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_87(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=None)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_88(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_89(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(
        2
        * (
            1
            - stats.t.cdf(
                abs(t_stats[2]),
            )
        )
    )

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_90(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(None), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_91(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_92(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n + 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_93(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 5)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_94(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = None
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_95(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(None)
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_96(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[4])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_97(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = None

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_98(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(None)

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_99(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 / (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_100(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(3 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_101(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 + stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_102(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (2 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_103(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(None, df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_104(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=None)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_105(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_106(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(
        2
        * (
            1
            - stats.t.cdf(
                abs(t_stats[3]),
            )
        )
    )

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_107(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(None), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_108(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[4]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_109(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n + 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_110(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 5)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_111(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = None

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_112(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        None,
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_113(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=None,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_114(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_115(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_116(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [1, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_117(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 2, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_118(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_119(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_120(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_121(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_122(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_123(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_124(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_125(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_126(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_127(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 2],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_128(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = None
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_129(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = None
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_130(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = None
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_131(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float(None)
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_132(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) * (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_133(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(None) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_134(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 / sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_135(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (4 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_136(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = None

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_137(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(None)

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_138(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 + stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_139(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(2 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_140(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(None, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_141(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=None, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_142(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=None))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_143(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_144(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_145(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(
        1
        - stats.f.cdf(
            f_stat,
            dfn=3,
        )
    )

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_146(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=4, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_147(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n + 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_148(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 5))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_149(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=None,
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_150(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=None,
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_151(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=None,
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_152(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=None,
    )


def x_sign_bias_test__mutmut_153(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_154(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_155(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        joint=(f_stat, f_pvalue),
    )


def x_sign_bias_test__mutmut_156(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
    )


x_sign_bias_test__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_sign_bias_test__mutmut_1": x_sign_bias_test__mutmut_1,
    "x_sign_bias_test__mutmut_2": x_sign_bias_test__mutmut_2,
    "x_sign_bias_test__mutmut_3": x_sign_bias_test__mutmut_3,
    "x_sign_bias_test__mutmut_4": x_sign_bias_test__mutmut_4,
    "x_sign_bias_test__mutmut_5": x_sign_bias_test__mutmut_5,
    "x_sign_bias_test__mutmut_6": x_sign_bias_test__mutmut_6,
    "x_sign_bias_test__mutmut_7": x_sign_bias_test__mutmut_7,
    "x_sign_bias_test__mutmut_8": x_sign_bias_test__mutmut_8,
    "x_sign_bias_test__mutmut_9": x_sign_bias_test__mutmut_9,
    "x_sign_bias_test__mutmut_10": x_sign_bias_test__mutmut_10,
    "x_sign_bias_test__mutmut_11": x_sign_bias_test__mutmut_11,
    "x_sign_bias_test__mutmut_12": x_sign_bias_test__mutmut_12,
    "x_sign_bias_test__mutmut_13": x_sign_bias_test__mutmut_13,
    "x_sign_bias_test__mutmut_14": x_sign_bias_test__mutmut_14,
    "x_sign_bias_test__mutmut_15": x_sign_bias_test__mutmut_15,
    "x_sign_bias_test__mutmut_16": x_sign_bias_test__mutmut_16,
    "x_sign_bias_test__mutmut_17": x_sign_bias_test__mutmut_17,
    "x_sign_bias_test__mutmut_18": x_sign_bias_test__mutmut_18,
    "x_sign_bias_test__mutmut_19": x_sign_bias_test__mutmut_19,
    "x_sign_bias_test__mutmut_20": x_sign_bias_test__mutmut_20,
    "x_sign_bias_test__mutmut_21": x_sign_bias_test__mutmut_21,
    "x_sign_bias_test__mutmut_22": x_sign_bias_test__mutmut_22,
    "x_sign_bias_test__mutmut_23": x_sign_bias_test__mutmut_23,
    "x_sign_bias_test__mutmut_24": x_sign_bias_test__mutmut_24,
    "x_sign_bias_test__mutmut_25": x_sign_bias_test__mutmut_25,
    "x_sign_bias_test__mutmut_26": x_sign_bias_test__mutmut_26,
    "x_sign_bias_test__mutmut_27": x_sign_bias_test__mutmut_27,
    "x_sign_bias_test__mutmut_28": x_sign_bias_test__mutmut_28,
    "x_sign_bias_test__mutmut_29": x_sign_bias_test__mutmut_29,
    "x_sign_bias_test__mutmut_30": x_sign_bias_test__mutmut_30,
    "x_sign_bias_test__mutmut_31": x_sign_bias_test__mutmut_31,
    "x_sign_bias_test__mutmut_32": x_sign_bias_test__mutmut_32,
    "x_sign_bias_test__mutmut_33": x_sign_bias_test__mutmut_33,
    "x_sign_bias_test__mutmut_34": x_sign_bias_test__mutmut_34,
    "x_sign_bias_test__mutmut_35": x_sign_bias_test__mutmut_35,
    "x_sign_bias_test__mutmut_36": x_sign_bias_test__mutmut_36,
    "x_sign_bias_test__mutmut_37": x_sign_bias_test__mutmut_37,
    "x_sign_bias_test__mutmut_38": x_sign_bias_test__mutmut_38,
    "x_sign_bias_test__mutmut_39": x_sign_bias_test__mutmut_39,
    "x_sign_bias_test__mutmut_40": x_sign_bias_test__mutmut_40,
    "x_sign_bias_test__mutmut_41": x_sign_bias_test__mutmut_41,
    "x_sign_bias_test__mutmut_42": x_sign_bias_test__mutmut_42,
    "x_sign_bias_test__mutmut_43": x_sign_bias_test__mutmut_43,
    "x_sign_bias_test__mutmut_44": x_sign_bias_test__mutmut_44,
    "x_sign_bias_test__mutmut_45": x_sign_bias_test__mutmut_45,
    "x_sign_bias_test__mutmut_46": x_sign_bias_test__mutmut_46,
    "x_sign_bias_test__mutmut_47": x_sign_bias_test__mutmut_47,
    "x_sign_bias_test__mutmut_48": x_sign_bias_test__mutmut_48,
    "x_sign_bias_test__mutmut_49": x_sign_bias_test__mutmut_49,
    "x_sign_bias_test__mutmut_50": x_sign_bias_test__mutmut_50,
    "x_sign_bias_test__mutmut_51": x_sign_bias_test__mutmut_51,
    "x_sign_bias_test__mutmut_52": x_sign_bias_test__mutmut_52,
    "x_sign_bias_test__mutmut_53": x_sign_bias_test__mutmut_53,
    "x_sign_bias_test__mutmut_54": x_sign_bias_test__mutmut_54,
    "x_sign_bias_test__mutmut_55": x_sign_bias_test__mutmut_55,
    "x_sign_bias_test__mutmut_56": x_sign_bias_test__mutmut_56,
    "x_sign_bias_test__mutmut_57": x_sign_bias_test__mutmut_57,
    "x_sign_bias_test__mutmut_58": x_sign_bias_test__mutmut_58,
    "x_sign_bias_test__mutmut_59": x_sign_bias_test__mutmut_59,
    "x_sign_bias_test__mutmut_60": x_sign_bias_test__mutmut_60,
    "x_sign_bias_test__mutmut_61": x_sign_bias_test__mutmut_61,
    "x_sign_bias_test__mutmut_62": x_sign_bias_test__mutmut_62,
    "x_sign_bias_test__mutmut_63": x_sign_bias_test__mutmut_63,
    "x_sign_bias_test__mutmut_64": x_sign_bias_test__mutmut_64,
    "x_sign_bias_test__mutmut_65": x_sign_bias_test__mutmut_65,
    "x_sign_bias_test__mutmut_66": x_sign_bias_test__mutmut_66,
    "x_sign_bias_test__mutmut_67": x_sign_bias_test__mutmut_67,
    "x_sign_bias_test__mutmut_68": x_sign_bias_test__mutmut_68,
    "x_sign_bias_test__mutmut_69": x_sign_bias_test__mutmut_69,
    "x_sign_bias_test__mutmut_70": x_sign_bias_test__mutmut_70,
    "x_sign_bias_test__mutmut_71": x_sign_bias_test__mutmut_71,
    "x_sign_bias_test__mutmut_72": x_sign_bias_test__mutmut_72,
    "x_sign_bias_test__mutmut_73": x_sign_bias_test__mutmut_73,
    "x_sign_bias_test__mutmut_74": x_sign_bias_test__mutmut_74,
    "x_sign_bias_test__mutmut_75": x_sign_bias_test__mutmut_75,
    "x_sign_bias_test__mutmut_76": x_sign_bias_test__mutmut_76,
    "x_sign_bias_test__mutmut_77": x_sign_bias_test__mutmut_77,
    "x_sign_bias_test__mutmut_78": x_sign_bias_test__mutmut_78,
    "x_sign_bias_test__mutmut_79": x_sign_bias_test__mutmut_79,
    "x_sign_bias_test__mutmut_80": x_sign_bias_test__mutmut_80,
    "x_sign_bias_test__mutmut_81": x_sign_bias_test__mutmut_81,
    "x_sign_bias_test__mutmut_82": x_sign_bias_test__mutmut_82,
    "x_sign_bias_test__mutmut_83": x_sign_bias_test__mutmut_83,
    "x_sign_bias_test__mutmut_84": x_sign_bias_test__mutmut_84,
    "x_sign_bias_test__mutmut_85": x_sign_bias_test__mutmut_85,
    "x_sign_bias_test__mutmut_86": x_sign_bias_test__mutmut_86,
    "x_sign_bias_test__mutmut_87": x_sign_bias_test__mutmut_87,
    "x_sign_bias_test__mutmut_88": x_sign_bias_test__mutmut_88,
    "x_sign_bias_test__mutmut_89": x_sign_bias_test__mutmut_89,
    "x_sign_bias_test__mutmut_90": x_sign_bias_test__mutmut_90,
    "x_sign_bias_test__mutmut_91": x_sign_bias_test__mutmut_91,
    "x_sign_bias_test__mutmut_92": x_sign_bias_test__mutmut_92,
    "x_sign_bias_test__mutmut_93": x_sign_bias_test__mutmut_93,
    "x_sign_bias_test__mutmut_94": x_sign_bias_test__mutmut_94,
    "x_sign_bias_test__mutmut_95": x_sign_bias_test__mutmut_95,
    "x_sign_bias_test__mutmut_96": x_sign_bias_test__mutmut_96,
    "x_sign_bias_test__mutmut_97": x_sign_bias_test__mutmut_97,
    "x_sign_bias_test__mutmut_98": x_sign_bias_test__mutmut_98,
    "x_sign_bias_test__mutmut_99": x_sign_bias_test__mutmut_99,
    "x_sign_bias_test__mutmut_100": x_sign_bias_test__mutmut_100,
    "x_sign_bias_test__mutmut_101": x_sign_bias_test__mutmut_101,
    "x_sign_bias_test__mutmut_102": x_sign_bias_test__mutmut_102,
    "x_sign_bias_test__mutmut_103": x_sign_bias_test__mutmut_103,
    "x_sign_bias_test__mutmut_104": x_sign_bias_test__mutmut_104,
    "x_sign_bias_test__mutmut_105": x_sign_bias_test__mutmut_105,
    "x_sign_bias_test__mutmut_106": x_sign_bias_test__mutmut_106,
    "x_sign_bias_test__mutmut_107": x_sign_bias_test__mutmut_107,
    "x_sign_bias_test__mutmut_108": x_sign_bias_test__mutmut_108,
    "x_sign_bias_test__mutmut_109": x_sign_bias_test__mutmut_109,
    "x_sign_bias_test__mutmut_110": x_sign_bias_test__mutmut_110,
    "x_sign_bias_test__mutmut_111": x_sign_bias_test__mutmut_111,
    "x_sign_bias_test__mutmut_112": x_sign_bias_test__mutmut_112,
    "x_sign_bias_test__mutmut_113": x_sign_bias_test__mutmut_113,
    "x_sign_bias_test__mutmut_114": x_sign_bias_test__mutmut_114,
    "x_sign_bias_test__mutmut_115": x_sign_bias_test__mutmut_115,
    "x_sign_bias_test__mutmut_116": x_sign_bias_test__mutmut_116,
    "x_sign_bias_test__mutmut_117": x_sign_bias_test__mutmut_117,
    "x_sign_bias_test__mutmut_118": x_sign_bias_test__mutmut_118,
    "x_sign_bias_test__mutmut_119": x_sign_bias_test__mutmut_119,
    "x_sign_bias_test__mutmut_120": x_sign_bias_test__mutmut_120,
    "x_sign_bias_test__mutmut_121": x_sign_bias_test__mutmut_121,
    "x_sign_bias_test__mutmut_122": x_sign_bias_test__mutmut_122,
    "x_sign_bias_test__mutmut_123": x_sign_bias_test__mutmut_123,
    "x_sign_bias_test__mutmut_124": x_sign_bias_test__mutmut_124,
    "x_sign_bias_test__mutmut_125": x_sign_bias_test__mutmut_125,
    "x_sign_bias_test__mutmut_126": x_sign_bias_test__mutmut_126,
    "x_sign_bias_test__mutmut_127": x_sign_bias_test__mutmut_127,
    "x_sign_bias_test__mutmut_128": x_sign_bias_test__mutmut_128,
    "x_sign_bias_test__mutmut_129": x_sign_bias_test__mutmut_129,
    "x_sign_bias_test__mutmut_130": x_sign_bias_test__mutmut_130,
    "x_sign_bias_test__mutmut_131": x_sign_bias_test__mutmut_131,
    "x_sign_bias_test__mutmut_132": x_sign_bias_test__mutmut_132,
    "x_sign_bias_test__mutmut_133": x_sign_bias_test__mutmut_133,
    "x_sign_bias_test__mutmut_134": x_sign_bias_test__mutmut_134,
    "x_sign_bias_test__mutmut_135": x_sign_bias_test__mutmut_135,
    "x_sign_bias_test__mutmut_136": x_sign_bias_test__mutmut_136,
    "x_sign_bias_test__mutmut_137": x_sign_bias_test__mutmut_137,
    "x_sign_bias_test__mutmut_138": x_sign_bias_test__mutmut_138,
    "x_sign_bias_test__mutmut_139": x_sign_bias_test__mutmut_139,
    "x_sign_bias_test__mutmut_140": x_sign_bias_test__mutmut_140,
    "x_sign_bias_test__mutmut_141": x_sign_bias_test__mutmut_141,
    "x_sign_bias_test__mutmut_142": x_sign_bias_test__mutmut_142,
    "x_sign_bias_test__mutmut_143": x_sign_bias_test__mutmut_143,
    "x_sign_bias_test__mutmut_144": x_sign_bias_test__mutmut_144,
    "x_sign_bias_test__mutmut_145": x_sign_bias_test__mutmut_145,
    "x_sign_bias_test__mutmut_146": x_sign_bias_test__mutmut_146,
    "x_sign_bias_test__mutmut_147": x_sign_bias_test__mutmut_147,
    "x_sign_bias_test__mutmut_148": x_sign_bias_test__mutmut_148,
    "x_sign_bias_test__mutmut_149": x_sign_bias_test__mutmut_149,
    "x_sign_bias_test__mutmut_150": x_sign_bias_test__mutmut_150,
    "x_sign_bias_test__mutmut_151": x_sign_bias_test__mutmut_151,
    "x_sign_bias_test__mutmut_152": x_sign_bias_test__mutmut_152,
    "x_sign_bias_test__mutmut_153": x_sign_bias_test__mutmut_153,
    "x_sign_bias_test__mutmut_154": x_sign_bias_test__mutmut_154,
    "x_sign_bias_test__mutmut_155": x_sign_bias_test__mutmut_155,
    "x_sign_bias_test__mutmut_156": x_sign_bias_test__mutmut_156,
}
x_sign_bias_test__mutmut_orig.__name__ = "x_sign_bias_test"
