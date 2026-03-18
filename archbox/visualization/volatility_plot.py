"""Volatility visualization for archbox.

Provides plots for conditional volatility, returns with volatility bands,
standardized residuals, and variance persistence analysis.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from archbox.visualization.themes import Theme, get_theme


def plot_volatility(
    results: Any,
    annualize: bool = False,
    ci: float = 0.95,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot conditional volatility panel.

    Creates a vertical panel with 3 subplots:
    1. Returns: time series of returns
    2. Conditional Volatility: sigma_t with confidence bands
    3. Standardized Residuals: z_t = eps_t / sigma_t with +-2 lines

    Parameters
    ----------
    results : ArchResults
        Fitted model results containing conditional_volatility,
        resid, and std_resid attributes.
    annualize : bool
        If True, multiply sigma by sqrt(252).
    ci : float
        Confidence interval level (e.g. 0.95).
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

    # Apply theme
    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or (theme.figure_size[0], theme.figure_size[1] * 1.2)

        # Extract data from results
        returns: NDArray[np.float64] = np.asarray(results.resid, dtype=np.float64)
        sigma: NDArray[np.float64] = np.asarray(results.conditional_volatility, dtype=np.float64)

        # Check for standardized residuals
        if hasattr(results, "std_resid") and results.std_resid is not None:
            std_resid: NDArray[np.float64] = np.asarray(results.std_resid, dtype=np.float64)
        else:
            std_resid = returns / np.maximum(sigma, 1e-12)

        n_panels = 3
        scale = np.sqrt(252) if annualize else 1.0
        sigma_scaled = sigma * scale

        # Confidence interval multiplier
        from scipy import stats

        z_ci = stats.norm.ppf(0.5 + ci / 2)

        t_len = len(returns)
        t_axis = np.arange(t_len)

        fig, axes = plt.subplots(n_panels, 1, figsize=fig_size, sharex=True)

        # Panel 1: Returns
        ax1 = axes[0]
        ax1.plot(
            t_axis,
            returns,
            color=theme.colors.get("returns", "#7f7f7f"),
            linewidth=theme.line_widths.get("secondary", 0.8),
            alpha=0.7,
        )
        ax1.axhline(
            y=0,
            color=theme.colors.get("grid", "#cccccc"),
            linewidth=theme.line_widths.get("grid", 0.5),
        )
        ax1.set_ylabel("Returns")
        ax1.set_title(title or "Conditional Volatility Analysis")

        # Panel 2: Conditional Volatility
        ax2 = axes[1]
        ax2.plot(
            t_axis,
            sigma_scaled,
            color=theme.colors.get("volatility", "#2e75b6"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label=r"$\sigma_t$",
        )

        # Returns overlay in gray
        ax2.fill_between(
            t_axis,
            -np.abs(returns) * scale,
            np.abs(returns) * scale,
            color=theme.colors.get("returns", "#7f7f7f"),
            alpha=0.15,
            label="Returns",
        )

        # Confidence bands
        upper = sigma_scaled * z_ci
        lower = -sigma_scaled * z_ci
        ax2.fill_between(
            t_axis,
            lower,
            upper,
            color=theme.colors.get("confidence_band", "#2e75b6"),
            alpha=0.1,
            label=f"{ci:.0%} CI",
        )

        ylabel = "Annualized Volatility" if annualize else "Conditional Volatility"
        ax2.set_ylabel(ylabel)
        ax2.legend(loc="upper right", framealpha=0.8)

        # Panel 3: Standardized Residuals
        ax3 = axes[2]
        ax3.plot(
            t_axis,
            std_resid,
            color=theme.colors.get("residuals", "#548235"),
            linewidth=theme.line_widths.get("secondary", 0.8),
            alpha=0.7,
        )
        ax3.axhline(
            y=2,
            color=theme.colors.get("accent", "#c00000"),
            linestyle="--",
            linewidth=0.8,
            alpha=0.6,
        )
        ax3.axhline(
            y=-2,
            color=theme.colors.get("accent", "#c00000"),
            linestyle="--",
            linewidth=0.8,
            alpha=0.6,
        )
        ax3.axhline(
            y=0,
            color=theme.colors.get("grid", "#cccccc"),
            linewidth=theme.line_widths.get("grid", 0.5),
        )
        ax3.set_ylabel("Standardized Residuals")
        ax3.set_xlabel("Observation")

        fig.tight_layout()
        return fig


def plot_variance_persistence(
    results: Any,
    max_lags: int = 50,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
) -> Figure:
    """Plot variance persistence via autocorrelation analysis.

    Shows autocorrelation of squared returns with fitted GARCH ACF overlay
    and displays the half-life of volatility shocks.

    Parameters
    ----------
    results : ArchResults
        Fitted model results.
    max_lags : int
        Maximum number of lags for ACF.
    theme : str or Theme
        Visual theme name or Theme instance.
    figsize : tuple, optional
        Figure size override.

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

        resids: NDArray[np.float64] = np.asarray(results.resid, dtype=np.float64)
        resids2 = resids**2
        resids2_demean = resids2 - np.mean(resids2)

        # Compute empirical ACF
        t_len = len(resids2)
        acf_vals = np.zeros(max_lags + 1)
        var_r2 = np.var(resids2)
        for lag in range(max_lags + 1):
            if lag == 0:
                acf_vals[lag] = 1.0
            else:
                cov = np.mean(resids2_demean[lag:] * resids2_demean[:-lag])
                acf_vals[lag] = cov / var_r2 if var_r2 > 0 else 0.0

        # Compute theoretical GARCH ACF if persistence available
        persistence = getattr(results, "persistence", None)
        if persistence is not None and 0 < persistence < 1:
            theoretical_acf = persistence ** np.arange(max_lags + 1)
            half_life = np.log(0.5) / np.log(persistence)
        else:
            theoretical_acf = None
            half_life = None

        # Significance bounds
        sig_bound = 1.96 / np.sqrt(t_len)

        fig, ax = plt.subplots(1, 1, figsize=fig_size)
        lags = np.arange(max_lags + 1)

        # Empirical ACF as bars
        ax.bar(
            lags,
            acf_vals,
            color=theme.colors.get("primary", "#1f4e79"),
            alpha=0.6,
            width=0.8,
            label=r"ACF($r^2$)",
        )

        # Theoretical ACF overlay
        if theoretical_acf is not None:
            ax.plot(
                lags,
                theoretical_acf,
                color=theme.colors.get("accent", "#c00000"),
                linewidth=theme.line_widths.get("primary", 1.5),
                linestyle="--",
                label="GARCH Fitted ACF",
            )

        # Significance bounds
        ax.axhline(
            y=sig_bound, color=theme.colors.get("grid", "#cccccc"), linestyle=":", linewidth=0.8
        )
        ax.axhline(
            y=-sig_bound, color=theme.colors.get("grid", "#cccccc"), linestyle=":", linewidth=0.8
        )

        ax.set_xlabel("Lag")
        ax.set_ylabel("Autocorrelation")
        ax.set_title("Variance Persistence: ACF of Squared Returns")
        ax.legend(loc="upper right", framealpha=0.8)

        if half_life is not None:
            ax.annotate(
                f"Half-life: {half_life:.1f} obs",
                xy=(0.95, 0.85),
                xycoords="axes fraction",
                ha="right",
                fontsize=theme.font_sizes.get("annotation", 9),
                bbox={"boxstyle": "round,pad=0.3", "facecolor": "wheat", "alpha": 0.5},
            )

        fig.tight_layout()
        return fig
