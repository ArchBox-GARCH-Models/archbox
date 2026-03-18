"""Transition function visualization for STAR models.

Provides plots for Smooth Transition Autoregressive (STAR) models:
- Transition function G(s) for LSTAR/ESTAR
- Phase diagrams y_t vs y_{t-1} colored by regime
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from archbox.visualization.themes import Theme, get_theme


def plot_transition_function(
    results: Any,
    gamma_values: list[float] | None = None,
    n_points: int = 300,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot transition function G(s) for LSTAR/ESTAR models.

    Parameters
    ----------
    results : STARResults
        Fitted STAR results. Must have:
        - transition_variable: (T,) array of s_t values
        - gamma: transition speed parameter
        - c: location parameter (threshold)
        - transition_type: 'LSTAR' or 'ESTAR'
    gamma_values : list of float, optional
        Additional gamma values to overlay for comparison.
    n_points : int
        Number of points for the smooth curve.
    theme : str or Theme
        Visual theme.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom title.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size

        s_t = np.asarray(results.transition_variable, dtype=np.float64)
        gamma = float(results.gamma)
        c = float(results.c)
        trans_type = getattr(results, "transition_type", "LSTAR")

        # Create smooth s range
        s_min = min(s_t.min(), c - 3 * np.std(s_t))
        s_max = max(s_t.max(), c + 3 * np.std(s_t))
        s_range = np.linspace(s_min, s_max, n_points)

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        # Plot main transition function
        g_main = _compute_transition(s_range, gamma, c, trans_type)
        ax.plot(
            s_range,
            g_main,
            color=theme.colors.get("primary", "#1f4e79"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label=f"G(s), \u03b3={gamma:.2f}",
        )

        # Plot for different gamma values
        if gamma_values:
            color_cycle = [
                theme.colors.get("accent", "#c00000"),
                theme.colors.get("secondary", "#2e75b6"),
                theme.colors.get("positive", "#548235"),
            ]
            for idx, g in enumerate(gamma_values):
                g_alt = _compute_transition(s_range, g, c, trans_type)
                color = color_cycle[idx % len(color_cycle)]
                ax.plot(
                    s_range,
                    g_alt,
                    color=color,
                    linewidth=theme.line_widths.get("secondary", 1.0),
                    linestyle="--",
                    label=f"\u03b3={g:.2f}",
                )

        # Plot observed transition variable values
        g_observed = _compute_transition(s_t, gamma, c, trans_type)
        ax.scatter(
            s_t, g_observed, color=theme.colors.get("returns", "#7f7f7f"), s=5, alpha=0.3, zorder=0
        )

        # Reference lines
        ax.axhline(y=0.5, color=theme.colors.get("grid", "#cccccc"), linestyle=":", linewidth=0.7)
        ax.axvline(x=c, color=theme.colors.get("grid", "#cccccc"), linestyle=":", linewidth=0.7)

        ax.set_xlabel("Transition Variable (s)")
        ax.set_ylabel("G(s)")
        ax.set_ylim(-0.05, 1.05)
        ax.set_title(title or f"{trans_type} Transition Function")
        ax.legend(loc="lower right", framealpha=0.8)

        fig.tight_layout()
        return fig


def plot_phase_diagram(
    results: Any,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot phase diagram y_t vs y_{t-1} colored by regime.

    Parameters
    ----------
    results : STARResults or RegimeResults
        Fitted results with:
        - series: (T,) original series
        - regime_probs or smoothed_probs: (T, K) probabilities
    theme : str or Theme
        Visual theme.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom title.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size

        series = np.asarray(results.series, dtype=np.float64)
        y_t = series[1:]
        y_tm1 = series[:-1]

        # Get regime assignment
        if hasattr(results, "smoothed_probs"):
            probs = np.asarray(results.smoothed_probs, dtype=np.float64)
        elif hasattr(results, "regime_probs"):
            probs = np.asarray(results.regime_probs, dtype=np.float64)
        else:
            # Fallback: single regime
            probs = np.ones((len(series), 1))

        # Use probabilities from t=1 onward (matching y_t)
        probs = probs[1:]
        regime_class = np.argmax(probs, axis=1)
        n_regimes = probs.shape[1]

        regime_colors = [
            "#2e75b6",  # Blue
            "#c00000",  # Red
            "#548235",  # Green
            "#ffc000",  # Yellow
        ]

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        for k in range(n_regimes):
            mask = regime_class == k
            ax.scatter(
                y_tm1[mask],
                y_t[mask],
                color=regime_colors[k % len(regime_colors)],
                s=15,
                alpha=0.5,
                label=f"Regime {k + 1}",
                edgecolors="none",
            )

            # Regression line per regime
            if np.sum(mask) > 2:
                coeffs = np.polyfit(y_tm1[mask], y_t[mask], 1)
                x_fit = np.linspace(y_tm1[mask].min(), y_tm1[mask].max(), 50)
                y_fit = np.polyval(coeffs, x_fit)
                ax.plot(
                    x_fit,
                    y_fit,
                    color=regime_colors[k % len(regime_colors)],
                    linewidth=theme.line_widths.get("primary", 1.5),
                    linestyle="--",
                    alpha=0.8,
                )

        # 45-degree line
        lims = [min(y_tm1.min(), y_t.min()), max(y_tm1.max(), y_t.max())]
        ax.plot(lims, lims, color=theme.colors.get("grid", "#cccccc"), linestyle=":", linewidth=0.7)

        ax.set_xlabel(r"$y_{t-1}$")
        ax.set_ylabel(r"$y_t$")
        ax.set_title(title or "Phase Diagram")
        ax.legend(loc="upper left", framealpha=0.8)

        fig.tight_layout()
        return fig


def _compute_transition(
    s: NDArray[np.float64],
    gamma: float,
    c: float,
    trans_type: str,
) -> NDArray[np.float64]:
    """Compute transition function value.

    Parameters
    ----------
    s : ndarray
        Transition variable values.
    gamma : float
        Transition speed parameter.
    c : float
        Location parameter (threshold).
    trans_type : str
        'LSTAR' or 'ESTAR'.

    Returns
    -------
    ndarray
        Transition function values in [0, 1].
    """
    if trans_type.upper() == "LSTAR":
        # Logistic: G(s) = 1 / (1 + exp(-gamma * (s - c)))
        arg = -gamma * (s - c)
        # Clip to avoid overflow
        arg = np.clip(arg, -500, 500)
        result: NDArray[np.float64] = 1.0 / (1.0 + np.exp(arg))
    elif trans_type.upper() == "ESTAR":
        # Exponential: G(s) = 1 - exp(-gamma * (s - c)^2)
        result = 1.0 - np.exp(-gamma * (s - c) ** 2)
    else:
        msg = f"Unknown transition type: {trans_type}. Use 'LSTAR' or 'ESTAR'."
        raise ValueError(msg)

    return result
