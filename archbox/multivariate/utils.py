"""Utility functions for multivariate GARCH models."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def ensure_positive_definite(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(eigenvalues, epsilon)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def is_positive_definite(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        return bool(np.all(eigenvalues > 0))
    except np.linalg.LinAlgError:
        return False


def cov_to_corr(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def corr_to_cov(
    corr: NDArray[np.float64],
    volatilities: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Convert correlation matrix + volatilities to covariance matrix.

    Parameters
    ----------
    corr : ndarray
        Correlation matrix (k, k).
    volatilities : ndarray
        Standard deviations (k,).

    Returns
    -------
    ndarray
        Covariance matrix (k, k).
    """
    d_mat = np.diag(volatilities)
    return d_mat @ corr @ d_mat


def validate_multivariate_returns(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)
