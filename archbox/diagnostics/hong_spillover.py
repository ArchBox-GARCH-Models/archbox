"""Hong (2001) Volatility Spillover Test.

Tests for volatility spillover between two time series.

References
----------
- Hong, Y. (2001). A Test for Volatility Spillover with Application
  to Exchange Rates. Journal of Econometrics, 103(1-2), 183-224.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class HongSpilloverResult:
    """Container for Hong spillover test result.

    Attributes
    ----------
    statistic : float
        Q test statistic (asymptotically N(0,1) under H0).
    pvalue : float
        p-value from standard normal.
    bandwidth : int
        Bandwidth parameter M.
    test_name : str
        Name of the test.
    """

    statistic: float
    pvalue: float
    bandwidth: int
    test_name: str = "Hong Volatility Spillover"

    def __repr__(self) -> str:
        """Return string representation of the test result."""
        return (
            f"{self.test_name}(M={self.bandwidth}): "
            f"statistic={self.statistic:.4f}, pvalue={self.pvalue:.4f}"
        )


def _bartlett_kernel(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) <= 1:
        return 1 - abs(x)
    return 0.0


def hong_spillover_test(
    std_resids_1: object,
    std_resids_2: object,
    bandwidth: int | None = None,
) -> HongSpilloverResult:
    """Hong (2001) test for volatility spillover.

    Tests H0: no volatility spillover from series 2 to series 1.

    Parameters
    ----------
    std_resids_1 : array-like
        Standardized residuals from series 1, z_{1,t}.
    std_resids_2 : array-like
        Standardized residuals from series 2, z_{2,t}.
    bandwidth : int, optional
        Bandwidth parameter M. If None, uses floor(T^{1/3}).

    Returns
    -------
    HongSpilloverResult
        Q statistic (asymptotically N(0,1)) and p-value.

    Notes
    -----
    Q = [T * sum_{j=1}^{T-1} k^2(j/M) * rho^2_{12}(j) - C_T] / sqrt(2 * D_T)

    Where:
        rho_{12}(j) = cross-correlation of squared std residuals at lag j
        k(x) = Bartlett kernel
        C_T = sum_{j=1}^{T-1} k^2(j/M)
        D_T = sum_{j=1}^{T-1} k^4(j/M)
    """
    z1 = np.asarray(std_resids_1, dtype=np.float64).ravel()
    z2 = np.asarray(std_resids_2, dtype=np.float64).ravel()

    if len(z1) != len(z2):
        msg = f"Series must have same length, got {len(z1)} and {len(z2)}"
        raise ValueError(msg)

    n_obs = len(z1)

    if bandwidth is None:
        bandwidth = int(np.floor(n_obs ** (1 / 3)))

    bw = bandwidth

    # Squared standardized residuals (centered)
    u1 = z1**2 - 1  # centered: E[z^2] = 1
    u2 = z2**2 - 1

    # Variance terms for normalization
    gamma_11 = np.sum(u1**2) / n_obs
    gamma_22 = np.sum(u2**2) / n_obs

    denom = np.sqrt(gamma_11 * gamma_22)
    if denom < 1e-20:
        return HongSpilloverResult(statistic=0.0, pvalue=1.0, bandwidth=bw)

    # Compute Q statistic
    weighted_sum = 0.0
    c_t = 0.0
    d_t = 0.0

    for j in range(1, n_obs):
        kj = _bartlett_kernel(j / bw)
        k2 = kj**2

        if k2 < 1e-20:
            continue

        # Cross-correlation at lag j: corr(u1_t, u2_{t-j})
        gamma_12_j = np.sum(u1[j:] * u2[: n_obs - j]) / n_obs
        rho_12_j = gamma_12_j / denom

        weighted_sum += k2 * rho_12_j**2
        c_t += k2
        d_t += kj**4

    q_num = n_obs * weighted_sum - c_t
    q_denom = np.sqrt(2 * d_t)

    if q_denom < 1e-20:
        return HongSpilloverResult(statistic=0.0, pvalue=1.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )
