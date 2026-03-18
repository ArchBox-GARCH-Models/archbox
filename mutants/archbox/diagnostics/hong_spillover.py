"""Hong (2001) Volatility Spillover Test.

Tests for volatility spillover between two time series.

References
----------
- Hong, Y. (2001). A Test for Volatility Spillover with Application
  to Exchange Rates. Journal of Econometrics, 103(1-2), 183-224.
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
    args = [x]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x__bartlett_kernel__mutmut_orig, x__bartlett_kernel__mutmut_mutants, args, kwargs, None
    )


def x__bartlett_kernel__mutmut_orig(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) <= 1:
        return 1 - abs(x)
    return 0.0


def x__bartlett_kernel__mutmut_1(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(None) <= 1:
        return 1 - abs(x)
    return 0.0


def x__bartlett_kernel__mutmut_2(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) < 1:
        return 1 - abs(x)
    return 0.0


def x__bartlett_kernel__mutmut_3(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) <= 2:
        return 1 - abs(x)
    return 0.0


def x__bartlett_kernel__mutmut_4(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) <= 1:
        return 1 + abs(x)
    return 0.0


def x__bartlett_kernel__mutmut_5(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) <= 1:
        return 2 - abs(x)
    return 0.0


def x__bartlett_kernel__mutmut_6(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) <= 1:
        return 1 - abs(None)
    return 0.0


def x__bartlett_kernel__mutmut_7(x: float) -> float:
    """Bartlett kernel: k(x) = (1 - |x|) if |x| <= 1, else 0."""
    if abs(x) <= 1:
        return 1 - abs(x)
    return 1.0


x__bartlett_kernel__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x__bartlett_kernel__mutmut_1": x__bartlett_kernel__mutmut_1,
    "x__bartlett_kernel__mutmut_2": x__bartlett_kernel__mutmut_2,
    "x__bartlett_kernel__mutmut_3": x__bartlett_kernel__mutmut_3,
    "x__bartlett_kernel__mutmut_4": x__bartlett_kernel__mutmut_4,
    "x__bartlett_kernel__mutmut_5": x__bartlett_kernel__mutmut_5,
    "x__bartlett_kernel__mutmut_6": x__bartlett_kernel__mutmut_6,
    "x__bartlett_kernel__mutmut_7": x__bartlett_kernel__mutmut_7,
}
x__bartlett_kernel__mutmut_orig.__name__ = "x__bartlett_kernel"


def hong_spillover_test(
    std_resids_1: object,
    std_resids_2: object,
    bandwidth: int | None = None,
) -> HongSpilloverResult:
    args = [std_resids_1, std_resids_2, bandwidth]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_hong_spillover_test__mutmut_orig,
        x_hong_spillover_test__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_hong_spillover_test__mutmut_orig(
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


def x_hong_spillover_test__mutmut_1(
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
    z1 = None
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


def x_hong_spillover_test__mutmut_2(
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
    z1 = np.asarray(None, dtype=np.float64).ravel()
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


def x_hong_spillover_test__mutmut_3(
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
    z1 = np.asarray(std_resids_1, dtype=None).ravel()
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


def x_hong_spillover_test__mutmut_4(
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
    z1 = np.asarray(dtype=np.float64).ravel()
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


def x_hong_spillover_test__mutmut_5(
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
    z1 = np.asarray(
        std_resids_1,
    ).ravel()
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


def x_hong_spillover_test__mutmut_6(
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
    z2 = None

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


def x_hong_spillover_test__mutmut_7(
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
    z2 = np.asarray(None, dtype=np.float64).ravel()

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


def x_hong_spillover_test__mutmut_8(
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
    z2 = np.asarray(std_resids_2, dtype=None).ravel()

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


def x_hong_spillover_test__mutmut_9(
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
    z2 = np.asarray(dtype=np.float64).ravel()

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


def x_hong_spillover_test__mutmut_10(
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
    z2 = np.asarray(
        std_resids_2,
    ).ravel()

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


def x_hong_spillover_test__mutmut_11(
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

    if len(z1) == len(z2):
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


def x_hong_spillover_test__mutmut_12(
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
        msg = None
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


def x_hong_spillover_test__mutmut_13(
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
        raise ValueError(None)

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


def x_hong_spillover_test__mutmut_14(
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

    n_obs = None

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


def x_hong_spillover_test__mutmut_15(
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

    if bandwidth is not None:
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


def x_hong_spillover_test__mutmut_16(
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
        bandwidth = None

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


def x_hong_spillover_test__mutmut_17(
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
        bandwidth = int(None)

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


def x_hong_spillover_test__mutmut_18(
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
        bandwidth = int(np.floor(None))

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


def x_hong_spillover_test__mutmut_19(
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
        bandwidth = int(np.floor(n_obs * (1 / 3)))

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


def x_hong_spillover_test__mutmut_20(
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
        bandwidth = int(np.floor(n_obs ** (1 * 3)))

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


def x_hong_spillover_test__mutmut_21(
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
        bandwidth = int(np.floor(n_obs ** (2 / 3)))

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


def x_hong_spillover_test__mutmut_22(
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
        bandwidth = int(np.floor(n_obs ** (1 / 4)))

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


def x_hong_spillover_test__mutmut_23(
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

    bw = None

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


def x_hong_spillover_test__mutmut_24(
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
    u1 = None  # centered: E[z^2] = 1
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


def x_hong_spillover_test__mutmut_25(
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
    u1 = z1**2 + 1  # centered: E[z^2] = 1
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


def x_hong_spillover_test__mutmut_26(
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
    u1 = z1 * 2 - 1  # centered: E[z^2] = 1
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


def x_hong_spillover_test__mutmut_27(
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
    u1 = z1**3 - 1  # centered: E[z^2] = 1
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


def x_hong_spillover_test__mutmut_28(
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
    u1 = z1**2 - 2  # centered: E[z^2] = 1
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


def x_hong_spillover_test__mutmut_29(
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
    u2 = None

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


def x_hong_spillover_test__mutmut_30(
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
    u2 = z2**2 + 1

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


def x_hong_spillover_test__mutmut_31(
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
    u2 = z2 * 2 - 1

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


def x_hong_spillover_test__mutmut_32(
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
    u2 = z2**3 - 1

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


def x_hong_spillover_test__mutmut_33(
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
    u2 = z2**2 - 2

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


def x_hong_spillover_test__mutmut_34(
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
    gamma_11 = None
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


def x_hong_spillover_test__mutmut_35(
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
    gamma_11 = np.sum(u1**2) * n_obs
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


def x_hong_spillover_test__mutmut_36(
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
    gamma_11 = np.sum(None) / n_obs
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


def x_hong_spillover_test__mutmut_37(
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
    gamma_11 = np.sum(u1 * 2) / n_obs
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


def x_hong_spillover_test__mutmut_38(
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
    gamma_11 = np.sum(u1**3) / n_obs
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


def x_hong_spillover_test__mutmut_39(
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
    gamma_22 = None

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


def x_hong_spillover_test__mutmut_40(
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
    gamma_22 = np.sum(u2**2) * n_obs

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


def x_hong_spillover_test__mutmut_41(
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
    gamma_22 = np.sum(None) / n_obs

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


def x_hong_spillover_test__mutmut_42(
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
    gamma_22 = np.sum(u2 * 2) / n_obs

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


def x_hong_spillover_test__mutmut_43(
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
    gamma_22 = np.sum(u2**3) / n_obs

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


def x_hong_spillover_test__mutmut_44(
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

    denom = None
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


def x_hong_spillover_test__mutmut_45(
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

    denom = np.sqrt(None)
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


def x_hong_spillover_test__mutmut_46(
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

    denom = np.sqrt(gamma_11 / gamma_22)
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


def x_hong_spillover_test__mutmut_47(
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
    if denom <= 1e-20:
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


def x_hong_spillover_test__mutmut_48(
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
    if denom < 1.0:
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


def x_hong_spillover_test__mutmut_49(
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
        return HongSpilloverResult(statistic=None, pvalue=1.0, bandwidth=bw)

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


def x_hong_spillover_test__mutmut_50(
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
        return HongSpilloverResult(statistic=0.0, pvalue=None, bandwidth=bw)

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


def x_hong_spillover_test__mutmut_51(
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
        return HongSpilloverResult(statistic=0.0, pvalue=1.0, bandwidth=None)

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


def x_hong_spillover_test__mutmut_52(
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
        return HongSpilloverResult(pvalue=1.0, bandwidth=bw)

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


def x_hong_spillover_test__mutmut_53(
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
        return HongSpilloverResult(statistic=0.0, bandwidth=bw)

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


def x_hong_spillover_test__mutmut_54(
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
        return HongSpilloverResult(
            statistic=0.0,
            pvalue=1.0,
        )

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


def x_hong_spillover_test__mutmut_55(
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
        return HongSpilloverResult(statistic=1.0, pvalue=1.0, bandwidth=bw)

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


def x_hong_spillover_test__mutmut_56(
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
        return HongSpilloverResult(statistic=0.0, pvalue=2.0, bandwidth=bw)

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


def x_hong_spillover_test__mutmut_57(
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
    weighted_sum = None
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


def x_hong_spillover_test__mutmut_58(
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
    weighted_sum = 1.0
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


def x_hong_spillover_test__mutmut_59(
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
    c_t = None
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


def x_hong_spillover_test__mutmut_60(
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
    c_t = 1.0
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


def x_hong_spillover_test__mutmut_61(
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
    d_t = None

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


def x_hong_spillover_test__mutmut_62(
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
    d_t = 1.0

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


def x_hong_spillover_test__mutmut_63(
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

    for j in range(None, n_obs):
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


def x_hong_spillover_test__mutmut_64(
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

    for j in range(1, None):
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


def x_hong_spillover_test__mutmut_65(
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

    for j in range(n_obs):
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


def x_hong_spillover_test__mutmut_66(
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

    for j in range(
        1,
    ):
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


def x_hong_spillover_test__mutmut_67(
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

    for j in range(2, n_obs):
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


def x_hong_spillover_test__mutmut_68(
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
        kj = None
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


def x_hong_spillover_test__mutmut_69(
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
        kj = _bartlett_kernel(None)
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


def x_hong_spillover_test__mutmut_70(
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
        kj = _bartlett_kernel(j * bw)
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


def x_hong_spillover_test__mutmut_71(
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
        k2 = None

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


def x_hong_spillover_test__mutmut_72(
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
        k2 = kj * 2

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


def x_hong_spillover_test__mutmut_73(
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
        k2 = kj**3

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


def x_hong_spillover_test__mutmut_74(
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

        if k2 <= 1e-20:
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


def x_hong_spillover_test__mutmut_75(
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

        if k2 < 1.0:
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


def x_hong_spillover_test__mutmut_76(
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
            break

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


def x_hong_spillover_test__mutmut_77(
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
        gamma_12_j = None
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


def x_hong_spillover_test__mutmut_78(
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
        gamma_12_j = np.sum(u1[j:] * u2[: n_obs - j]) * n_obs
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


def x_hong_spillover_test__mutmut_79(
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
        gamma_12_j = np.sum(None) / n_obs
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


def x_hong_spillover_test__mutmut_80(
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
        gamma_12_j = np.sum(u1[j:] / u2[: n_obs - j]) / n_obs
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


def x_hong_spillover_test__mutmut_81(
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
        gamma_12_j = np.sum(u1[j:] * u2[: n_obs + j]) / n_obs
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


def x_hong_spillover_test__mutmut_82(
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
        rho_12_j = None

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


def x_hong_spillover_test__mutmut_83(
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
        rho_12_j = gamma_12_j * denom

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


def x_hong_spillover_test__mutmut_84(
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

        weighted_sum = k2 * rho_12_j**2
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


def x_hong_spillover_test__mutmut_85(
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

        weighted_sum -= k2 * rho_12_j**2
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


def x_hong_spillover_test__mutmut_86(
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

        weighted_sum += k2 / rho_12_j**2
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


def x_hong_spillover_test__mutmut_87(
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

        weighted_sum += k2 * rho_12_j * 2
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


def x_hong_spillover_test__mutmut_88(
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

        weighted_sum += k2 * rho_12_j**3
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


def x_hong_spillover_test__mutmut_89(
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
        c_t = k2
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


def x_hong_spillover_test__mutmut_90(
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
        c_t -= k2
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


def x_hong_spillover_test__mutmut_91(
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
        d_t = kj**4

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


def x_hong_spillover_test__mutmut_92(
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
        d_t -= kj**4

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


def x_hong_spillover_test__mutmut_93(
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
        d_t += kj * 4

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


def x_hong_spillover_test__mutmut_94(
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
        d_t += kj**5

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


def x_hong_spillover_test__mutmut_95(
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

    q_num = None
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


def x_hong_spillover_test__mutmut_96(
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

    q_num = n_obs * weighted_sum + c_t
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


def x_hong_spillover_test__mutmut_97(
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

    q_num = n_obs / weighted_sum - c_t
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


def x_hong_spillover_test__mutmut_98(
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
    q_denom = None

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


def x_hong_spillover_test__mutmut_99(
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
    q_denom = np.sqrt(None)

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


def x_hong_spillover_test__mutmut_100(
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
    q_denom = np.sqrt(2 / d_t)

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


def x_hong_spillover_test__mutmut_101(
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
    q_denom = np.sqrt(3 * d_t)

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


def x_hong_spillover_test__mutmut_102(
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

    if q_denom <= 1e-20:
        return HongSpilloverResult(statistic=0.0, pvalue=1.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_103(
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

    if q_denom < 1.0:
        return HongSpilloverResult(statistic=0.0, pvalue=1.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_104(
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
        return HongSpilloverResult(statistic=None, pvalue=1.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_105(
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
        return HongSpilloverResult(statistic=0.0, pvalue=None, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_106(
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
        return HongSpilloverResult(statistic=0.0, pvalue=1.0, bandwidth=None)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_107(
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
        return HongSpilloverResult(pvalue=1.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_108(
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
        return HongSpilloverResult(statistic=0.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_109(
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
        return HongSpilloverResult(
            statistic=0.0,
            pvalue=1.0,
        )

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_110(
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
        return HongSpilloverResult(statistic=1.0, pvalue=1.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_111(
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
        return HongSpilloverResult(statistic=0.0, pvalue=2.0, bandwidth=bw)

    q_stat = q_num / q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_112(
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

    q_stat = None

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_113(
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

    q_stat = q_num * q_denom

    # One-sided test (right tail)
    pvalue = float(1 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_114(
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
    pvalue = None

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_115(
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
    pvalue = float(None)

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_116(
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
    pvalue = float(1 + stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_117(
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
    pvalue = float(2 - stats.norm.cdf(q_stat))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_118(
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
    pvalue = float(1 - stats.norm.cdf(None))

    return HongSpilloverResult(
        statistic=float(q_stat),
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_119(
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
        statistic=None,
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_120(
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
        pvalue=None,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_121(
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
        bandwidth=None,
    )


def x_hong_spillover_test__mutmut_122(
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
        pvalue=pvalue,
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_123(
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
        bandwidth=bw,
    )


def x_hong_spillover_test__mutmut_124(
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
    )


def x_hong_spillover_test__mutmut_125(
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
        statistic=float(None),
        pvalue=pvalue,
        bandwidth=bw,
    )


x_hong_spillover_test__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_hong_spillover_test__mutmut_1": x_hong_spillover_test__mutmut_1,
    "x_hong_spillover_test__mutmut_2": x_hong_spillover_test__mutmut_2,
    "x_hong_spillover_test__mutmut_3": x_hong_spillover_test__mutmut_3,
    "x_hong_spillover_test__mutmut_4": x_hong_spillover_test__mutmut_4,
    "x_hong_spillover_test__mutmut_5": x_hong_spillover_test__mutmut_5,
    "x_hong_spillover_test__mutmut_6": x_hong_spillover_test__mutmut_6,
    "x_hong_spillover_test__mutmut_7": x_hong_spillover_test__mutmut_7,
    "x_hong_spillover_test__mutmut_8": x_hong_spillover_test__mutmut_8,
    "x_hong_spillover_test__mutmut_9": x_hong_spillover_test__mutmut_9,
    "x_hong_spillover_test__mutmut_10": x_hong_spillover_test__mutmut_10,
    "x_hong_spillover_test__mutmut_11": x_hong_spillover_test__mutmut_11,
    "x_hong_spillover_test__mutmut_12": x_hong_spillover_test__mutmut_12,
    "x_hong_spillover_test__mutmut_13": x_hong_spillover_test__mutmut_13,
    "x_hong_spillover_test__mutmut_14": x_hong_spillover_test__mutmut_14,
    "x_hong_spillover_test__mutmut_15": x_hong_spillover_test__mutmut_15,
    "x_hong_spillover_test__mutmut_16": x_hong_spillover_test__mutmut_16,
    "x_hong_spillover_test__mutmut_17": x_hong_spillover_test__mutmut_17,
    "x_hong_spillover_test__mutmut_18": x_hong_spillover_test__mutmut_18,
    "x_hong_spillover_test__mutmut_19": x_hong_spillover_test__mutmut_19,
    "x_hong_spillover_test__mutmut_20": x_hong_spillover_test__mutmut_20,
    "x_hong_spillover_test__mutmut_21": x_hong_spillover_test__mutmut_21,
    "x_hong_spillover_test__mutmut_22": x_hong_spillover_test__mutmut_22,
    "x_hong_spillover_test__mutmut_23": x_hong_spillover_test__mutmut_23,
    "x_hong_spillover_test__mutmut_24": x_hong_spillover_test__mutmut_24,
    "x_hong_spillover_test__mutmut_25": x_hong_spillover_test__mutmut_25,
    "x_hong_spillover_test__mutmut_26": x_hong_spillover_test__mutmut_26,
    "x_hong_spillover_test__mutmut_27": x_hong_spillover_test__mutmut_27,
    "x_hong_spillover_test__mutmut_28": x_hong_spillover_test__mutmut_28,
    "x_hong_spillover_test__mutmut_29": x_hong_spillover_test__mutmut_29,
    "x_hong_spillover_test__mutmut_30": x_hong_spillover_test__mutmut_30,
    "x_hong_spillover_test__mutmut_31": x_hong_spillover_test__mutmut_31,
    "x_hong_spillover_test__mutmut_32": x_hong_spillover_test__mutmut_32,
    "x_hong_spillover_test__mutmut_33": x_hong_spillover_test__mutmut_33,
    "x_hong_spillover_test__mutmut_34": x_hong_spillover_test__mutmut_34,
    "x_hong_spillover_test__mutmut_35": x_hong_spillover_test__mutmut_35,
    "x_hong_spillover_test__mutmut_36": x_hong_spillover_test__mutmut_36,
    "x_hong_spillover_test__mutmut_37": x_hong_spillover_test__mutmut_37,
    "x_hong_spillover_test__mutmut_38": x_hong_spillover_test__mutmut_38,
    "x_hong_spillover_test__mutmut_39": x_hong_spillover_test__mutmut_39,
    "x_hong_spillover_test__mutmut_40": x_hong_spillover_test__mutmut_40,
    "x_hong_spillover_test__mutmut_41": x_hong_spillover_test__mutmut_41,
    "x_hong_spillover_test__mutmut_42": x_hong_spillover_test__mutmut_42,
    "x_hong_spillover_test__mutmut_43": x_hong_spillover_test__mutmut_43,
    "x_hong_spillover_test__mutmut_44": x_hong_spillover_test__mutmut_44,
    "x_hong_spillover_test__mutmut_45": x_hong_spillover_test__mutmut_45,
    "x_hong_spillover_test__mutmut_46": x_hong_spillover_test__mutmut_46,
    "x_hong_spillover_test__mutmut_47": x_hong_spillover_test__mutmut_47,
    "x_hong_spillover_test__mutmut_48": x_hong_spillover_test__mutmut_48,
    "x_hong_spillover_test__mutmut_49": x_hong_spillover_test__mutmut_49,
    "x_hong_spillover_test__mutmut_50": x_hong_spillover_test__mutmut_50,
    "x_hong_spillover_test__mutmut_51": x_hong_spillover_test__mutmut_51,
    "x_hong_spillover_test__mutmut_52": x_hong_spillover_test__mutmut_52,
    "x_hong_spillover_test__mutmut_53": x_hong_spillover_test__mutmut_53,
    "x_hong_spillover_test__mutmut_54": x_hong_spillover_test__mutmut_54,
    "x_hong_spillover_test__mutmut_55": x_hong_spillover_test__mutmut_55,
    "x_hong_spillover_test__mutmut_56": x_hong_spillover_test__mutmut_56,
    "x_hong_spillover_test__mutmut_57": x_hong_spillover_test__mutmut_57,
    "x_hong_spillover_test__mutmut_58": x_hong_spillover_test__mutmut_58,
    "x_hong_spillover_test__mutmut_59": x_hong_spillover_test__mutmut_59,
    "x_hong_spillover_test__mutmut_60": x_hong_spillover_test__mutmut_60,
    "x_hong_spillover_test__mutmut_61": x_hong_spillover_test__mutmut_61,
    "x_hong_spillover_test__mutmut_62": x_hong_spillover_test__mutmut_62,
    "x_hong_spillover_test__mutmut_63": x_hong_spillover_test__mutmut_63,
    "x_hong_spillover_test__mutmut_64": x_hong_spillover_test__mutmut_64,
    "x_hong_spillover_test__mutmut_65": x_hong_spillover_test__mutmut_65,
    "x_hong_spillover_test__mutmut_66": x_hong_spillover_test__mutmut_66,
    "x_hong_spillover_test__mutmut_67": x_hong_spillover_test__mutmut_67,
    "x_hong_spillover_test__mutmut_68": x_hong_spillover_test__mutmut_68,
    "x_hong_spillover_test__mutmut_69": x_hong_spillover_test__mutmut_69,
    "x_hong_spillover_test__mutmut_70": x_hong_spillover_test__mutmut_70,
    "x_hong_spillover_test__mutmut_71": x_hong_spillover_test__mutmut_71,
    "x_hong_spillover_test__mutmut_72": x_hong_spillover_test__mutmut_72,
    "x_hong_spillover_test__mutmut_73": x_hong_spillover_test__mutmut_73,
    "x_hong_spillover_test__mutmut_74": x_hong_spillover_test__mutmut_74,
    "x_hong_spillover_test__mutmut_75": x_hong_spillover_test__mutmut_75,
    "x_hong_spillover_test__mutmut_76": x_hong_spillover_test__mutmut_76,
    "x_hong_spillover_test__mutmut_77": x_hong_spillover_test__mutmut_77,
    "x_hong_spillover_test__mutmut_78": x_hong_spillover_test__mutmut_78,
    "x_hong_spillover_test__mutmut_79": x_hong_spillover_test__mutmut_79,
    "x_hong_spillover_test__mutmut_80": x_hong_spillover_test__mutmut_80,
    "x_hong_spillover_test__mutmut_81": x_hong_spillover_test__mutmut_81,
    "x_hong_spillover_test__mutmut_82": x_hong_spillover_test__mutmut_82,
    "x_hong_spillover_test__mutmut_83": x_hong_spillover_test__mutmut_83,
    "x_hong_spillover_test__mutmut_84": x_hong_spillover_test__mutmut_84,
    "x_hong_spillover_test__mutmut_85": x_hong_spillover_test__mutmut_85,
    "x_hong_spillover_test__mutmut_86": x_hong_spillover_test__mutmut_86,
    "x_hong_spillover_test__mutmut_87": x_hong_spillover_test__mutmut_87,
    "x_hong_spillover_test__mutmut_88": x_hong_spillover_test__mutmut_88,
    "x_hong_spillover_test__mutmut_89": x_hong_spillover_test__mutmut_89,
    "x_hong_spillover_test__mutmut_90": x_hong_spillover_test__mutmut_90,
    "x_hong_spillover_test__mutmut_91": x_hong_spillover_test__mutmut_91,
    "x_hong_spillover_test__mutmut_92": x_hong_spillover_test__mutmut_92,
    "x_hong_spillover_test__mutmut_93": x_hong_spillover_test__mutmut_93,
    "x_hong_spillover_test__mutmut_94": x_hong_spillover_test__mutmut_94,
    "x_hong_spillover_test__mutmut_95": x_hong_spillover_test__mutmut_95,
    "x_hong_spillover_test__mutmut_96": x_hong_spillover_test__mutmut_96,
    "x_hong_spillover_test__mutmut_97": x_hong_spillover_test__mutmut_97,
    "x_hong_spillover_test__mutmut_98": x_hong_spillover_test__mutmut_98,
    "x_hong_spillover_test__mutmut_99": x_hong_spillover_test__mutmut_99,
    "x_hong_spillover_test__mutmut_100": x_hong_spillover_test__mutmut_100,
    "x_hong_spillover_test__mutmut_101": x_hong_spillover_test__mutmut_101,
    "x_hong_spillover_test__mutmut_102": x_hong_spillover_test__mutmut_102,
    "x_hong_spillover_test__mutmut_103": x_hong_spillover_test__mutmut_103,
    "x_hong_spillover_test__mutmut_104": x_hong_spillover_test__mutmut_104,
    "x_hong_spillover_test__mutmut_105": x_hong_spillover_test__mutmut_105,
    "x_hong_spillover_test__mutmut_106": x_hong_spillover_test__mutmut_106,
    "x_hong_spillover_test__mutmut_107": x_hong_spillover_test__mutmut_107,
    "x_hong_spillover_test__mutmut_108": x_hong_spillover_test__mutmut_108,
    "x_hong_spillover_test__mutmut_109": x_hong_spillover_test__mutmut_109,
    "x_hong_spillover_test__mutmut_110": x_hong_spillover_test__mutmut_110,
    "x_hong_spillover_test__mutmut_111": x_hong_spillover_test__mutmut_111,
    "x_hong_spillover_test__mutmut_112": x_hong_spillover_test__mutmut_112,
    "x_hong_spillover_test__mutmut_113": x_hong_spillover_test__mutmut_113,
    "x_hong_spillover_test__mutmut_114": x_hong_spillover_test__mutmut_114,
    "x_hong_spillover_test__mutmut_115": x_hong_spillover_test__mutmut_115,
    "x_hong_spillover_test__mutmut_116": x_hong_spillover_test__mutmut_116,
    "x_hong_spillover_test__mutmut_117": x_hong_spillover_test__mutmut_117,
    "x_hong_spillover_test__mutmut_118": x_hong_spillover_test__mutmut_118,
    "x_hong_spillover_test__mutmut_119": x_hong_spillover_test__mutmut_119,
    "x_hong_spillover_test__mutmut_120": x_hong_spillover_test__mutmut_120,
    "x_hong_spillover_test__mutmut_121": x_hong_spillover_test__mutmut_121,
    "x_hong_spillover_test__mutmut_122": x_hong_spillover_test__mutmut_122,
    "x_hong_spillover_test__mutmut_123": x_hong_spillover_test__mutmut_123,
    "x_hong_spillover_test__mutmut_124": x_hong_spillover_test__mutmut_124,
    "x_hong_spillover_test__mutmut_125": x_hong_spillover_test__mutmut_125,
}
x_hong_spillover_test__mutmut_orig.__name__ = "x_hong_spillover_test"
