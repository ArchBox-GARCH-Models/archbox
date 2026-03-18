"""Portfolio utilities for multivariate GARCH models.

Provides portfolio variance, minimum variance weights, and risk decomposition.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def portfolio_variance(
    weights: NDArray[np.float64],
    h_t: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute portfolio variance w' H_t w for all t.

    Parameters
    ----------
    weights : ndarray
        Portfolio weights (k,).
    h_t : ndarray
        Dynamic covariance matrices (T, k, k).

    Returns
    -------
    ndarray
        Portfolio variance series (T,).
    """
    w = np.asarray(weights, dtype=np.float64)
    nobs = h_t.shape[0]
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def portfolio_volatility(
    weights: NDArray[np.float64],
    h_t: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute portfolio volatility (std dev) for all t.

    Parameters
    ----------
    weights : ndarray
        Portfolio weights (k,).
    h_t : ndarray
        Dynamic covariance matrices (T, k, k).

    Returns
    -------
    ndarray
        Portfolio volatility series (T,).
    """
    var = portfolio_variance(weights, h_t)
    return np.sqrt(np.maximum(var, 0.0))


def minimum_variance_weights(
    h: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute minimum variance portfolio weights for a single H matrix.

    w* = H^{-1} * 1 / (1' * H^{-1} * 1)

    Parameters
    ----------
    h : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Minimum variance portfolio weights (k,). Sums to 1.
    """
    k = h.shape[0]
    ones = np.ones(k)
    try:
        h_inv = np.linalg.inv(h)
    except np.linalg.LinAlgError:
        h_reg = h + np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def minimum_variance_weights_dynamic(
    h_t: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute time-varying minimum variance portfolio weights.

    Parameters
    ----------
    h_t : ndarray
        Dynamic covariance matrices (T, k, k).

    Returns
    -------
    ndarray
        Time-varying weights (T, k). Each row sums to 1.
    """
    nobs, k, _ = h_t.shape
    weights = np.zeros((nobs, k))
    for t in range(nobs):
        weights[t] = minimum_variance_weights(h_t[t])
    return weights


def marginal_risk_contribution(
    weights: NDArray[np.float64],
    h: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute marginal contribution to risk for each asset.

    MC_i = (H * w)_i / sigma_p

    Parameters
    ----------
    weights : ndarray
        Portfolio weights (k,).
    h : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Marginal risk contributions (k,).
    """
    w = np.asarray(weights, dtype=np.float64)
    sigma_p = np.sqrt(float(w @ h @ w))
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def risk_contribution(
    weights: NDArray[np.float64],
    h: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute total risk contribution for each asset.

    RC_i = w_i * MC_i

    Property: sum(RC_i) = sigma_p (Euler decomposition).

    Parameters
    ----------
    weights : ndarray
        Portfolio weights (k,).
    h : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Risk contributions (k,). Sums to sigma_p.
    """
    w = np.asarray(weights, dtype=np.float64)
    mc = marginal_risk_contribution(w, h)
    return w * mc


def risk_decomposition(
    weights: NDArray[np.float64],
    h: NDArray[np.float64],
) -> dict[str, NDArray[np.float64]]:
    """Full risk decomposition for a portfolio.

    Parameters
    ----------
    weights : ndarray
        Portfolio weights (k,).
    h : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    dict
        Dictionary with:
        - 'weights': portfolio weights (k,)
        - 'portfolio_volatility': scalar
        - 'marginal_contribution': MC_i (k,)
        - 'risk_contribution': RC_i (k,)
        - 'pct_contribution': RC_i / sigma_p (k,), sums to 1
    """
    w = np.asarray(weights, dtype=np.float64)
    sigma_p = np.sqrt(float(w @ h @ w))
    mc = marginal_risk_contribution(w, h)
    rc = w * mc

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }
