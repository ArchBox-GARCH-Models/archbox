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


def logistic_transition(
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


def exponential_transition(
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


def logistic_transition_order2(
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


def plot_transition(
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
