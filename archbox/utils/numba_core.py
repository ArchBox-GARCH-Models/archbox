"""Numba-optimized core functions for archbox.

These functions provide JIT-compiled versions of the critical inner loops.
If numba is not installed, equivalent pure Python functions are used instead.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

try:
    from numba import njit

    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

    def njit(*args, **kwargs):  # type: ignore[misc]
        """No-op decorator when numba is not available."""
        if len(args) == 1 and callable(args[0]):
            return args[0]

        def decorator(func):  # type: ignore[no-untyped-def]
            """Return function unchanged as numba fallback."""
            return func

        return decorator


@njit(cache=True)
def garch_recursion_numba(
    resids: NDArray[np.float64],
    sigma2: NDArray[np.float64],
    omega: float,
    alphas: NDArray[np.float64],
    betas: NDArray[np.float64],
    p: int,
    q: int,
    backcast: float,
) -> NDArray[np.float64]:
    """GARCH variance recursion loop.

    Computes: sigma2_t = omega + sum_i(alpha_i * eps_{t-i}^2) + sum_j(beta_j * sigma2_{t-j})

    Parameters
    ----------
    resids : ndarray
        Residuals array, shape (T,).
    sigma2 : ndarray
        Output variance array, shape (T,). sigma2[0] should be set to backcast.
    omega : float
        Constant term.
    alphas : ndarray
        ARCH coefficients, shape (q,).
    betas : ndarray
        GARCH coefficients, shape (p,).
    p : int
        Number of GARCH lags.
    q : int
        Number of ARCH lags.
    backcast : float
        Initial variance value.

    Returns
    -------
    ndarray
        Conditional variance series, shape (T,).
    """
    nobs = len(resids)
    sigma2[0] = backcast
    for t in range(1, nobs):
        sigma2[t] = omega
        for i in range(q):
            if t - i - 1 >= 0:
                sigma2[t] += alphas[i] * resids[t - i - 1] ** 2
            else:
                sigma2[t] += alphas[i] * backcast
        for j in range(p):
            if t - j - 1 >= 0:
                sigma2[t] += betas[j] * sigma2[t - j - 1]
            else:
                sigma2[t] += betas[j] * backcast
    return sigma2


@njit(cache=True)
def egarch_recursion_numba(
    resids: NDArray[np.float64],
    log_sigma2: NDArray[np.float64],
    omega: float,
    alpha: float,
    gamma: float,
    beta: float,
    backcast: float,
) -> NDArray[np.float64]:
    """EGARCH recursion in log-space.

    Computes: log(sigma2_t) = omega + alpha*(|z_{t-1}| - E|z|) + gamma*z_{t-1}
              + beta*log(sigma2_{t-1})

    Parameters
    ----------
    resids : ndarray
        Residuals array, shape (T,).
    log_sigma2 : ndarray
        Output log-variance array, shape (T,).
    omega : float
        Constant term.
    alpha : float
        ARCH coefficient.
    gamma : float
        Leverage coefficient.
    beta : float
        GARCH coefficient.
    backcast : float
        Initial log-variance value.

    Returns
    -------
    ndarray
        Log-conditional variance series, shape (T,).
    """
    nobs = len(resids)
    e_abs_z = np.sqrt(2.0 / np.pi)  # E[|z|] for standard normal
    log_sigma2[0] = backcast

    for t in range(1, nobs):
        sigma_prev = np.exp(log_sigma2[t - 1] / 2.0)
        z = resids[t - 1] / max(sigma_prev, 1e-12)
        log_sigma2[t] = omega + alpha * (np.abs(z) - e_abs_z) + gamma * z + beta * log_sigma2[t - 1]
    return log_sigma2


@njit(cache=True)
def hamilton_filter_numba(
    regime_ll: NDArray[np.float64],
    transition_matrix: NDArray[np.float64],
    init_probs: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Hamilton filter loop for regime-switching models.

    Parameters
    ----------
    regime_ll : ndarray
        Per-regime log-likelihoods, shape (T, k).
    transition_matrix : ndarray
        Transition probability matrix, shape (k, k).
    init_probs : ndarray
        Initial regime probabilities, shape (k,).

    Returns
    -------
    tuple[ndarray, ndarray, ndarray]
        (filtered_probs, predicted_probs, marginal_ll):
        - filtered_probs: shape (T, k)
        - predicted_probs: shape (T, k)
        - marginal_ll: shape (T,)
    """
    nobs, k = regime_ll.shape
    filtered = np.empty((nobs, k))
    predicted = np.empty((nobs, k))
    marginal_ll = np.empty(nobs)

    # First observation
    predicted[0, :] = init_probs
    for j in range(k):
        filtered[0, j] = predicted[0, j] * np.exp(regime_ll[0, j])
    marginal_ll[0] = 0.0
    total = 0.0
    for j in range(k):
        total += filtered[0, j]
    if total > 0:
        marginal_ll[0] = np.log(total)
        for j in range(k):
            filtered[0, j] /= total
    else:
        for j in range(k):
            filtered[0, j] = 1.0 / k

    # Forward pass
    for t in range(1, nobs):
        # Prediction
        for j in range(k):
            predicted[t, j] = 0.0
            for i in range(k):
                predicted[t, j] += transition_matrix[i, j] * filtered[t - 1, i]

        # Update
        total = 0.0
        for j in range(k):
            filtered[t, j] = predicted[t, j] * np.exp(regime_ll[t, j])
            total += filtered[t, j]

        if total > 0:
            marginal_ll[t] = np.log(total)
            for j in range(k):
                filtered[t, j] /= total
        else:
            marginal_ll[t] = -1e10
            for j in range(k):
                filtered[t, j] = 1.0 / k

    return filtered, predicted, marginal_ll


@njit(cache=True)
def dcc_recursion_numba(
    std_resids: NDArray[np.float64],
    q_bar: NDArray[np.float64],
    a: float,
    b: float,
) -> NDArray[np.float64]:
    """DCC Q_t recursion.

    Computes: Q_t = (1 - a - b) * Q_bar + a * (z_{t-1} * z_{t-1}') + b * Q_{t-1}

    Parameters
    ----------
    std_resids : ndarray
        Standardized residuals, shape (T, k).
    q_bar : ndarray
        Unconditional correlation matrix, shape (k, k).
    a : float
        DCC alpha parameter.
    b : float
        DCC beta parameter.

    Returns
    -------
    ndarray
        Dynamic Q matrices, shape (T, k, k).
    """
    nobs, k = std_resids.shape
    q_mat = np.empty((nobs, k, k))
    intercept = 1.0 - a - b

    # Initialize q_mat[0] = q_bar
    for i in range(k):
        for j in range(k):
            q_mat[0, i, j] = q_bar[i, j]

    for t in range(1, nobs):
        for i in range(k):
            for j in range(k):
                q_mat[t, i, j] = (
                    intercept * q_bar[i, j]
                    + a * std_resids[t - 1, i] * std_resids[t - 1, j]
                    + b * q_mat[t - 1, i, j]
                )

    return q_mat


# --- Pure Python fallbacks ---


def garch_recursion_python(
    resids: NDArray[np.float64],
    sigma2: NDArray[np.float64],
    omega: float,
    alphas: NDArray[np.float64],
    betas: NDArray[np.float64],
    p: int,
    q: int,
    backcast: float,
) -> NDArray[np.float64]:
    """Pure Python GARCH variance recursion (fallback)."""
    nobs = len(resids)
    sigma2[0] = backcast
    for t in range(1, nobs):
        sigma2[t] = omega
        for i in range(q):
            if t - i - 1 >= 0:
                sigma2[t] += alphas[i] * resids[t - i - 1] ** 2
            else:
                sigma2[t] += alphas[i] * backcast
        for j in range(p):
            if t - j - 1 >= 0:
                sigma2[t] += betas[j] * sigma2[t - j - 1]
            else:
                sigma2[t] += betas[j] * backcast
    return sigma2


def egarch_recursion_python(
    resids: NDArray[np.float64],
    log_sigma2: NDArray[np.float64],
    omega: float,
    alpha: float,
    gamma: float,
    beta: float,
    backcast: float,
) -> NDArray[np.float64]:
    """Pure Python EGARCH recursion (fallback)."""
    nobs = len(resids)
    e_abs_z = np.sqrt(2.0 / np.pi)
    log_sigma2[0] = backcast
    for t in range(1, nobs):
        sigma_prev = np.exp(log_sigma2[t - 1] / 2.0)
        z = resids[t - 1] / max(sigma_prev, 1e-12)
        log_sigma2[t] = omega + alpha * (np.abs(z) - e_abs_z) + gamma * z + beta * log_sigma2[t - 1]
    return log_sigma2
