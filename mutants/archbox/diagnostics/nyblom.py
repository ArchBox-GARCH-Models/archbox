"""Nyblom (1989) Parameter Stability Test.

Tests H0: parameters are constant over time.

References
----------
- Nyblom, J. (1989). Testing for the Constancy of Parameters Over Time.
  Journal of the American Statistical Association, 84(405), 223-230.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

# Asymptotic critical values (Hansen, 1990; Nyblom, 1989)
# Rows: number of parameters (1, 2, ..., 10)
# Columns: 10%, 5%, 1%
_CRITICAL_VALUES = {
    1: (0.353, 0.470, 0.748),
    2: (0.466, 0.574, 0.868),
    3: (0.573, 0.678, 0.982),
    4: (0.676, 0.778, 1.088),
    5: (0.775, 0.877, 1.190),
    6: (0.871, 0.973, 1.289),
    7: (0.964, 1.066, 1.385),
    8: (1.055, 1.157, 1.479),
    9: (1.144, 1.246, 1.571),
    10: (1.231, 1.334, 1.661),
}
from collections.abc import Callable
from typing import Annotated, ClassVar

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
class NyblomResult:
    """Container for Nyblom stability test result.

    Attributes
    ----------
    joint_statistic : float
        Joint test statistic L_c.
    individual_statistics : NDArray[np.float64]
        Individual test statistics L_i for each parameter.
    critical_values_joint : tuple[float, float, float]
        Critical values (10%, 5%, 1%) for joint test.
    critical_values_individual : tuple[float, float, float]
        Critical values (10%, 5%, 1%) for individual tests.
    num_params : int
        Number of parameters tested.
    test_name : str
        Name of the test.
    """

    joint_statistic: float
    individual_statistics: NDArray[np.float64]
    critical_values_joint: tuple[float, float, float]
    critical_values_individual: tuple[float, float, float]
    num_params: int
    test_name: str = "Nyblom Stability"

    @property
    def joint_rejects_5pct(self) -> bool:
        """Whether joint test rejects at 5% level."""
        return self.joint_statistic > self.critical_values_joint[1]

    def __repr__(self) -> str:
        """Return string representation of Nyblom stability test results."""
        cv = self.critical_values_joint
        lines = [
            f"Nyblom Stability Test (k={self.num_params})",
            f"  Joint statistic: {self.joint_statistic:.4f}",
            f"  Critical values: 10%={cv[0]:.3f}, 5%={cv[1]:.3f}, 1%={cv[2]:.3f}",
            f"  Rejects at 5%: {self.joint_rejects_5pct}",
            "  Individual statistics:",
        ]
        for i, stat in enumerate(self.individual_statistics):
            lines.append(f"    param[{i}]: {stat:.4f}")
        return "\n".join(lines)


def nyblom_test(scores: object) -> NyblomResult:
    args = [scores]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_nyblom_test__mutmut_orig, x_nyblom_test__mutmut_mutants, args, kwargs, None
    )


def x_nyblom_test__mutmut_orig(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_1(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = None
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_2(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(None, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_3(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=None)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_4(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_5(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(
        scores,
    )
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_6(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim != 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_7(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 2:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_8(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = None

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_9(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(None, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_10(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, None)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_11(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_12(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(
            -1,
        )

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_13(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(+1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_14(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-2, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_15(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 2)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_16(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = None

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_17(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = None  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_18(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(None, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_19(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=None)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_20(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_21(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(
        scores_arr,
    )  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_22(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=1)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_23(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = None  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_24(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr * n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_25(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = None
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_26(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(None)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_27(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = None

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_28(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(None)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_29(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = None
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_30(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 1.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_31(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(None):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_32(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat = float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_33(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat -= float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_34(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(None)
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_35(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat = n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_36(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat *= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_37(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs / n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_38(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = None
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_39(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(None)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_40(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = None
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_41(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(None, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_42(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, None)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_43(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_44(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(
        var_diag,
    )
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_45(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1.0)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_46(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = None

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_47(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) * (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_48(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(None, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_49(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=None) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_50(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_51(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(
        cum_scores**2,
    ) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_52(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores * 2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_53(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**3, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_54(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=1) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_55(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs / var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_56(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs / n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_57(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = None
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_58(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(None, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_59(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, None)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_60(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_61(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(
        k,
    )
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_62(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 11)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_63(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = None
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_64(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(None, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_65(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv)
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_66(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get((0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_67(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(
        k_cv,
    )
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_68(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 / k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_69(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (1.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_70(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 / k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_71(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 1.47 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_72(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 / k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_73(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 1.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_74(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = None

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_75(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[2]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_76(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=None,
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_77(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=None,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_78(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=None,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_79(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=None,
        num_params=k,
    )


def x_nyblom_test__mutmut_80(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=None,
    )


def x_nyblom_test__mutmut_81(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_82(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_83(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_individual=cv_individual,
        num_params=k,
    )


def x_nyblom_test__mutmut_84(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        num_params=k,
    )


def x_nyblom_test__mutmut_85(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(joint_stat),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
    )


def x_nyblom_test__mutmut_86(scores: object) -> NyblomResult:
    """Nyblom (1989) parameter stability test.

    Parameters
    ----------
    scores : array-like
        Score matrix (T x k), where T is the number of observations
        and k is the number of parameters.
        g_t = d(loglik_t) / d(theta) evaluated at the MLE.

    Returns
    -------
    NyblomResult
        Joint and individual test statistics with critical values.

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)

    n_obs, k = scores_arr.shape

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = 0.0
    for t in range(n_obs):
        joint_stat += float(cum_scores[t] @ var_inv @ cum_scores[t])
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    # Critical values
    k_cv = min(k, 10)
    cv_joint = _CRITICAL_VALUES.get(k_cv, (0.353 * k_cv, 0.470 * k_cv, 0.748 * k_cv))
    cv_individual = _CRITICAL_VALUES[1]

    return NyblomResult(
        joint_statistic=float(None),
        individual_statistics=individual_stats,
        critical_values_joint=cv_joint,
        critical_values_individual=cv_individual,
        num_params=k,
    )


x_nyblom_test__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_nyblom_test__mutmut_1": x_nyblom_test__mutmut_1,
    "x_nyblom_test__mutmut_2": x_nyblom_test__mutmut_2,
    "x_nyblom_test__mutmut_3": x_nyblom_test__mutmut_3,
    "x_nyblom_test__mutmut_4": x_nyblom_test__mutmut_4,
    "x_nyblom_test__mutmut_5": x_nyblom_test__mutmut_5,
    "x_nyblom_test__mutmut_6": x_nyblom_test__mutmut_6,
    "x_nyblom_test__mutmut_7": x_nyblom_test__mutmut_7,
    "x_nyblom_test__mutmut_8": x_nyblom_test__mutmut_8,
    "x_nyblom_test__mutmut_9": x_nyblom_test__mutmut_9,
    "x_nyblom_test__mutmut_10": x_nyblom_test__mutmut_10,
    "x_nyblom_test__mutmut_11": x_nyblom_test__mutmut_11,
    "x_nyblom_test__mutmut_12": x_nyblom_test__mutmut_12,
    "x_nyblom_test__mutmut_13": x_nyblom_test__mutmut_13,
    "x_nyblom_test__mutmut_14": x_nyblom_test__mutmut_14,
    "x_nyblom_test__mutmut_15": x_nyblom_test__mutmut_15,
    "x_nyblom_test__mutmut_16": x_nyblom_test__mutmut_16,
    "x_nyblom_test__mutmut_17": x_nyblom_test__mutmut_17,
    "x_nyblom_test__mutmut_18": x_nyblom_test__mutmut_18,
    "x_nyblom_test__mutmut_19": x_nyblom_test__mutmut_19,
    "x_nyblom_test__mutmut_20": x_nyblom_test__mutmut_20,
    "x_nyblom_test__mutmut_21": x_nyblom_test__mutmut_21,
    "x_nyblom_test__mutmut_22": x_nyblom_test__mutmut_22,
    "x_nyblom_test__mutmut_23": x_nyblom_test__mutmut_23,
    "x_nyblom_test__mutmut_24": x_nyblom_test__mutmut_24,
    "x_nyblom_test__mutmut_25": x_nyblom_test__mutmut_25,
    "x_nyblom_test__mutmut_26": x_nyblom_test__mutmut_26,
    "x_nyblom_test__mutmut_27": x_nyblom_test__mutmut_27,
    "x_nyblom_test__mutmut_28": x_nyblom_test__mutmut_28,
    "x_nyblom_test__mutmut_29": x_nyblom_test__mutmut_29,
    "x_nyblom_test__mutmut_30": x_nyblom_test__mutmut_30,
    "x_nyblom_test__mutmut_31": x_nyblom_test__mutmut_31,
    "x_nyblom_test__mutmut_32": x_nyblom_test__mutmut_32,
    "x_nyblom_test__mutmut_33": x_nyblom_test__mutmut_33,
    "x_nyblom_test__mutmut_34": x_nyblom_test__mutmut_34,
    "x_nyblom_test__mutmut_35": x_nyblom_test__mutmut_35,
    "x_nyblom_test__mutmut_36": x_nyblom_test__mutmut_36,
    "x_nyblom_test__mutmut_37": x_nyblom_test__mutmut_37,
    "x_nyblom_test__mutmut_38": x_nyblom_test__mutmut_38,
    "x_nyblom_test__mutmut_39": x_nyblom_test__mutmut_39,
    "x_nyblom_test__mutmut_40": x_nyblom_test__mutmut_40,
    "x_nyblom_test__mutmut_41": x_nyblom_test__mutmut_41,
    "x_nyblom_test__mutmut_42": x_nyblom_test__mutmut_42,
    "x_nyblom_test__mutmut_43": x_nyblom_test__mutmut_43,
    "x_nyblom_test__mutmut_44": x_nyblom_test__mutmut_44,
    "x_nyblom_test__mutmut_45": x_nyblom_test__mutmut_45,
    "x_nyblom_test__mutmut_46": x_nyblom_test__mutmut_46,
    "x_nyblom_test__mutmut_47": x_nyblom_test__mutmut_47,
    "x_nyblom_test__mutmut_48": x_nyblom_test__mutmut_48,
    "x_nyblom_test__mutmut_49": x_nyblom_test__mutmut_49,
    "x_nyblom_test__mutmut_50": x_nyblom_test__mutmut_50,
    "x_nyblom_test__mutmut_51": x_nyblom_test__mutmut_51,
    "x_nyblom_test__mutmut_52": x_nyblom_test__mutmut_52,
    "x_nyblom_test__mutmut_53": x_nyblom_test__mutmut_53,
    "x_nyblom_test__mutmut_54": x_nyblom_test__mutmut_54,
    "x_nyblom_test__mutmut_55": x_nyblom_test__mutmut_55,
    "x_nyblom_test__mutmut_56": x_nyblom_test__mutmut_56,
    "x_nyblom_test__mutmut_57": x_nyblom_test__mutmut_57,
    "x_nyblom_test__mutmut_58": x_nyblom_test__mutmut_58,
    "x_nyblom_test__mutmut_59": x_nyblom_test__mutmut_59,
    "x_nyblom_test__mutmut_60": x_nyblom_test__mutmut_60,
    "x_nyblom_test__mutmut_61": x_nyblom_test__mutmut_61,
    "x_nyblom_test__mutmut_62": x_nyblom_test__mutmut_62,
    "x_nyblom_test__mutmut_63": x_nyblom_test__mutmut_63,
    "x_nyblom_test__mutmut_64": x_nyblom_test__mutmut_64,
    "x_nyblom_test__mutmut_65": x_nyblom_test__mutmut_65,
    "x_nyblom_test__mutmut_66": x_nyblom_test__mutmut_66,
    "x_nyblom_test__mutmut_67": x_nyblom_test__mutmut_67,
    "x_nyblom_test__mutmut_68": x_nyblom_test__mutmut_68,
    "x_nyblom_test__mutmut_69": x_nyblom_test__mutmut_69,
    "x_nyblom_test__mutmut_70": x_nyblom_test__mutmut_70,
    "x_nyblom_test__mutmut_71": x_nyblom_test__mutmut_71,
    "x_nyblom_test__mutmut_72": x_nyblom_test__mutmut_72,
    "x_nyblom_test__mutmut_73": x_nyblom_test__mutmut_73,
    "x_nyblom_test__mutmut_74": x_nyblom_test__mutmut_74,
    "x_nyblom_test__mutmut_75": x_nyblom_test__mutmut_75,
    "x_nyblom_test__mutmut_76": x_nyblom_test__mutmut_76,
    "x_nyblom_test__mutmut_77": x_nyblom_test__mutmut_77,
    "x_nyblom_test__mutmut_78": x_nyblom_test__mutmut_78,
    "x_nyblom_test__mutmut_79": x_nyblom_test__mutmut_79,
    "x_nyblom_test__mutmut_80": x_nyblom_test__mutmut_80,
    "x_nyblom_test__mutmut_81": x_nyblom_test__mutmut_81,
    "x_nyblom_test__mutmut_82": x_nyblom_test__mutmut_82,
    "x_nyblom_test__mutmut_83": x_nyblom_test__mutmut_83,
    "x_nyblom_test__mutmut_84": x_nyblom_test__mutmut_84,
    "x_nyblom_test__mutmut_85": x_nyblom_test__mutmut_85,
    "x_nyblom_test__mutmut_86": x_nyblom_test__mutmut_86,
}
x_nyblom_test__mutmut_orig.__name__ = "x_nyblom_test"
