"""News Impact Curve visualization for archbox.

The News Impact Curve (NIC) shows how past shocks (eps_{t-1}) affect
current conditional variance (sigma^2_t). For symmetric models (GARCH),
the NIC is a parabola. For asymmetric models (EGARCH, GJR), negative
shocks generate more volatility than positive shocks of the same magnitude.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from archbox.visualization.themes import Theme, get_theme


def plot_news_impact(
    results: Any,
    n_points: int = 200,
    n_sigma: float = 3.0,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot the News Impact Curve.

    Parameters
    ----------
    results : ArchResults
        Fitted model results. Must have a `news_impact` method or
        sufficient parameters to compute the NIC.
    n_points : int
        Number of points on the x-axis.
    n_sigma : float
        Range in standard deviations (from -n_sigma*sigma to +n_sigma*sigma).
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
        fig_size = figsize or theme.figure_size

        # Compute NIC data
        if hasattr(results, "news_impact"):
            eps_range, sigma2 = results.news_impact(n_points=n_points, n_sigma=n_sigma)
        else:
            # Fallback: compute from parameters
            eps_range, sigma2 = _compute_news_impact(results, n_points, n_sigma)

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        ax.plot(
            eps_range,
            sigma2,
            color=theme.colors.get("primary", "#1f4e79"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label=getattr(results, "model_name", "Model"),
        )

        # Add symmetric reference (parabola)
        if hasattr(results, "params") and len(results.params) > 0:
            omega = results.params[0] if hasattr(results, "params") else np.mean(sigma2)
            sym_sigma2 = omega + np.mean(sigma2) / np.max(eps_range**2 + 1e-12) * eps_range**2
            ax.plot(
                eps_range,
                sym_sigma2,
                color=theme.colors.get("grid", "#cccccc"),
                linewidth=theme.line_widths.get("secondary", 0.8),
                linestyle="--",
                alpha=0.5,
                label="Symmetric Reference",
            )

        # Highlight asymmetry region
        ax.axvline(
            x=0,
            color=theme.colors.get("grid", "#cccccc"),
            linewidth=theme.line_widths.get("grid", 0.5),
            linestyle=":",
        )

        ax.set_xlabel(r"$\varepsilon_{t-1}$")
        ax.set_ylabel(r"$\sigma^2_t$")
        ax.set_title(title or "News Impact Curve")
        ax.legend(loc="upper center", framealpha=0.8)

        fig.tight_layout()
        return fig


def plot_news_impact_comparison(
    results_list: list[Any],
    labels: list[str] | None = None,
    n_points: int = 200,
    n_sigma: float = 3.0,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot multiple News Impact Curves for comparison.

    Parameters
    ----------
    results_list : list
        List of fitted model results.
    labels : list of str, optional
        Labels for each model. If None, uses model_name attribute.
    n_points : int
        Number of points on the x-axis.
    n_sigma : float
        Range in standard deviations.
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

    if labels is None:
        labels = [getattr(r, "model_name", f"Model {i}") for i, r in enumerate(results_list)]

    rc_params = theme.to_matplotlib_rcparams()
    color_cycle = [
        theme.colors.get("primary", "#1f4e79"),
        theme.colors.get("accent", "#c00000"),
        theme.colors.get("secondary", "#2e75b6"),
        theme.colors.get("positive", "#548235"),
    ]

    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size
        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        for idx, (results, label) in enumerate(zip(results_list, labels, strict=False)):
            if hasattr(results, "news_impact"):
                eps_range, sigma2 = results.news_impact(n_points=n_points, n_sigma=n_sigma)
            else:
                eps_range, sigma2 = _compute_news_impact(results, n_points, n_sigma)

            color = color_cycle[idx % len(color_cycle)]
            ax.plot(
                eps_range,
                sigma2,
                color=color,
                linewidth=theme.line_widths.get("primary", 1.5),
                label=label,
            )

        ax.axvline(
            x=0,
            color=theme.colors.get("grid", "#cccccc"),
            linewidth=theme.line_widths.get("grid", 0.5),
            linestyle=":",
        )

        ax.set_xlabel(r"$\varepsilon_{t-1}$")
        ax.set_ylabel(r"$\sigma^2_t$")
        ax.set_title(title or "News Impact Curve Comparison")
        ax.legend(loc="upper center", framealpha=0.8)

        fig.tight_layout()
        return fig


def _compute_news_impact(
    results: Any, n_points: int, n_sigma: float
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute News Impact Curve from model parameters.

    Fallback computation when results doesn't have a news_impact method.
    Uses the variance recursion with a single shock.
    """
    # Get unconditional variance
    if hasattr(results, "conditional_volatility"):
        sigma_bar = float(np.mean(results.conditional_volatility))
    else:
        sigma_bar = 0.01

    eps_range = np.linspace(-n_sigma * sigma_bar, n_sigma * sigma_bar, n_points)

    # Get model parameters
    params = np.asarray(results.params, dtype=np.float64) if hasattr(results, "params") else None

    if params is not None and len(params) >= 3:
        omega = params[0]
        alpha = params[1]
        beta = params[2] if len(params) > 2 else 0.0
        sigma2_bar = omega / (1.0 - alpha - beta) if (alpha + beta) < 1 else sigma_bar**2

        # GARCH NIC: sigma^2_t = omega + alpha * eps^2_{t-1} + beta * sigma^2_bar
        sigma2 = omega + alpha * eps_range**2 + beta * sigma2_bar
    else:
        # Fallback: simple parabola
        sigma2 = sigma_bar**2 + 0.1 * eps_range**2

    return eps_range, sigma2
