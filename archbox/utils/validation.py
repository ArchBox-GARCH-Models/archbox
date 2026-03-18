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


def validate_positive_integer(val: int, name: str) -> int:
    """Validate that val is a positive integer.

    Parameters
    ----------
    val : int
        Value to validate.
    name : str
        Parameter name for error message.

    Returns
    -------
    int
        Validated value.
    """
    if not isinstance(val, int) or val < 1:
        msg = f"{name} must be a positive integer, got {val}"
        raise ValueError(msg)
    return val


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
