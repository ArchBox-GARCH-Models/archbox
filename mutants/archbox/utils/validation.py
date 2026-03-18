"""Input validation utilities for archbox."""

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


def validate_returns(y: object) -> NDArray[np.float64]:
    args = [y]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_validate_returns__mutmut_orig, x_validate_returns__mutmut_mutants, args, kwargs, None
    )


def x_validate_returns__mutmut_orig(y: object) -> NDArray[np.float64]:
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


def x_validate_returns__mutmut_1(y: object) -> NDArray[np.float64]:
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
    arr = None
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


def x_validate_returns__mutmut_2(y: object) -> NDArray[np.float64]:
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
    arr = np.asarray(None, dtype=np.float64)
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


def x_validate_returns__mutmut_3(y: object) -> NDArray[np.float64]:
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
    arr = np.asarray(y, dtype=None)
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


def x_validate_returns__mutmut_4(y: object) -> NDArray[np.float64]:
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
    arr = np.asarray(dtype=np.float64)
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


def x_validate_returns__mutmut_5(y: object) -> NDArray[np.float64]:
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
    arr = np.asarray(
        y,
    )
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


def x_validate_returns__mutmut_6(y: object) -> NDArray[np.float64]:
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
    if arr.ndim == 1:
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


def x_validate_returns__mutmut_7(y: object) -> NDArray[np.float64]:
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
    if arr.ndim != 2:
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


def x_validate_returns__mutmut_8(y: object) -> NDArray[np.float64]:
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
        msg = None
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


def x_validate_returns__mutmut_9(y: object) -> NDArray[np.float64]:
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
        raise ValueError(None)
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


def x_validate_returns__mutmut_10(y: object) -> NDArray[np.float64]:
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
    if len(arr) <= 10:
        msg = f"Returns must have at least 10 observations, got {len(arr)}"
        raise ValueError(msg)
    if np.any(np.isnan(arr)):
        msg = "Returns contain NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_11(y: object) -> NDArray[np.float64]:
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
    if len(arr) < 11:
        msg = f"Returns must have at least 10 observations, got {len(arr)}"
        raise ValueError(msg)
    if np.any(np.isnan(arr)):
        msg = "Returns contain NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_12(y: object) -> NDArray[np.float64]:
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
        msg = None
        raise ValueError(msg)
    if np.any(np.isnan(arr)):
        msg = "Returns contain NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_13(y: object) -> NDArray[np.float64]:
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
        raise ValueError(None)
    if np.any(np.isnan(arr)):
        msg = "Returns contain NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_14(y: object) -> NDArray[np.float64]:
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
    if np.any(None):
        msg = "Returns contain NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_15(y: object) -> NDArray[np.float64]:
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
    if np.any(np.isnan(None)):
        msg = "Returns contain NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_16(y: object) -> NDArray[np.float64]:
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
        msg = None
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_17(y: object) -> NDArray[np.float64]:
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
        msg = "XXReturns contain NaN valuesXX"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_18(y: object) -> NDArray[np.float64]:
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
        msg = "returns contain nan values"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_19(y: object) -> NDArray[np.float64]:
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
        msg = "RETURNS CONTAIN NAN VALUES"
        raise ValueError(msg)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_20(y: object) -> NDArray[np.float64]:
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
        raise ValueError(None)
    if np.any(np.isinf(arr)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_21(y: object) -> NDArray[np.float64]:
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
    if np.any(None):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_22(y: object) -> NDArray[np.float64]:
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
    if np.any(np.isinf(None)):
        msg = "Returns contain Inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_23(y: object) -> NDArray[np.float64]:
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
        msg = None
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_24(y: object) -> NDArray[np.float64]:
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
        msg = "XXReturns contain Inf valuesXX"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_25(y: object) -> NDArray[np.float64]:
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
        msg = "returns contain inf values"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_26(y: object) -> NDArray[np.float64]:
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
        msg = "RETURNS CONTAIN INF VALUES"
        raise ValueError(msg)
    return arr


def x_validate_returns__mutmut_27(y: object) -> NDArray[np.float64]:
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
        raise ValueError(None)
    return arr


x_validate_returns__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_validate_returns__mutmut_1": x_validate_returns__mutmut_1,
    "x_validate_returns__mutmut_2": x_validate_returns__mutmut_2,
    "x_validate_returns__mutmut_3": x_validate_returns__mutmut_3,
    "x_validate_returns__mutmut_4": x_validate_returns__mutmut_4,
    "x_validate_returns__mutmut_5": x_validate_returns__mutmut_5,
    "x_validate_returns__mutmut_6": x_validate_returns__mutmut_6,
    "x_validate_returns__mutmut_7": x_validate_returns__mutmut_7,
    "x_validate_returns__mutmut_8": x_validate_returns__mutmut_8,
    "x_validate_returns__mutmut_9": x_validate_returns__mutmut_9,
    "x_validate_returns__mutmut_10": x_validate_returns__mutmut_10,
    "x_validate_returns__mutmut_11": x_validate_returns__mutmut_11,
    "x_validate_returns__mutmut_12": x_validate_returns__mutmut_12,
    "x_validate_returns__mutmut_13": x_validate_returns__mutmut_13,
    "x_validate_returns__mutmut_14": x_validate_returns__mutmut_14,
    "x_validate_returns__mutmut_15": x_validate_returns__mutmut_15,
    "x_validate_returns__mutmut_16": x_validate_returns__mutmut_16,
    "x_validate_returns__mutmut_17": x_validate_returns__mutmut_17,
    "x_validate_returns__mutmut_18": x_validate_returns__mutmut_18,
    "x_validate_returns__mutmut_19": x_validate_returns__mutmut_19,
    "x_validate_returns__mutmut_20": x_validate_returns__mutmut_20,
    "x_validate_returns__mutmut_21": x_validate_returns__mutmut_21,
    "x_validate_returns__mutmut_22": x_validate_returns__mutmut_22,
    "x_validate_returns__mutmut_23": x_validate_returns__mutmut_23,
    "x_validate_returns__mutmut_24": x_validate_returns__mutmut_24,
    "x_validate_returns__mutmut_25": x_validate_returns__mutmut_25,
    "x_validate_returns__mutmut_26": x_validate_returns__mutmut_26,
    "x_validate_returns__mutmut_27": x_validate_returns__mutmut_27,
}
x_validate_returns__mutmut_orig.__name__ = "x_validate_returns"


def validate_positive_integer(val: int, name: str) -> int:
    args = [val, name]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_validate_positive_integer__mutmut_orig,
        x_validate_positive_integer__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_validate_positive_integer__mutmut_orig(val: int, name: str) -> int:
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


def x_validate_positive_integer__mutmut_1(val: int, name: str) -> int:
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
    if not isinstance(val, int) and val < 1:
        msg = f"{name} must be a positive integer, got {val}"
        raise ValueError(msg)
    return val


def x_validate_positive_integer__mutmut_2(val: int, name: str) -> int:
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
    if isinstance(val, int) or val < 1:
        msg = f"{name} must be a positive integer, got {val}"
        raise ValueError(msg)
    return val


def x_validate_positive_integer__mutmut_3(val: int, name: str) -> int:
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
    if not isinstance(val, int) or val <= 1:
        msg = f"{name} must be a positive integer, got {val}"
        raise ValueError(msg)
    return val


def x_validate_positive_integer__mutmut_4(val: int, name: str) -> int:
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
    if not isinstance(val, int) or val < 2:
        msg = f"{name} must be a positive integer, got {val}"
        raise ValueError(msg)
    return val


def x_validate_positive_integer__mutmut_5(val: int, name: str) -> int:
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
        msg = None
        raise ValueError(msg)
    return val


def x_validate_positive_integer__mutmut_6(val: int, name: str) -> int:
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
        raise ValueError(None)
    return val


x_validate_positive_integer__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_validate_positive_integer__mutmut_1": x_validate_positive_integer__mutmut_1,
    "x_validate_positive_integer__mutmut_2": x_validate_positive_integer__mutmut_2,
    "x_validate_positive_integer__mutmut_3": x_validate_positive_integer__mutmut_3,
    "x_validate_positive_integer__mutmut_4": x_validate_positive_integer__mutmut_4,
    "x_validate_positive_integer__mutmut_5": x_validate_positive_integer__mutmut_5,
    "x_validate_positive_integer__mutmut_6": x_validate_positive_integer__mutmut_6,
}
x_validate_positive_integer__mutmut_orig.__name__ = "x_validate_positive_integer"


def check_stationarity(params: NDArray[np.float64], p: int, q: int) -> bool:
    args = [params, p, q]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_check_stationarity__mutmut_orig, x_check_stationarity__mutmut_mutants, args, kwargs, None
    )


def x_check_stationarity__mutmut_orig(params: NDArray[np.float64], p: int, q: int) -> bool:
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


def x_check_stationarity__mutmut_1(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    alphas = None
    betas = params[1 + q : 1 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_2(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    alphas = params[2 : 1 + q]
    betas = params[1 + q : 1 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_3(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    alphas = params[1 : 1 - q]
    betas = params[1 + q : 1 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_4(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    alphas = params[1 : 2 + q]
    betas = params[1 + q : 1 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_5(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    betas = None
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_6(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    betas = params[1 - q : 1 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_7(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    betas = params[2 + q : 1 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_8(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    betas = params[1 + q : 1 + q - p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_9(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    betas = params[1 + q : 1 - q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_10(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    betas = params[1 + q : 2 + q + p]
    persistence = np.sum(alphas) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_11(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    persistence = None
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_12(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    persistence = np.sum(alphas) - np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_13(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    persistence = np.sum(None) + np.sum(betas)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_14(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    persistence = np.sum(alphas) + np.sum(None)
    return bool(persistence < 1.0)


def x_check_stationarity__mutmut_15(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    return bool(None)


def x_check_stationarity__mutmut_16(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    return bool(persistence <= 1.0)


def x_check_stationarity__mutmut_17(params: NDArray[np.float64], p: int, q: int) -> bool:
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
    return bool(persistence < 2.0)


x_check_stationarity__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_check_stationarity__mutmut_1": x_check_stationarity__mutmut_1,
    "x_check_stationarity__mutmut_2": x_check_stationarity__mutmut_2,
    "x_check_stationarity__mutmut_3": x_check_stationarity__mutmut_3,
    "x_check_stationarity__mutmut_4": x_check_stationarity__mutmut_4,
    "x_check_stationarity__mutmut_5": x_check_stationarity__mutmut_5,
    "x_check_stationarity__mutmut_6": x_check_stationarity__mutmut_6,
    "x_check_stationarity__mutmut_7": x_check_stationarity__mutmut_7,
    "x_check_stationarity__mutmut_8": x_check_stationarity__mutmut_8,
    "x_check_stationarity__mutmut_9": x_check_stationarity__mutmut_9,
    "x_check_stationarity__mutmut_10": x_check_stationarity__mutmut_10,
    "x_check_stationarity__mutmut_11": x_check_stationarity__mutmut_11,
    "x_check_stationarity__mutmut_12": x_check_stationarity__mutmut_12,
    "x_check_stationarity__mutmut_13": x_check_stationarity__mutmut_13,
    "x_check_stationarity__mutmut_14": x_check_stationarity__mutmut_14,
    "x_check_stationarity__mutmut_15": x_check_stationarity__mutmut_15,
    "x_check_stationarity__mutmut_16": x_check_stationarity__mutmut_16,
    "x_check_stationarity__mutmut_17": x_check_stationarity__mutmut_17,
}
x_check_stationarity__mutmut_orig.__name__ = "x_check_stationarity"
