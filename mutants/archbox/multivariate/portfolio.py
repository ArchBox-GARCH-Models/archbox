"""Portfolio utilities for multivariate GARCH models.

Provides portfolio variance, minimum variance weights, and risk decomposition.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, ClassVar

import numpy as np
from numpy.typing import NDArray

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


def portfolio_variance(
    weights: NDArray[np.float64],
    h_t: NDArray[np.float64],
) -> NDArray[np.float64]:
    args = [weights, h_t]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_portfolio_variance__mutmut_orig, x_portfolio_variance__mutmut_mutants, args, kwargs, None
    )


def x_portfolio_variance__mutmut_orig(
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


def x_portfolio_variance__mutmut_1(
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
    w = None
    nobs = h_t.shape[0]
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_2(
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
    w = np.asarray(None, dtype=np.float64)
    nobs = h_t.shape[0]
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_3(
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
    w = np.asarray(weights, dtype=None)
    nobs = h_t.shape[0]
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_4(
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
    w = np.asarray(dtype=np.float64)
    nobs = h_t.shape[0]
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_5(
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
    w = np.asarray(
        weights,
    )
    nobs = h_t.shape[0]
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_6(
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
    nobs = None
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_7(
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
    nobs = h_t.shape[1]
    port_var = np.zeros(nobs)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_8(
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
    port_var = None
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_9(
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
    port_var = np.zeros(None)
    for t in range(nobs):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_10(
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
    for t in range(None):
        port_var[t] = float(w @ h_t[t] @ w)
    return port_var


def x_portfolio_variance__mutmut_11(
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
        port_var[t] = None
    return port_var


def x_portfolio_variance__mutmut_12(
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
        port_var[t] = float(None)
    return port_var


x_portfolio_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_portfolio_variance__mutmut_1": x_portfolio_variance__mutmut_1,
    "x_portfolio_variance__mutmut_2": x_portfolio_variance__mutmut_2,
    "x_portfolio_variance__mutmut_3": x_portfolio_variance__mutmut_3,
    "x_portfolio_variance__mutmut_4": x_portfolio_variance__mutmut_4,
    "x_portfolio_variance__mutmut_5": x_portfolio_variance__mutmut_5,
    "x_portfolio_variance__mutmut_6": x_portfolio_variance__mutmut_6,
    "x_portfolio_variance__mutmut_7": x_portfolio_variance__mutmut_7,
    "x_portfolio_variance__mutmut_8": x_portfolio_variance__mutmut_8,
    "x_portfolio_variance__mutmut_9": x_portfolio_variance__mutmut_9,
    "x_portfolio_variance__mutmut_10": x_portfolio_variance__mutmut_10,
    "x_portfolio_variance__mutmut_11": x_portfolio_variance__mutmut_11,
    "x_portfolio_variance__mutmut_12": x_portfolio_variance__mutmut_12,
}
x_portfolio_variance__mutmut_orig.__name__ = "x_portfolio_variance"


def portfolio_volatility(
    weights: NDArray[np.float64],
    h_t: NDArray[np.float64],
) -> NDArray[np.float64]:
    args = [weights, h_t]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_portfolio_volatility__mutmut_orig,
        x_portfolio_volatility__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_portfolio_volatility__mutmut_orig(
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


def x_portfolio_volatility__mutmut_1(
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
    var = None
    return np.sqrt(np.maximum(var, 0.0))


def x_portfolio_volatility__mutmut_2(
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
    var = portfolio_variance(None, h_t)
    return np.sqrt(np.maximum(var, 0.0))


def x_portfolio_volatility__mutmut_3(
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
    var = portfolio_variance(weights, None)
    return np.sqrt(np.maximum(var, 0.0))


def x_portfolio_volatility__mutmut_4(
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
    var = portfolio_variance(h_t)
    return np.sqrt(np.maximum(var, 0.0))


def x_portfolio_volatility__mutmut_5(
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
    var = portfolio_variance(
        weights,
    )
    return np.sqrt(np.maximum(var, 0.0))


def x_portfolio_volatility__mutmut_6(
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
    return np.sqrt(None)


def x_portfolio_volatility__mutmut_7(
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
    return np.sqrt(np.maximum(None, 0.0))


def x_portfolio_volatility__mutmut_8(
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
    return np.sqrt(np.maximum(var, None))


def x_portfolio_volatility__mutmut_9(
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
    return np.sqrt(np.maximum(0.0))


def x_portfolio_volatility__mutmut_10(
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
    return np.sqrt(
        np.maximum(
            var,
        )
    )


def x_portfolio_volatility__mutmut_11(
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
    return np.sqrt(np.maximum(var, 1.0))


x_portfolio_volatility__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_portfolio_volatility__mutmut_1": x_portfolio_volatility__mutmut_1,
    "x_portfolio_volatility__mutmut_2": x_portfolio_volatility__mutmut_2,
    "x_portfolio_volatility__mutmut_3": x_portfolio_volatility__mutmut_3,
    "x_portfolio_volatility__mutmut_4": x_portfolio_volatility__mutmut_4,
    "x_portfolio_volatility__mutmut_5": x_portfolio_volatility__mutmut_5,
    "x_portfolio_volatility__mutmut_6": x_portfolio_volatility__mutmut_6,
    "x_portfolio_volatility__mutmut_7": x_portfolio_volatility__mutmut_7,
    "x_portfolio_volatility__mutmut_8": x_portfolio_volatility__mutmut_8,
    "x_portfolio_volatility__mutmut_9": x_portfolio_volatility__mutmut_9,
    "x_portfolio_volatility__mutmut_10": x_portfolio_volatility__mutmut_10,
    "x_portfolio_volatility__mutmut_11": x_portfolio_volatility__mutmut_11,
}
x_portfolio_volatility__mutmut_orig.__name__ = "x_portfolio_volatility"


def minimum_variance_weights(
    h: NDArray[np.float64],
) -> NDArray[np.float64]:
    args = [h]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_minimum_variance_weights__mutmut_orig,
        x_minimum_variance_weights__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_minimum_variance_weights__mutmut_orig(
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


def x_minimum_variance_weights__mutmut_1(
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
    k = None
    ones = np.ones(k)
    try:
        h_inv = np.linalg.inv(h)
    except np.linalg.LinAlgError:
        h_reg = h + np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_2(
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
    k = h.shape[1]
    ones = np.ones(k)
    try:
        h_inv = np.linalg.inv(h)
    except np.linalg.LinAlgError:
        h_reg = h + np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_3(
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
    ones = None
    try:
        h_inv = np.linalg.inv(h)
    except np.linalg.LinAlgError:
        h_reg = h + np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_4(
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
    ones = np.ones(None)
    try:
        h_inv = np.linalg.inv(h)
    except np.linalg.LinAlgError:
        h_reg = h + np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_5(
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
        h_inv = None
    except np.linalg.LinAlgError:
        h_reg = h + np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_6(
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
        h_inv = np.linalg.inv(None)
    except np.linalg.LinAlgError:
        h_reg = h + np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_7(
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
        h_reg = None
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_8(
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
        h_reg = h - np.eye(k) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_9(
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
        h_reg = h + np.eye(k) / 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_10(
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
        h_reg = h + np.eye(None) * 1e-8
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_11(
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
        h_reg = h + np.eye(k) * 1.00000001
        h_inv = np.linalg.inv(h_reg)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_12(
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
        h_inv = None

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_13(
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
        h_inv = np.linalg.inv(None)

    w = h_inv @ ones
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_14(
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

    w = None
    w = w / np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_15(
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
    w = None
    return w


def x_minimum_variance_weights__mutmut_16(
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
    w = w * np.sum(w)
    return w


def x_minimum_variance_weights__mutmut_17(
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
    w = w / np.sum(None)
    return w


x_minimum_variance_weights__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_minimum_variance_weights__mutmut_1": x_minimum_variance_weights__mutmut_1,
    "x_minimum_variance_weights__mutmut_2": x_minimum_variance_weights__mutmut_2,
    "x_minimum_variance_weights__mutmut_3": x_minimum_variance_weights__mutmut_3,
    "x_minimum_variance_weights__mutmut_4": x_minimum_variance_weights__mutmut_4,
    "x_minimum_variance_weights__mutmut_5": x_minimum_variance_weights__mutmut_5,
    "x_minimum_variance_weights__mutmut_6": x_minimum_variance_weights__mutmut_6,
    "x_minimum_variance_weights__mutmut_7": x_minimum_variance_weights__mutmut_7,
    "x_minimum_variance_weights__mutmut_8": x_minimum_variance_weights__mutmut_8,
    "x_minimum_variance_weights__mutmut_9": x_minimum_variance_weights__mutmut_9,
    "x_minimum_variance_weights__mutmut_10": x_minimum_variance_weights__mutmut_10,
    "x_minimum_variance_weights__mutmut_11": x_minimum_variance_weights__mutmut_11,
    "x_minimum_variance_weights__mutmut_12": x_minimum_variance_weights__mutmut_12,
    "x_minimum_variance_weights__mutmut_13": x_minimum_variance_weights__mutmut_13,
    "x_minimum_variance_weights__mutmut_14": x_minimum_variance_weights__mutmut_14,
    "x_minimum_variance_weights__mutmut_15": x_minimum_variance_weights__mutmut_15,
    "x_minimum_variance_weights__mutmut_16": x_minimum_variance_weights__mutmut_16,
    "x_minimum_variance_weights__mutmut_17": x_minimum_variance_weights__mutmut_17,
}
x_minimum_variance_weights__mutmut_orig.__name__ = "x_minimum_variance_weights"


def minimum_variance_weights_dynamic(
    h_t: NDArray[np.float64],
) -> NDArray[np.float64]:
    args = [h_t]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_minimum_variance_weights_dynamic__mutmut_orig,
        x_minimum_variance_weights_dynamic__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_minimum_variance_weights_dynamic__mutmut_orig(
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


def x_minimum_variance_weights_dynamic__mutmut_1(
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
    nobs, k, _ = None
    weights = np.zeros((nobs, k))
    for t in range(nobs):
        weights[t] = minimum_variance_weights(h_t[t])
    return weights


def x_minimum_variance_weights_dynamic__mutmut_2(
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
    weights = None
    for t in range(nobs):
        weights[t] = minimum_variance_weights(h_t[t])
    return weights


def x_minimum_variance_weights_dynamic__mutmut_3(
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
    weights = np.zeros(None)
    for t in range(nobs):
        weights[t] = minimum_variance_weights(h_t[t])
    return weights


def x_minimum_variance_weights_dynamic__mutmut_4(
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
    for t in range(None):
        weights[t] = minimum_variance_weights(h_t[t])
    return weights


def x_minimum_variance_weights_dynamic__mutmut_5(
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
        weights[t] = None
    return weights


def x_minimum_variance_weights_dynamic__mutmut_6(
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
        weights[t] = minimum_variance_weights(None)
    return weights


x_minimum_variance_weights_dynamic__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_minimum_variance_weights_dynamic__mutmut_1": x_minimum_variance_weights_dynamic__mutmut_1,
    "x_minimum_variance_weights_dynamic__mutmut_2": x_minimum_variance_weights_dynamic__mutmut_2,
    "x_minimum_variance_weights_dynamic__mutmut_3": x_minimum_variance_weights_dynamic__mutmut_3,
    "x_minimum_variance_weights_dynamic__mutmut_4": x_minimum_variance_weights_dynamic__mutmut_4,
    "x_minimum_variance_weights_dynamic__mutmut_5": x_minimum_variance_weights_dynamic__mutmut_5,
    "x_minimum_variance_weights_dynamic__mutmut_6": x_minimum_variance_weights_dynamic__mutmut_6,
}
x_minimum_variance_weights_dynamic__mutmut_orig.__name__ = "x_minimum_variance_weights_dynamic"


def marginal_risk_contribution(
    weights: NDArray[np.float64],
    h: NDArray[np.float64],
) -> NDArray[np.float64]:
    args = [weights, h]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_marginal_risk_contribution__mutmut_orig,
        x_marginal_risk_contribution__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_marginal_risk_contribution__mutmut_orig(
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


def x_marginal_risk_contribution__mutmut_1(
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
    w = None
    sigma_p = np.sqrt(float(w @ h @ w))
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_2(
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
    w = np.asarray(None, dtype=np.float64)
    sigma_p = np.sqrt(float(w @ h @ w))
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_3(
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
    w = np.asarray(weights, dtype=None)
    sigma_p = np.sqrt(float(w @ h @ w))
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_4(
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
    w = np.asarray(dtype=np.float64)
    sigma_p = np.sqrt(float(w @ h @ w))
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_5(
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
    w = np.asarray(
        weights,
    )
    sigma_p = np.sqrt(float(w @ h @ w))
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_6(
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
    sigma_p = None
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_7(
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
    sigma_p = np.sqrt(None)
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_8(
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
    sigma_p = np.sqrt(float(None))
    if sigma_p < 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_9(
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
    if sigma_p <= 1e-12:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_10(
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
    if sigma_p < 1.000000000001:
        return np.zeros_like(w)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_11(
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
        return np.zeros_like(None)
    hw = h @ w
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_12(
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
    hw = None
    return hw / sigma_p


def x_marginal_risk_contribution__mutmut_13(
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
    return hw * sigma_p


x_marginal_risk_contribution__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_marginal_risk_contribution__mutmut_1": x_marginal_risk_contribution__mutmut_1,
    "x_marginal_risk_contribution__mutmut_2": x_marginal_risk_contribution__mutmut_2,
    "x_marginal_risk_contribution__mutmut_3": x_marginal_risk_contribution__mutmut_3,
    "x_marginal_risk_contribution__mutmut_4": x_marginal_risk_contribution__mutmut_4,
    "x_marginal_risk_contribution__mutmut_5": x_marginal_risk_contribution__mutmut_5,
    "x_marginal_risk_contribution__mutmut_6": x_marginal_risk_contribution__mutmut_6,
    "x_marginal_risk_contribution__mutmut_7": x_marginal_risk_contribution__mutmut_7,
    "x_marginal_risk_contribution__mutmut_8": x_marginal_risk_contribution__mutmut_8,
    "x_marginal_risk_contribution__mutmut_9": x_marginal_risk_contribution__mutmut_9,
    "x_marginal_risk_contribution__mutmut_10": x_marginal_risk_contribution__mutmut_10,
    "x_marginal_risk_contribution__mutmut_11": x_marginal_risk_contribution__mutmut_11,
    "x_marginal_risk_contribution__mutmut_12": x_marginal_risk_contribution__mutmut_12,
    "x_marginal_risk_contribution__mutmut_13": x_marginal_risk_contribution__mutmut_13,
}
x_marginal_risk_contribution__mutmut_orig.__name__ = "x_marginal_risk_contribution"


def risk_contribution(
    weights: NDArray[np.float64],
    h: NDArray[np.float64],
) -> NDArray[np.float64]:
    args = [weights, h]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_risk_contribution__mutmut_orig, x_risk_contribution__mutmut_mutants, args, kwargs, None
    )


def x_risk_contribution__mutmut_orig(
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


def x_risk_contribution__mutmut_1(
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
    w = None
    mc = marginal_risk_contribution(w, h)
    return w * mc


def x_risk_contribution__mutmut_2(
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
    w = np.asarray(None, dtype=np.float64)
    mc = marginal_risk_contribution(w, h)
    return w * mc


def x_risk_contribution__mutmut_3(
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
    w = np.asarray(weights, dtype=None)
    mc = marginal_risk_contribution(w, h)
    return w * mc


def x_risk_contribution__mutmut_4(
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
    w = np.asarray(dtype=np.float64)
    mc = marginal_risk_contribution(w, h)
    return w * mc


def x_risk_contribution__mutmut_5(
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
    w = np.asarray(
        weights,
    )
    mc = marginal_risk_contribution(w, h)
    return w * mc


def x_risk_contribution__mutmut_6(
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
    mc = None
    return w * mc


def x_risk_contribution__mutmut_7(
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
    mc = marginal_risk_contribution(None, h)
    return w * mc


def x_risk_contribution__mutmut_8(
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
    mc = marginal_risk_contribution(w, None)
    return w * mc


def x_risk_contribution__mutmut_9(
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
    mc = marginal_risk_contribution(h)
    return w * mc


def x_risk_contribution__mutmut_10(
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
    mc = marginal_risk_contribution(
        w,
    )
    return w * mc


def x_risk_contribution__mutmut_11(
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
    return w / mc


x_risk_contribution__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_risk_contribution__mutmut_1": x_risk_contribution__mutmut_1,
    "x_risk_contribution__mutmut_2": x_risk_contribution__mutmut_2,
    "x_risk_contribution__mutmut_3": x_risk_contribution__mutmut_3,
    "x_risk_contribution__mutmut_4": x_risk_contribution__mutmut_4,
    "x_risk_contribution__mutmut_5": x_risk_contribution__mutmut_5,
    "x_risk_contribution__mutmut_6": x_risk_contribution__mutmut_6,
    "x_risk_contribution__mutmut_7": x_risk_contribution__mutmut_7,
    "x_risk_contribution__mutmut_8": x_risk_contribution__mutmut_8,
    "x_risk_contribution__mutmut_9": x_risk_contribution__mutmut_9,
    "x_risk_contribution__mutmut_10": x_risk_contribution__mutmut_10,
    "x_risk_contribution__mutmut_11": x_risk_contribution__mutmut_11,
}
x_risk_contribution__mutmut_orig.__name__ = "x_risk_contribution"


def risk_decomposition(
    weights: NDArray[np.float64],
    h: NDArray[np.float64],
) -> dict[str, NDArray[np.float64]]:
    args = [weights, h]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_risk_decomposition__mutmut_orig, x_risk_decomposition__mutmut_mutants, args, kwargs, None
    )


def x_risk_decomposition__mutmut_orig(
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


def x_risk_decomposition__mutmut_1(
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
    w = None
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


def x_risk_decomposition__mutmut_2(
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
    w = np.asarray(None, dtype=np.float64)
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


def x_risk_decomposition__mutmut_3(
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
    w = np.asarray(weights, dtype=None)
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


def x_risk_decomposition__mutmut_4(
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
    w = np.asarray(dtype=np.float64)
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


def x_risk_decomposition__mutmut_5(
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
    w = np.asarray(
        weights,
    )
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


def x_risk_decomposition__mutmut_6(
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
    sigma_p = None
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


def x_risk_decomposition__mutmut_7(
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
    sigma_p = np.sqrt(None)
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


def x_risk_decomposition__mutmut_8(
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
    sigma_p = np.sqrt(float(None))
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


def x_risk_decomposition__mutmut_9(
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
    mc = None
    rc = w * mc

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_10(
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
    mc = marginal_risk_contribution(None, h)
    rc = w * mc

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_11(
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
    mc = marginal_risk_contribution(w, None)
    rc = w * mc

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_12(
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
    mc = marginal_risk_contribution(h)
    rc = w * mc

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_13(
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
    mc = marginal_risk_contribution(
        w,
    )
    rc = w * mc

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_14(
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
    rc = None

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_15(
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
    rc = w / mc

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_16(
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

    pct = None

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_17(
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

    pct = rc * sigma_p if sigma_p > 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_18(
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

    pct = rc / sigma_p if sigma_p >= 1e-12 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_19(
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

    pct = rc / sigma_p if sigma_p > 1.000000000001 else np.zeros_like(w)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_20(
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

    pct = rc / sigma_p if sigma_p > 1e-12 else np.zeros_like(None)

    return {
        "weights": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_21(
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
        "XXweightsXX": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_22(
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
        "WEIGHTS": w,
        "portfolio_volatility": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_23(
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
        "XXportfolio_volatilityXX": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_24(
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
        "PORTFOLIO_VOLATILITY": np.array([sigma_p]),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_25(
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
        "portfolio_volatility": np.array(None),
        "marginal_contribution": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_26(
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
        "XXmarginal_contributionXX": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_27(
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
        "MARGINAL_CONTRIBUTION": mc,
        "risk_contribution": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_28(
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
        "XXrisk_contributionXX": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_29(
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
        "RISK_CONTRIBUTION": rc,
        "pct_contribution": pct,
    }


def x_risk_decomposition__mutmut_30(
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
        "XXpct_contributionXX": pct,
    }


def x_risk_decomposition__mutmut_31(
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
        "PCT_CONTRIBUTION": pct,
    }


x_risk_decomposition__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_risk_decomposition__mutmut_1": x_risk_decomposition__mutmut_1,
    "x_risk_decomposition__mutmut_2": x_risk_decomposition__mutmut_2,
    "x_risk_decomposition__mutmut_3": x_risk_decomposition__mutmut_3,
    "x_risk_decomposition__mutmut_4": x_risk_decomposition__mutmut_4,
    "x_risk_decomposition__mutmut_5": x_risk_decomposition__mutmut_5,
    "x_risk_decomposition__mutmut_6": x_risk_decomposition__mutmut_6,
    "x_risk_decomposition__mutmut_7": x_risk_decomposition__mutmut_7,
    "x_risk_decomposition__mutmut_8": x_risk_decomposition__mutmut_8,
    "x_risk_decomposition__mutmut_9": x_risk_decomposition__mutmut_9,
    "x_risk_decomposition__mutmut_10": x_risk_decomposition__mutmut_10,
    "x_risk_decomposition__mutmut_11": x_risk_decomposition__mutmut_11,
    "x_risk_decomposition__mutmut_12": x_risk_decomposition__mutmut_12,
    "x_risk_decomposition__mutmut_13": x_risk_decomposition__mutmut_13,
    "x_risk_decomposition__mutmut_14": x_risk_decomposition__mutmut_14,
    "x_risk_decomposition__mutmut_15": x_risk_decomposition__mutmut_15,
    "x_risk_decomposition__mutmut_16": x_risk_decomposition__mutmut_16,
    "x_risk_decomposition__mutmut_17": x_risk_decomposition__mutmut_17,
    "x_risk_decomposition__mutmut_18": x_risk_decomposition__mutmut_18,
    "x_risk_decomposition__mutmut_19": x_risk_decomposition__mutmut_19,
    "x_risk_decomposition__mutmut_20": x_risk_decomposition__mutmut_20,
    "x_risk_decomposition__mutmut_21": x_risk_decomposition__mutmut_21,
    "x_risk_decomposition__mutmut_22": x_risk_decomposition__mutmut_22,
    "x_risk_decomposition__mutmut_23": x_risk_decomposition__mutmut_23,
    "x_risk_decomposition__mutmut_24": x_risk_decomposition__mutmut_24,
    "x_risk_decomposition__mutmut_25": x_risk_decomposition__mutmut_25,
    "x_risk_decomposition__mutmut_26": x_risk_decomposition__mutmut_26,
    "x_risk_decomposition__mutmut_27": x_risk_decomposition__mutmut_27,
    "x_risk_decomposition__mutmut_28": x_risk_decomposition__mutmut_28,
    "x_risk_decomposition__mutmut_29": x_risk_decomposition__mutmut_29,
    "x_risk_decomposition__mutmut_30": x_risk_decomposition__mutmut_30,
    "x_risk_decomposition__mutmut_31": x_risk_decomposition__mutmut_31,
}
x_risk_decomposition__mutmut_orig.__name__ = "x_risk_decomposition"
