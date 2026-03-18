"""Transition functions for threshold and STAR models.

This module provides the core transition functions used by LSTAR, ESTAR,
and related smooth transition autoregressive models.

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    import matplotlib.figure
from collections.abc import Callable
from typing import Annotated, ClassVar

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


def logistic_transition(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    args = [s, gamma, c]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_logistic_transition__mutmut_orig,
        x_logistic_transition__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_logistic_transition__mutmut_orig(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_1(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = None
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_2(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(None, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_3(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=None)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_4(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_5(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(
        s,
    )
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_6(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = None
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_7(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma / (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_8(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = +gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_9(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s + c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_10(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = None
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_11(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(None, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_12(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, None, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_13(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, None)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_14(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(-500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_15(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_16(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(
        exponent,
        -500.0,
    )
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_17(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, +500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_18(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -501.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_19(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 501.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_20(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 * (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_21(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 2.0 / (1.0 + np.exp(exponent))


def x_logistic_transition__mutmut_22(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 - np.exp(exponent))


def x_logistic_transition__mutmut_23(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (2.0 + np.exp(exponent))


def x_logistic_transition__mutmut_24(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Logistic transition function.

    G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    # Clip exponent to avoid overflow
    exponent = -gamma * (s - c)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(None))


x_logistic_transition__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_logistic_transition__mutmut_1": x_logistic_transition__mutmut_1,
    "x_logistic_transition__mutmut_2": x_logistic_transition__mutmut_2,
    "x_logistic_transition__mutmut_3": x_logistic_transition__mutmut_3,
    "x_logistic_transition__mutmut_4": x_logistic_transition__mutmut_4,
    "x_logistic_transition__mutmut_5": x_logistic_transition__mutmut_5,
    "x_logistic_transition__mutmut_6": x_logistic_transition__mutmut_6,
    "x_logistic_transition__mutmut_7": x_logistic_transition__mutmut_7,
    "x_logistic_transition__mutmut_8": x_logistic_transition__mutmut_8,
    "x_logistic_transition__mutmut_9": x_logistic_transition__mutmut_9,
    "x_logistic_transition__mutmut_10": x_logistic_transition__mutmut_10,
    "x_logistic_transition__mutmut_11": x_logistic_transition__mutmut_11,
    "x_logistic_transition__mutmut_12": x_logistic_transition__mutmut_12,
    "x_logistic_transition__mutmut_13": x_logistic_transition__mutmut_13,
    "x_logistic_transition__mutmut_14": x_logistic_transition__mutmut_14,
    "x_logistic_transition__mutmut_15": x_logistic_transition__mutmut_15,
    "x_logistic_transition__mutmut_16": x_logistic_transition__mutmut_16,
    "x_logistic_transition__mutmut_17": x_logistic_transition__mutmut_17,
    "x_logistic_transition__mutmut_18": x_logistic_transition__mutmut_18,
    "x_logistic_transition__mutmut_19": x_logistic_transition__mutmut_19,
    "x_logistic_transition__mutmut_20": x_logistic_transition__mutmut_20,
    "x_logistic_transition__mutmut_21": x_logistic_transition__mutmut_21,
    "x_logistic_transition__mutmut_22": x_logistic_transition__mutmut_22,
    "x_logistic_transition__mutmut_23": x_logistic_transition__mutmut_23,
    "x_logistic_transition__mutmut_24": x_logistic_transition__mutmut_24,
}
x_logistic_transition__mutmut_orig.__name__ = "x_logistic_transition"


def exponential_transition(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    args = [s, gamma, c]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_exponential_transition__mutmut_orig,
        x_exponential_transition__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_exponential_transition__mutmut_orig(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_1(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = None
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_2(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(None, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_3(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=None)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_4(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_5(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(
        s,
    )
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_6(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = None
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_7(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma / (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_8(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = +gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_9(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) * 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_10(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s + c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_11(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 3
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_12(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = None
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_13(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(None, -500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_14(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, None, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_15(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, None)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_16(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(-500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_17(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_18(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(
        exponent,
        -500.0,
    )
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_19(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, +500.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_20(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -501.0, 0.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_21(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 1.0)
    return 1.0 - np.exp(exponent)


def x_exponential_transition__mutmut_22(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 + np.exp(exponent)


def x_exponential_transition__mutmut_23(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 2.0 - np.exp(exponent)


def x_exponential_transition__mutmut_24(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
) -> NDArray[np.float64]:
    """Exponential transition function.

    G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c : float
        Location parameter (center of symmetry).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c) ** 2
    exponent = np.clip(exponent, -500.0, 0.0)
    return 1.0 - np.exp(None)


x_exponential_transition__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_exponential_transition__mutmut_1": x_exponential_transition__mutmut_1,
    "x_exponential_transition__mutmut_2": x_exponential_transition__mutmut_2,
    "x_exponential_transition__mutmut_3": x_exponential_transition__mutmut_3,
    "x_exponential_transition__mutmut_4": x_exponential_transition__mutmut_4,
    "x_exponential_transition__mutmut_5": x_exponential_transition__mutmut_5,
    "x_exponential_transition__mutmut_6": x_exponential_transition__mutmut_6,
    "x_exponential_transition__mutmut_7": x_exponential_transition__mutmut_7,
    "x_exponential_transition__mutmut_8": x_exponential_transition__mutmut_8,
    "x_exponential_transition__mutmut_9": x_exponential_transition__mutmut_9,
    "x_exponential_transition__mutmut_10": x_exponential_transition__mutmut_10,
    "x_exponential_transition__mutmut_11": x_exponential_transition__mutmut_11,
    "x_exponential_transition__mutmut_12": x_exponential_transition__mutmut_12,
    "x_exponential_transition__mutmut_13": x_exponential_transition__mutmut_13,
    "x_exponential_transition__mutmut_14": x_exponential_transition__mutmut_14,
    "x_exponential_transition__mutmut_15": x_exponential_transition__mutmut_15,
    "x_exponential_transition__mutmut_16": x_exponential_transition__mutmut_16,
    "x_exponential_transition__mutmut_17": x_exponential_transition__mutmut_17,
    "x_exponential_transition__mutmut_18": x_exponential_transition__mutmut_18,
    "x_exponential_transition__mutmut_19": x_exponential_transition__mutmut_19,
    "x_exponential_transition__mutmut_20": x_exponential_transition__mutmut_20,
    "x_exponential_transition__mutmut_21": x_exponential_transition__mutmut_21,
    "x_exponential_transition__mutmut_22": x_exponential_transition__mutmut_22,
    "x_exponential_transition__mutmut_23": x_exponential_transition__mutmut_23,
    "x_exponential_transition__mutmut_24": x_exponential_transition__mutmut_24,
}
x_exponential_transition__mutmut_orig.__name__ = "x_exponential_transition"


def logistic_transition_order2(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    args = [s, gamma, c1, c2]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_logistic_transition_order2__mutmut_orig,
        x_logistic_transition_order2__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_logistic_transition_order2__mutmut_orig(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_1(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = None
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_2(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(None, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_3(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=None)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_4(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_5(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(
        s,
    )
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_6(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = None
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_7(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) / (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_8(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma / (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_9(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = +gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_10(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s + c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_11(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s + c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_12(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = None
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_13(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(None, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_14(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, None, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_15(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, None)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_16(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(-500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_17(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_18(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(
        exponent,
        -500.0,
    )
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_19(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, +500.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_20(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -501.0, 500.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_21(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 501.0)
    return 1.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_22(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 * (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_23(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 2.0 / (1.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_24(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 - np.exp(exponent))


def x_logistic_transition_order2__mutmut_25(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (2.0 + np.exp(exponent))


def x_logistic_transition_order2__mutmut_26(
    s: NDArray[np.float64],
    gamma: float,
    c1: float,
    c2: float,
) -> NDArray[np.float64]:
    """Second-order logistic transition function for 3-regime LSTAR.

    G(s; gamma, c1, c2) = 1 / (1 + exp(-gamma * (s - c1) * (s - c2)))

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Speed of transition (gamma > 0).
    c1 : float
        First location parameter (lower threshold).
    c2 : float
        Second location parameter (upper threshold).

    Returns
    -------
    ndarray
        Transition values in [0, 1], same shape as s.
    """
    s = np.asarray(s, dtype=np.float64)
    exponent = -gamma * (s - c1) * (s - c2)
    exponent = np.clip(exponent, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(None))


x_logistic_transition_order2__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_logistic_transition_order2__mutmut_1": x_logistic_transition_order2__mutmut_1,
    "x_logistic_transition_order2__mutmut_2": x_logistic_transition_order2__mutmut_2,
    "x_logistic_transition_order2__mutmut_3": x_logistic_transition_order2__mutmut_3,
    "x_logistic_transition_order2__mutmut_4": x_logistic_transition_order2__mutmut_4,
    "x_logistic_transition_order2__mutmut_5": x_logistic_transition_order2__mutmut_5,
    "x_logistic_transition_order2__mutmut_6": x_logistic_transition_order2__mutmut_6,
    "x_logistic_transition_order2__mutmut_7": x_logistic_transition_order2__mutmut_7,
    "x_logistic_transition_order2__mutmut_8": x_logistic_transition_order2__mutmut_8,
    "x_logistic_transition_order2__mutmut_9": x_logistic_transition_order2__mutmut_9,
    "x_logistic_transition_order2__mutmut_10": x_logistic_transition_order2__mutmut_10,
    "x_logistic_transition_order2__mutmut_11": x_logistic_transition_order2__mutmut_11,
    "x_logistic_transition_order2__mutmut_12": x_logistic_transition_order2__mutmut_12,
    "x_logistic_transition_order2__mutmut_13": x_logistic_transition_order2__mutmut_13,
    "x_logistic_transition_order2__mutmut_14": x_logistic_transition_order2__mutmut_14,
    "x_logistic_transition_order2__mutmut_15": x_logistic_transition_order2__mutmut_15,
    "x_logistic_transition_order2__mutmut_16": x_logistic_transition_order2__mutmut_16,
    "x_logistic_transition_order2__mutmut_17": x_logistic_transition_order2__mutmut_17,
    "x_logistic_transition_order2__mutmut_18": x_logistic_transition_order2__mutmut_18,
    "x_logistic_transition_order2__mutmut_19": x_logistic_transition_order2__mutmut_19,
    "x_logistic_transition_order2__mutmut_20": x_logistic_transition_order2__mutmut_20,
    "x_logistic_transition_order2__mutmut_21": x_logistic_transition_order2__mutmut_21,
    "x_logistic_transition_order2__mutmut_22": x_logistic_transition_order2__mutmut_22,
    "x_logistic_transition_order2__mutmut_23": x_logistic_transition_order2__mutmut_23,
    "x_logistic_transition_order2__mutmut_24": x_logistic_transition_order2__mutmut_24,
    "x_logistic_transition_order2__mutmut_25": x_logistic_transition_order2__mutmut_25,
    "x_logistic_transition_order2__mutmut_26": x_logistic_transition_order2__mutmut_26,
}
x_logistic_transition_order2__mutmut_orig.__name__ = "x_logistic_transition_order2"


def plot_transition(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    args = [s_range, gamma_values, c, transition_type]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_plot_transition__mutmut_orig, x_plot_transition__mutmut_mutants, args, kwargs, None
    )


def x_plot_transition__mutmut_orig(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_1(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "XXlogisticXX",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_2(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "LOGISTIC",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_3(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = None

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_4(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=None)

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_5(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(11, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_6(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 7))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_7(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type != "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_8(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "XXlogisticXX":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_9(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "LOGISTIC":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_10(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = None
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_11(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(None, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_12(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, None, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_13(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, None)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_14(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_15(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_16(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(
                s_range,
                gamma,
            )
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_17(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = None
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_18(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type != "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_19(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "XXexponentialXX":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_20(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "EXPONENTIAL":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_21(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = None
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_22(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(None, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_23(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, None, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_24(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, None)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_25(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_26(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_27(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(
                s_range,
                gamma,
            )
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_28(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = None
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_29(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = None
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_30(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(None)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_31(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(None, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_32(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, None, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_33(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=None)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_34(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_35(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_36(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(
            s_range,
            g_vals,
        )

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_37(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=None, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_38(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color=None, linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_39(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle=None, alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_40(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=None)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_41(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_42(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_43(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_44(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(
        y=0.5,
        color="gray",
        linestyle="--",
    )
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_45(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=1.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_46(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="XXgrayXX", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_47(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="GRAY", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_48(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="XX--XX", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_49(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=1.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_50(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=None, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_51(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color=None, linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_52(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle=None, alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_53(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=None)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_54(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_55(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_56(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_57(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(
        x=c,
        color="gray",
        linestyle="--",
    )
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_58(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="XXgrayXX", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_59(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="GRAY", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_60(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="XX--XX", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_61(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=1.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_62(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(None)
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_63(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("XXs (transition variable)XX")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_64(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("S (TRANSITION VARIABLE)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_65(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel(None)
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_66(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("XXG(s; gamma, c)XX")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_67(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("g(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_68(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(S; GAMMA, C)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_69(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(None)
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_70(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(None, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_71(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, None)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_72(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_73(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(
        -0.05,
    )
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_74(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(+0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_75(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-1.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_76(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 2.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_77(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(None, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_78(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=None)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_79(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_80(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(
        True,
    )
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_81(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(False, alpha=0.3)
    plt.tight_layout()

    return fig


def x_plot_transition__mutmut_82(
    s_range: NDArray[np.float64],
    gamma_values: list[float],
    c: float,
    transition_type: str = "logistic",
) -> matplotlib.figure.Figure:
    """Plot transition function for various gamma values.

    Parameters
    ----------
    s_range : ndarray
        Range of transition variable values.
    gamma_values : list[float]
        List of gamma values to plot.
    c : float
        Location parameter.
    transition_type : str
        Type of transition: 'logistic' or 'exponential'.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib figure object.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    for gamma in gamma_values:
        if transition_type == "logistic":
            g_vals = logistic_transition(s_range, gamma, c)
            label = f"Logistic (gamma={gamma})"
        elif transition_type == "exponential":
            g_vals = exponential_transition(s_range, gamma, c)
            label = f"Exponential (gamma={gamma})"
        else:
            msg = f"Unknown transition type: {transition_type}"
            raise ValueError(msg)
        ax.plot(s_range, g_vals, label=label)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(x=c, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s (transition variable)")
    ax.set_ylabel("G(s; gamma, c)")
    ax.set_title(f"{transition_type.capitalize()} Transition Function (c={c})")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=1.3)
    plt.tight_layout()

    return fig


x_plot_transition__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_plot_transition__mutmut_1": x_plot_transition__mutmut_1,
    "x_plot_transition__mutmut_2": x_plot_transition__mutmut_2,
    "x_plot_transition__mutmut_3": x_plot_transition__mutmut_3,
    "x_plot_transition__mutmut_4": x_plot_transition__mutmut_4,
    "x_plot_transition__mutmut_5": x_plot_transition__mutmut_5,
    "x_plot_transition__mutmut_6": x_plot_transition__mutmut_6,
    "x_plot_transition__mutmut_7": x_plot_transition__mutmut_7,
    "x_plot_transition__mutmut_8": x_plot_transition__mutmut_8,
    "x_plot_transition__mutmut_9": x_plot_transition__mutmut_9,
    "x_plot_transition__mutmut_10": x_plot_transition__mutmut_10,
    "x_plot_transition__mutmut_11": x_plot_transition__mutmut_11,
    "x_plot_transition__mutmut_12": x_plot_transition__mutmut_12,
    "x_plot_transition__mutmut_13": x_plot_transition__mutmut_13,
    "x_plot_transition__mutmut_14": x_plot_transition__mutmut_14,
    "x_plot_transition__mutmut_15": x_plot_transition__mutmut_15,
    "x_plot_transition__mutmut_16": x_plot_transition__mutmut_16,
    "x_plot_transition__mutmut_17": x_plot_transition__mutmut_17,
    "x_plot_transition__mutmut_18": x_plot_transition__mutmut_18,
    "x_plot_transition__mutmut_19": x_plot_transition__mutmut_19,
    "x_plot_transition__mutmut_20": x_plot_transition__mutmut_20,
    "x_plot_transition__mutmut_21": x_plot_transition__mutmut_21,
    "x_plot_transition__mutmut_22": x_plot_transition__mutmut_22,
    "x_plot_transition__mutmut_23": x_plot_transition__mutmut_23,
    "x_plot_transition__mutmut_24": x_plot_transition__mutmut_24,
    "x_plot_transition__mutmut_25": x_plot_transition__mutmut_25,
    "x_plot_transition__mutmut_26": x_plot_transition__mutmut_26,
    "x_plot_transition__mutmut_27": x_plot_transition__mutmut_27,
    "x_plot_transition__mutmut_28": x_plot_transition__mutmut_28,
    "x_plot_transition__mutmut_29": x_plot_transition__mutmut_29,
    "x_plot_transition__mutmut_30": x_plot_transition__mutmut_30,
    "x_plot_transition__mutmut_31": x_plot_transition__mutmut_31,
    "x_plot_transition__mutmut_32": x_plot_transition__mutmut_32,
    "x_plot_transition__mutmut_33": x_plot_transition__mutmut_33,
    "x_plot_transition__mutmut_34": x_plot_transition__mutmut_34,
    "x_plot_transition__mutmut_35": x_plot_transition__mutmut_35,
    "x_plot_transition__mutmut_36": x_plot_transition__mutmut_36,
    "x_plot_transition__mutmut_37": x_plot_transition__mutmut_37,
    "x_plot_transition__mutmut_38": x_plot_transition__mutmut_38,
    "x_plot_transition__mutmut_39": x_plot_transition__mutmut_39,
    "x_plot_transition__mutmut_40": x_plot_transition__mutmut_40,
    "x_plot_transition__mutmut_41": x_plot_transition__mutmut_41,
    "x_plot_transition__mutmut_42": x_plot_transition__mutmut_42,
    "x_plot_transition__mutmut_43": x_plot_transition__mutmut_43,
    "x_plot_transition__mutmut_44": x_plot_transition__mutmut_44,
    "x_plot_transition__mutmut_45": x_plot_transition__mutmut_45,
    "x_plot_transition__mutmut_46": x_plot_transition__mutmut_46,
    "x_plot_transition__mutmut_47": x_plot_transition__mutmut_47,
    "x_plot_transition__mutmut_48": x_plot_transition__mutmut_48,
    "x_plot_transition__mutmut_49": x_plot_transition__mutmut_49,
    "x_plot_transition__mutmut_50": x_plot_transition__mutmut_50,
    "x_plot_transition__mutmut_51": x_plot_transition__mutmut_51,
    "x_plot_transition__mutmut_52": x_plot_transition__mutmut_52,
    "x_plot_transition__mutmut_53": x_plot_transition__mutmut_53,
    "x_plot_transition__mutmut_54": x_plot_transition__mutmut_54,
    "x_plot_transition__mutmut_55": x_plot_transition__mutmut_55,
    "x_plot_transition__mutmut_56": x_plot_transition__mutmut_56,
    "x_plot_transition__mutmut_57": x_plot_transition__mutmut_57,
    "x_plot_transition__mutmut_58": x_plot_transition__mutmut_58,
    "x_plot_transition__mutmut_59": x_plot_transition__mutmut_59,
    "x_plot_transition__mutmut_60": x_plot_transition__mutmut_60,
    "x_plot_transition__mutmut_61": x_plot_transition__mutmut_61,
    "x_plot_transition__mutmut_62": x_plot_transition__mutmut_62,
    "x_plot_transition__mutmut_63": x_plot_transition__mutmut_63,
    "x_plot_transition__mutmut_64": x_plot_transition__mutmut_64,
    "x_plot_transition__mutmut_65": x_plot_transition__mutmut_65,
    "x_plot_transition__mutmut_66": x_plot_transition__mutmut_66,
    "x_plot_transition__mutmut_67": x_plot_transition__mutmut_67,
    "x_plot_transition__mutmut_68": x_plot_transition__mutmut_68,
    "x_plot_transition__mutmut_69": x_plot_transition__mutmut_69,
    "x_plot_transition__mutmut_70": x_plot_transition__mutmut_70,
    "x_plot_transition__mutmut_71": x_plot_transition__mutmut_71,
    "x_plot_transition__mutmut_72": x_plot_transition__mutmut_72,
    "x_plot_transition__mutmut_73": x_plot_transition__mutmut_73,
    "x_plot_transition__mutmut_74": x_plot_transition__mutmut_74,
    "x_plot_transition__mutmut_75": x_plot_transition__mutmut_75,
    "x_plot_transition__mutmut_76": x_plot_transition__mutmut_76,
    "x_plot_transition__mutmut_77": x_plot_transition__mutmut_77,
    "x_plot_transition__mutmut_78": x_plot_transition__mutmut_78,
    "x_plot_transition__mutmut_79": x_plot_transition__mutmut_79,
    "x_plot_transition__mutmut_80": x_plot_transition__mutmut_80,
    "x_plot_transition__mutmut_81": x_plot_transition__mutmut_81,
    "x_plot_transition__mutmut_82": x_plot_transition__mutmut_82,
}
x_plot_transition__mutmut_orig.__name__ = "x_plot_transition"
