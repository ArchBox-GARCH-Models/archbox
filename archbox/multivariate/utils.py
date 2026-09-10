"""Utility functions for multivariate GARCH models."""

from __future__ import annotations

from collections.abc import Callable

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

    Also accepts a stack of covariance matrices of shape (T, k, k), in which
    case a stack of correlation matrices is returned.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k) or stack of them (T, k, k).

    Returns
    -------
    ndarray
        Correlation matrix, same shape as ``cov``.
    """
    cov = np.asarray(cov, dtype=np.float64)
    d = np.sqrt(np.abs(np.diagonal(cov, axis1=-2, axis2=-1)))
    d_inv = np.where(d > 0, 1.0 / np.maximum(d, 1e-300), 0.0)
    corr: NDArray[np.float64] = cov * d_inv[..., :, None] * d_inv[..., None, :]
    return corr


def corr_to_cov(
    corr: NDArray[np.float64],
    volatilities: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Convert correlation matrix + volatilities to covariance matrix.

    Also accepts stacks: ``corr`` of shape (T, k, k) with ``volatilities`` of
    shape (T, k).

    Parameters
    ----------
    corr : ndarray
        Correlation matrix (k, k) or stack (T, k, k).
    volatilities : ndarray
        Standard deviations (k,) or (T, k).

    Returns
    -------
    ndarray
        Covariance matrix, same shape as ``corr``.
    """
    corr = np.asarray(corr, dtype=np.float64)
    vol = np.asarray(volatilities, dtype=np.float64)
    cov: NDArray[np.float64] = corr * vol[..., :, None] * vol[..., None, :]
    return cov


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


def numerical_hessian(
    func: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    step: float = 1e-4,
) -> NDArray[np.float64]:
    """Central-difference numerical Hessian of a scalar function.

    Parameters
    ----------
    func : callable
        Scalar objective evaluated at a parameter vector.
    x : ndarray
        Point at which to evaluate the Hessian, shape (n,).
    step : float
        Relative finite-difference step. The absolute step for coordinate ``i``
        is ``step * max(|x_i|, 1)``.

    Returns
    -------
    ndarray
        Symmetric (n, n) Hessian. Entries that could not be evaluated (the
        objective returned a non-finite value) are ``nan``.
    """
    x = np.asarray(x, dtype=np.float64)
    n = x.size
    hess = np.full((n, n), np.nan)
    if n == 0:
        return hess

    h = step * np.maximum(np.abs(x), 1.0)
    f0 = float(func(x))
    if not np.isfinite(f0):
        return hess

    for i in range(n):
        for j in range(i, n):
            xpp = x.copy()
            xpm = x.copy()
            xmp = x.copy()
            xmm = x.copy()
            xpp[i] += h[i]
            xpp[j] += h[j]
            xpm[i] += h[i]
            xpm[j] -= h[j]
            xmp[i] -= h[i]
            xmp[j] += h[j]
            xmm[i] -= h[i]
            xmm[j] -= h[j]
            fpp, fpm, fmp, fmm = (
                float(func(xpp)),
                float(func(xpm)),
                float(func(xmp)),
                float(func(xmm)),
            )
            if not all(np.isfinite(v) for v in (fpp, fpm, fmp, fmm)):
                continue
            value = (fpp - fpm - fmp + fmm) / (4.0 * h[i] * h[j])
            hess[i, j] = value
            hess[j, i] = value

    return hess


def standard_errors_from_hessian(
    hessian: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Standard errors from the Hessian of a *negative* log-likelihood.

    Parameters
    ----------
    hessian : ndarray
        Hessian (n, n) of the negative log-likelihood at the optimum.

    Returns
    -------
    ndarray
        Standard errors (n,). All ``nan`` when the Hessian is not finite, not
        positive definite, or cannot be inverted.
    """
    hessian = np.asarray(hessian, dtype=np.float64)
    n = hessian.shape[0] if hessian.ndim == 2 else 0
    nan_se = np.full(n, np.nan)
    if n == 0 or not np.all(np.isfinite(hessian)):
        return nan_se
    sym = 0.5 * (hessian + hessian.T)
    if not is_positive_definite(sym):
        return nan_se
    try:
        cov = np.linalg.inv(sym)
    except np.linalg.LinAlgError:
        return nan_se
    diag = np.diag(cov)
    if np.any(diag <= 0) or not np.all(np.isfinite(diag)):
        return nan_se
    return np.sqrt(diag)
