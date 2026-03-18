"""Correlation visualization for multivariate GARCH models.

Provides plots for dynamic correlations (DCC), correlation heatmaps,
and covariance decomposition.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from archbox.visualization.themes import Theme, get_theme


def plot_dynamic_correlation(
    results: Any,
    i: int = 0,
    j: int = 1,
    ccc_reference: bool = True,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot dynamic correlation between two series.

    Parameters
    ----------
    results : MultivariateResults
        Fitted multivariate model results with dynamic_correlations attribute.
    i : int
        Index of first series.
    j : int
        Index of second series.
    ccc_reference : bool
        If True, overlay constant (CCC) correlation as reference.
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

        # Extract dynamic correlations
        rho_t: NDArray[np.float64] = np.asarray(
            results.dynamic_correlations[:, i, j], dtype=np.float64
        )
        n_obs = len(rho_t)
        t_axis = np.arange(n_obs)

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        # Dynamic correlation
        ax.plot(
            t_axis,
            rho_t,
            color=theme.colors.get("primary", "#1f4e79"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label=r"$\rho_{ij,t}$ (DCC)",
        )

        # Confidence bands (approximate)
        rho_mean = float(np.mean(rho_t))
        rho_std = float(np.std(rho_t))
        ax.fill_between(
            t_axis,
            rho_t - 1.96 * rho_std * 0.1,
            rho_t + 1.96 * rho_std * 0.1,
            color=theme.colors.get("confidence_band", "#2e75b6"),
            alpha=0.1,
        )

        # CCC reference
        if ccc_reference:
            ax.axhline(
                y=rho_mean,
                color=theme.colors.get("accent", "#c00000"),
                linewidth=theme.line_widths.get("secondary", 1.0),
                linestyle="--",
                label=f"CCC = {rho_mean:.3f}",
            )

        series_names = getattr(results, "series_names", [f"Series {i}", f"Series {j}"])
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def plot_correlation_heatmap(
    results: Any,
    t: int | None = None,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot correlation matrix as heatmap.

    Parameters
    ----------
    results : MultivariateResults
        Fitted results with dynamic_correlations attribute (T, K, K).
    t : int, optional
        Time point for the correlation matrix. If None, uses the mean.
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
        corr_matrices = np.asarray(results.dynamic_correlations, dtype=np.float64)
        k = corr_matrices.shape[1]

        if t is not None:
            corr_mat = corr_matrices[t]
            subtitle = f"(t={t})"
        else:
            corr_mat = np.mean(corr_matrices, axis=0)
            subtitle = "(Mean)"

        fig_size = figsize or (max(6, k * 1.5), max(5, k * 1.3))
        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
        fig.colorbar(im, ax=ax, label="Correlation")

        # Add text annotations
        for row in range(k):
            for col in range(k):
                color = "white" if abs(corr_mat[row, col]) > 0.5 else "black"
                ax.text(
                    col,
                    row,
                    f"{corr_mat[row, col]:.3f}",
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=theme.font_sizes.get("annotation", 9),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def plot_covariance_decomposition(
    results: Any,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot covariance decomposition as stacked area chart.

    Shows variance of each series and covariance terms over time.

    Parameters
    ----------
    results : MultivariateResults
        Fitted results with dynamic_covariances (T, K, K).
    theme : str or Theme
        Visual theme.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom title.

    Returns
    -------
    matplotlib.figure.Figure
        Stacked area figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size

        cov_array = np.asarray(results.dynamic_covariances, dtype=np.float64)
        n_obs, k, _ = cov_array.shape
        t_axis = np.arange(n_obs)

        series_names = getattr(results, "series_names", [f"Series {idx}" for idx in range(k)])

        color_cycle = [
            "#2e75b6",
            "#c00000",
            "#548235",
            "#ffc000",
            "#7030a0",
        ]

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        # Extract variances (diagonal elements)
        variances = np.array([cov_array[:, idx, idx] for idx in range(k)])

        ax.stackplot(
            t_axis,
            *variances,
            labels=[f"Var({name})" for name in series_names[:k]],
            colors=color_cycle[:k],
            alpha=0.7,
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig
