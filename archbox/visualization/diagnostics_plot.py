"""Diagnostic plots for archbox model validation.

Provides a standard 2x2 diagnostic panel:
1. Top-left: Standardized residuals z_t vs time
2. Top-right: ACF of z^2_t with significance limits
3. Bottom-left: QQ-plot of z_t
4. Bottom-right: Histogram of z_t with fitted curve
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import stats

from archbox.visualization.themes import Theme, get_theme


def plot_diagnostics(
    results: Any,
    max_lags: int = 30,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot diagnostic panel (2x2).

    Creates a standard model diagnostic panel:
    1. Top-left: Standardized residuals z_t vs time
    2. Top-right: ACF of z^2_t with significance limits
    3. Bottom-left: QQ-plot of z_t
    4. Bottom-right: Histogram of z_t with fitted distribution

    Parameters
    ----------
    results : ArchResults
        Fitted model results containing std_resid or resid and
        conditional_volatility attributes.
    max_lags : int
        Maximum number of lags for ACF computation.
    theme : str or Theme
        Visual theme name or Theme instance.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom suptitle.

    Returns
    -------
    matplotlib.figure.Figure
        The generated 2x2 diagnostic figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size

        # Extract standardized residuals
        if hasattr(results, "std_resid") and results.std_resid is not None:
            z: NDArray[np.float64] = np.asarray(results.std_resid, dtype=np.float64)
        else:
            resid = np.asarray(results.resid, dtype=np.float64)
            sigma = np.asarray(results.conditional_volatility, dtype=np.float64)
            z = resid / np.maximum(sigma, 1e-12)

        n_obs = len(z)
        z2 = z**2

        fig, axes = plt.subplots(2, 2, figsize=fig_size)

        # --- Panel 1: Standardized Residuals ---
        ax1 = axes[0, 0]
        t_axis = np.arange(n_obs)
        ax1.plot(
            t_axis,
            z,
            color=theme.colors.get("primary", "#1f4e79"),
            linewidth=theme.line_widths.get("secondary", 0.8),
            alpha=0.7,
        )
        ax1.axhline(y=0, color=theme.colors.get("grid", "#cccccc"), linewidth=0.5)
        ax1.axhline(
            y=2,
            color=theme.colors.get("accent", "#c00000"),
            linestyle="--",
            linewidth=0.7,
            alpha=0.5,
        )
        ax1.axhline(
            y=-2,
            color=theme.colors.get("accent", "#c00000"),
            linestyle="--",
            linewidth=0.7,
            alpha=0.5,
        )
        ax1.set_title("Standardized Residuals")
        ax1.set_xlabel("Observation")
        ax1.set_ylabel(r"$z_t$")

        # --- Panel 2: ACF of z^2 ---
        ax2 = axes[0, 1]
        z2_demean = z2 - np.mean(z2)
        var_z2 = np.var(z2)
        acf_vals = np.zeros(max_lags)
        for lag in range(1, max_lags + 1):
            cov = np.mean(z2_demean[lag:] * z2_demean[:-lag])
            acf_vals[lag - 1] = cov / var_z2 if var_z2 > 0 else 0.0

        lags = np.arange(1, max_lags + 1)
        ax2.bar(
            lags,
            acf_vals,
            color=theme.colors.get("primary", "#1f4e79"),
            alpha=0.7,
            width=0.8,
        )
        sig_bound = 1.96 / np.sqrt(n_obs)
        ax2.axhline(
            y=sig_bound,
            color=theme.colors.get("accent", "#c00000"),
            linestyle="--",
            linewidth=0.7,
        )
        ax2.axhline(
            y=-sig_bound,
            color=theme.colors.get("accent", "#c00000"),
            linestyle="--",
            linewidth=0.7,
        )
        ax2.set_title(r"ACF of $z_t^2$")
        ax2.set_xlabel("Lag")
        ax2.set_ylabel("ACF")

        # --- Panel 3: QQ-Plot ---
        ax3 = axes[1, 0]
        sorted_z = np.sort(z)
        n = len(sorted_z)
        theoretical_q = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
        ax3.scatter(
            theoretical_q,
            sorted_z,
            color=theme.colors.get("primary", "#1f4e79"),
            s=8,
            alpha=0.5,
            edgecolors="none",
        )
        # 45-degree reference line
        q_min = min(theoretical_q.min(), sorted_z.min())
        q_max = max(theoretical_q.max(), sorted_z.max())
        ax3.plot(
            [q_min, q_max],
            [q_min, q_max],
            color=theme.colors.get("accent", "#c00000"),
            linewidth=1.0,
            linestyle="--",
        )
        ax3.set_title("QQ-Plot (Normal)")
        ax3.set_xlabel("Theoretical Quantiles")
        ax3.set_ylabel("Sample Quantiles")

        # --- Panel 4: Histogram ---
        ax4 = axes[1, 1]
        ax4.hist(
            z,
            bins=50,
            density=True,
            color=theme.colors.get("primary", "#1f4e79"),
            alpha=0.6,
            edgecolor="white",
            linewidth=0.3,
        )
        # Overlay fitted normal
        x_range = np.linspace(z.min() - 0.5, z.max() + 0.5, 200)
        ax4.plot(
            x_range,
            stats.norm.pdf(x_range, loc=np.mean(z), scale=np.std(z)),
            color=theme.colors.get("accent", "#c00000"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label="Normal Fit",
        )
        ax4.set_title("Histogram of Standardized Residuals")
        ax4.set_xlabel(r"$z_t$")
        ax4.set_ylabel("Density")
        ax4.legend(loc="upper right", framealpha=0.8)

        fig.suptitle(
            title or "Model Diagnostics",
            fontsize=theme.font_sizes.get("title", 14),
            y=1.02,
        )
        fig.tight_layout()
        return fig
