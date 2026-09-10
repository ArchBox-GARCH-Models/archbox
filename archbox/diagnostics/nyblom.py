"""Nyblom (1989) Parameter Stability Test.

Tests H0: parameters are constant over time.

References
----------
- Nyblom, J. (1989). Testing for the Constancy of Parameters Over Time.
  Journal of the American Statistical Association, 84(405), 223-230.
- Hansen, B.E. (1992). Testing for Parameter Instability in Linear Models.
  Journal of Policy Modeling, 14(4), 517-533.  Table 1 tabulates the
  asymptotic critical values of the joint statistic for k = 1, ..., 20.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

#: Largest number of parameters for which tabulated critical values exist.
MAX_NYBLOM_PARAMS = 20

# Asymptotic critical values of the joint statistic L_c (Hansen, 1992, Table 1);
# the same table is used by rugarch's ``nyblom()``.
# Key: number of parameters k.  Value: (10%, 5%, 1%) critical values.
#
# Under H0 the joint statistic converges to int_0^1 ||B_k(r)||^2 dr, where
# B_k is a k-dimensional standard Brownian bridge, i.e. to the sum of k
# independent Cramer-von Mises variates.  Simulating that functional
# (4e5 draws, 2000-step grid) reproduces every entry below to within
# Monte-Carlo error (<= 0.02 at the 1% level, <= 0.01 at 5% and 10%), so the
# table is used as published rather than re-simulated at import time.
_CRITICAL_VALUES: dict[int, tuple[float, float, float]] = {
    1: (0.353, 0.470, 0.748),
    2: (0.610, 0.749, 1.07),
    3: (0.846, 1.01, 1.35),
    4: (1.07, 1.24, 1.60),
    5: (1.28, 1.47, 1.88),
    6: (1.49, 1.68, 2.12),
    7: (1.69, 1.90, 2.35),
    8: (1.89, 2.11, 2.59),
    9: (2.10, 2.32, 2.82),
    10: (2.29, 2.54, 3.05),
    11: (2.49, 2.75, 3.27),
    12: (2.69, 2.96, 3.51),
    13: (2.89, 3.15, 3.69),
    14: (3.08, 3.34, 3.90),
    15: (3.26, 3.54, 4.07),
    16: (3.46, 3.75, 4.30),
    17: (3.64, 3.95, 4.51),
    18: (3.83, 4.14, 4.73),
    19: (4.03, 4.33, 4.92),
    20: (4.22, 4.52, 5.13),
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
        Critical values (10%, 5%, 1%) for the joint test.
    critical_values_individual : tuple[float, float, float]
        Critical values (10%, 5%, 1%) for the individual tests.
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

    Raises
    ------
    ValueError
        If the score matrix is not (T x k) with T > k >= 1, or if k exceeds
        :data:`MAX_NYBLOM_PARAMS` (no tabulated critical values are available
        beyond k = 20 and extrapolating them is not sound).

    Notes
    -----
    Joint statistic:
        L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t

    Individual statistic:
        L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}

    Where:
        S_t = sum_{s=1}^{t} g_s  (cumulative sum of scores)
        V = (1/T) * sum_t g_t * g_t'  (variance of scores)

    The critical values are those of Hansen (1992, Table 1); the individual
    statistics are compared against the k = 1 row.  Both are upper-tail
    critical values: reject constancy when the statistic exceeds them.
    """
    scores_arr = np.asarray(scores, dtype=np.float64)
    if scores_arr.ndim == 1:
        scores_arr = scores_arr.reshape(-1, 1)
    if scores_arr.ndim != 2:
        msg = f"scores must be 1D or 2D (T x k), got {scores_arr.ndim}D"
        raise ValueError(msg)

    n_obs, k = scores_arr.shape
    if k < 1 or n_obs <= k:
        msg = f"scores must be (T x k) with T > k >= 1, got T={n_obs}, k={k}"
        raise ValueError(msg)
    if k > MAX_NYBLOM_PARAMS:
        msg = (
            f"no tabulated Nyblom critical values for k={k} parameters "
            f"(Hansen 1992 Table 1 stops at k={MAX_NYBLOM_PARAMS})"
        )
        raise ValueError(msg)

    # Cumulative sum of scores
    cum_scores = np.cumsum(scores_arr, axis=0)  # (n_obs, k)

    # Variance of scores: V = (1/T) * sum_t g_t * g_t'
    var_scores = scores_arr.T @ scores_arr / n_obs  # (k, k)

    try:
        var_inv = np.linalg.inv(var_scores)
    except np.linalg.LinAlgError:
        var_inv = np.linalg.pinv(var_scores)

    # Joint statistic: L_c = (1/T^2) * sum_t S_t' * V^{-1} * S_t
    joint_stat = float(np.einsum("ti,ij,tj->", cum_scores, var_inv, cum_scores))
    joint_stat /= n_obs * n_obs

    # Individual statistics: L_i = (1/T^2) * sum_t S_{i,t}^2 / V_{ii}
    var_diag = np.diag(var_scores)
    var_diag_safe = np.maximum(var_diag, 1e-20)
    individual_stats = np.sum(cum_scores**2, axis=0) / (n_obs * n_obs * var_diag_safe)

    return NyblomResult(
        joint_statistic=joint_stat,
        individual_statistics=individual_stats,
        critical_values_joint=_CRITICAL_VALUES[k],
        critical_values_individual=_CRITICAL_VALUES[1],
        num_params=k,
    )
