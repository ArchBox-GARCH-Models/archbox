"""Input validation utilities for archbox."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def validate_returns(y: object) -> NDArray[np.float64]:
    """Validate and convert returns to numpy array.

    Parameters
    ----------
    y : array-like
        Time series of returns.

    Returns
    -------
    NDArray[np.float64]
        Validated 1D array.

    Raises
    ------
    ValueError
        If input is invalid.
    """
    arr = np.asarray(y, dtype=np.float64)
    if arr.ndim != 1:
        msg = f"Returns must be 1D, got {arr.ndim}D"
        raise ValueError(msg)
    if len(arr) < 10:
        msg = f"Returns must have at least 10 observations, got {len(arr)}"
        raise ValueError(msg)
    if np.any(np.isnan(arr)):
        msg = "Returns contain NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def validate_positive_integer(val: object, name: str) -> int:
    """Validate that ``val`` is a positive integer.

    Accepts Python ``int`` and NumPy integer scalars (``np.integer``).
    Booleans are rejected explicitly: ``bool`` is a subclass of ``int``
    in Python, but ``True``/``False`` are never valid lag orders.

    Parameters
    ----------
    val : object
        Value to validate.
    name : str
        Parameter name used in the error message.

    Returns
    -------
    int
        Validated value as a Python ``int``.

    Raises
    ------
    ValueError
        If ``val`` is not an integer type, is a boolean, or is < 1.
    """
    if isinstance(val, bool | np.bool_) or not isinstance(val, int | np.integer):
        msg = f"{name} must be a positive integer, got {val!r} of type {type(val).__name__}"
        raise ValueError(msg)
    ival = int(val)
    if ival < 1:
        msg = f"{name} must be a positive integer, got {ival}"
        raise ValueError(msg)
    return ival


def check_stationarity(params: NDArray[np.float64], p: int, q: int) -> bool:
    """Check if GARCH parameters satisfy stationarity constraint.

    Parameters
    ----------
    params : ndarray
        Array [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p].
    p : int
        Number of GARCH lags.
    q : int
        Number of ARCH lags.

    Returns
    -------
    bool
        True if sum(alpha) + sum(beta) < 1.
    """
    alphas = params[1 : 1 + q]
    betas = params[1 + q : 1 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def validate_realized_variance(rv: object, name: str = "realized_variance") -> NDArray[np.float64]:
    """Validate and convert a realized-variance series to a numpy array.

    Realized variance is a non-negative quantity by construction, so NaN,
    Inf and negative entries indicate a corrupted input series.

    Parameters
    ----------
    rv : array-like
        Realized variance series.
    name : str
        Parameter name used in error messages.

    Returns
    -------
    NDArray[np.float64]
        Validated 1D array.

    Raises
    ------
    ValueError
        If the series is not 1D, too short, or contains NaN/Inf/negative values.
    """
    arr = np.asarray(rv, dtype=np.float64)
    if arr.ndim != 1:
        msg = f"{name} must be 1D, got {arr.ndim}D"
        raise ValueError(msg)
    if len(arr) < 10:
        msg = f"{name} must have at least 10 observations, got {len(arr)}"
        raise ValueError(msg)
    if np.any(np.isnan(arr)):
        msg = f"{name} contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = f"{name} contains Inf values"
        raise ValueError(msg)
    if np.any(arr < 0.0):
        msg = f"{name} must be non-negative, got a minimum of {float(np.min(arr))}"
        raise ValueError(msg)
    return arr
