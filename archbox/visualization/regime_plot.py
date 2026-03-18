"""Regime-switching visualization for archbox.

Provides plots for Markov-Switching models showing regime shading,
smoothed/filtered probabilities, expected durations, and transition matrices.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from numpy.typing import NDArray

from archbox.visualization.themes import Theme, get_theme

# Default color palette for regimes
_REGIME_COLORS = [
    "#2e75b6",  # Blue (low vol / expansion)
    "#c00000",  # Red (high vol / recession)
    "#548235",  # Green (medium)
    "#ffc000",  # Yellow (transition)
    "#7030a0",  # Purple (extra)
]

_REGIME_ALPHAS = [0.15, 0.25, 0.20, 0.20, 0.20]


def plot_regimes(
    results: Any,
    which_probs: str = "smoothed",
    threshold: float = 0.5,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot regime-switching analysis panel.

    Creates a vertical panel with 3 subplots:
    1. Original series with shaded background by regime
    2. Smoothed (or filtered) probabilities P(S_t=j | Y_T) per regime
    3. Expected duration per regime (horizontal bars)

    Parameters
    ----------
    results : RegimeResults
        Fitted regime-switching results. Must have:
        - series: original time series
        - smoothed_probs or filtered_probs: (T, K) array of regime probabilities
        - transition_matrix: (K, K) transition probability matrix
        - n_regimes: number of regimes
    which_probs : str
        'smoothed' or 'filtered' probabilities.
    threshold : float
        Cutoff for regime classification (default 0.5).
    theme : str or Theme
        Visual theme name or Theme instance.
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
        fig_size = figsize or (theme.figure_size[0], theme.figure_size[1] * 1.3)

        # Extract data
        series: NDArray[np.float64] = np.asarray(results.series, dtype=np.float64)
        n_obs = len(series)
        t_axis = np.arange(n_obs, dtype=np.float64)

        n_regimes: int = int(results.n_regimes)

        if which_probs == "smoothed" and hasattr(results, "smoothed_probs"):
            probs = np.asarray(results.smoothed_probs, dtype=np.float64)
        elif hasattr(results, "filtered_probs"):
            probs = np.asarray(results.filtered_probs, dtype=np.float64)
        else:
            probs = np.asarray(results.smoothed_probs, dtype=np.float64)

        # Transition matrix for expected durations
        trans_mat = np.asarray(results.transition_matrix, dtype=np.float64)

        # Classify regimes
        regime_class = np.argmax(probs, axis=1)

        fig, axes = plt.subplots(3, 1, figsize=fig_size, gridspec_kw={"height_ratios": [3, 2, 1]})

        # --- Panel 1: Series with regime shading ---
        ax1 = axes[0]
        ax1.plot(
            t_axis,
            series,
            color=theme.colors.get("primary", "#1f4e79"),
            linewidth=theme.line_widths.get("primary", 1.5),
        )

        # Add shaded backgrounds for each regime
        for k in range(n_regimes):
            color = _REGIME_COLORS[k % len(_REGIME_COLORS)]
            alpha = _REGIME_ALPHAS[k % len(_REGIME_ALPHAS)]
            mask = regime_class == k
            _shade_regions(ax1, t_axis, mask, color=color, alpha=alpha)

        legend_handles = [
            Patch(
                facecolor=_REGIME_COLORS[k % len(_REGIME_COLORS)],
                alpha=_REGIME_ALPHAS[k % len(_REGIME_ALPHAS)],
                label=f"Regime {k + 1}",
            )
            for k in range(n_regimes)
        ]
        ax1.legend(handles=legend_handles, loc="upper right", framealpha=0.8)
        ax1.set_ylabel("Series")
        ax1.set_title(title or "Regime-Switching Analysis")

        # --- Panel 2: Smoothed/Filtered Probabilities ---
        ax2 = axes[1]
        for k in range(n_regimes):
            color = _REGIME_COLORS[k % len(_REGIME_COLORS)]
            ax2.plot(
                t_axis,
                probs[:, k],
                color=color,
                linewidth=theme.line_widths.get("primary", 1.5),
                label=f"P(S_t={k + 1})",
            )

        ax2.axhline(
            y=threshold,
            color=theme.colors.get("grid", "#cccccc"),
            linestyle="--",
            linewidth=0.7,
            alpha=0.5,
        )
        ax2.set_ylabel("Probability")
        prob_label = "Smoothed" if which_probs == "smoothed" else "Filtered"
        ax2.set_title(f"{prob_label} Probabilities")
        ax2.legend(loc="upper right", framealpha=0.8)
        ax2.set_ylim(-0.05, 1.05)

        # --- Panel 3: Expected Durations ---
        ax3 = axes[2]
        durations = np.array(
            [
                1.0 / (1.0 - trans_mat[k, k]) if trans_mat[k, k] < 1 else np.inf
                for k in range(n_regimes)
            ]
        )

        bars = ax3.barh(
            [f"Regime {k + 1}" for k in range(n_regimes)],
            durations,
            color=[_REGIME_COLORS[k % len(_REGIME_COLORS)] for k in range(n_regimes)],
            alpha=0.7,
        )
        for bar, dur in zip(bars, durations, strict=True):
            if np.isfinite(dur):
                ax3.text(
                    bar.get_width() + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f"{dur:.1f} obs",
                    va="center",
                    fontsize=theme.font_sizes.get("annotation", 9),
                )
        ax3.set_xlabel("Expected Duration (observations)")
        ax3.set_title("Expected Regime Durations")

        fig.tight_layout()
        return fig


def plot_transition_matrix(
    results: Any,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot transition matrix as heatmap.

    Parameters
    ----------
    results : RegimeResults
        Fitted results with transition_matrix attribute.
    theme : str or Theme
        Visual theme.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom title.

    Returns
    -------
    matplotlib.figure.Figure
        Heatmap figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        trans_mat = np.asarray(results.transition_matrix, dtype=np.float64)
        n_states = trans_mat.shape[0]
        fig_size = figsize or (max(6, n_states * 2), max(5, n_states * 1.8))

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        im = ax.imshow(trans_mat, cmap="Blues", vmin=0, vmax=1, aspect="equal")
        fig.colorbar(im, ax=ax, label="Transition Probability")

        # Add text annotations
        for i in range(n_states):
            for j in range(n_states):
                color = "white" if trans_mat[i, j] > 0.5 else "black"
                ax.text(
                    j,
                    i,
                    f"{trans_mat[i, j]:.3f}",
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=theme.font_sizes.get("annotation", 9),
                )

        ax.set_xticks(range(n_states))
        ax.set_yticks(range(n_states))
        ax.set_xticklabels([f"Regime {k + 1}" for k in range(n_states)])
        ax.set_yticklabels([f"Regime {k + 1}" for k in range(n_states)])
        ax.set_xlabel("To")
        ax.set_ylabel("From")
        ax.set_title(title or "Transition Probability Matrix")

        fig.tight_layout()
        return fig


def _shade_regions(
    ax: Any,
    t_axis: NDArray[np.float64],
    mask: NDArray[np.bool_],
    color: str,
    alpha: float,
) -> None:
    """Add vertical shaded regions where mask is True."""
    in_region = False
    start = 0
    for i in range(len(mask)):
        if mask[i] and not in_region:
            start = i
            in_region = True
        elif not mask[i] and in_region:
            ax.axvspan(t_axis[start], t_axis[i - 1], color=color, alpha=alpha)
            in_region = False
    if in_region:
        ax.axvspan(t_axis[start], t_axis[-1], color=color, alpha=alpha)
