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
