"""Distribution fit visualization for archbox.

Provides 2x2 panel for assessing distribution fit quality:
histogram, QQ-plot, tail comparison, and CDF comparison.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import stats

from archbox.visualization.themes import Theme, get_theme


def plot_distribution_fit(
    results: Any,
    dist_name: str = "normal",
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot distribution fit diagnostic panel (2x2).

    Creates 4 subplots:
    1. Histogram of standardized residuals + fitted distribution
    2. QQ-plot against estimated distribution
    3. Tail comparison (log-scale): left tail empirical vs fitted
    4. CDF comparison: empirical vs fitted

    Parameters
    ----------
    results : ArchResults
        Fitted model results.
    dist_name : str
        Distribution to fit: 'normal', 'studentt', 'skewt'.
    theme : str or Theme
        Visual theme.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom suptitle.

    Returns
    -------
    matplotlib.figure.Figure
        The generated 2x2 figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size

        # Get standardized residuals
        if hasattr(results, "std_resid") and results.std_resid is not None:
            z: NDArray[np.float64] = np.asarray(results.std_resid, dtype=np.float64)
        else:
            resid = np.asarray(results.resid, dtype=np.float64)
            sigma = np.asarray(results.conditional_volatility, dtype=np.float64)
            z = resid / np.maximum(sigma, 1e-12)

        # Fit distribution
        fitted_dist = _fit_distribution(z, dist_name)

        fig, axes = plt.subplots(2, 2, figsize=fig_size)

        # --- Panel 1: Histogram + Fitted PDF ---
        ax1 = axes[0, 0]
        ax1.hist(
            z,
            bins=60,
            density=True,
            color=theme.colors.get("primary", "#1f4e79"),
            alpha=0.5,
            edgecolor="white",
            linewidth=0.3,
            label="Empirical",
        )

        x_range = np.linspace(z.min() - 1, z.max() + 1, 300)
        ax1.plot(
            x_range,
            fitted_dist.pdf(x_range),
            color=theme.colors.get("accent", "#c00000"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label=f"Fitted ({dist_name})",
        )

        # Normal reference
        ax1.plot(
            x_range,
            stats.norm.pdf(x_range),
            color=theme.colors.get("grid", "#cccccc"),
            linewidth=theme.line_widths.get("secondary", 0.8),
            linestyle="--",
            label="Normal",
        )

        ax1.set_title("Histogram + Fitted Distribution")
        ax1.set_xlabel(r"$z_t$")
        ax1.set_ylabel("Density")
        ax1.legend(loc="upper right", fontsize=8, framealpha=0.8)

        # --- Panel 2: QQ-Plot ---
        ax2 = axes[0, 1]
        sorted_z = np.sort(z)
        n = len(sorted_z)
        probs = (np.arange(1, n + 1) - 0.5) / n
        theoretical_q = fitted_dist.ppf(probs)

        ax2.scatter(
            theoretical_q,
            sorted_z,
            color=theme.colors.get("primary", "#1f4e79"),
            s=6,
            alpha=0.4,
            edgecolors="none",
        )

        q_min = min(theoretical_q.min(), sorted_z.min())
        q_max = max(theoretical_q.max(), sorted_z.max())
        ax2.plot(
            [q_min, q_max],
            [q_min, q_max],
            color=theme.colors.get("accent", "#c00000"),
            linewidth=1.0,
            linestyle="--",
        )

        ax2.set_title(f"QQ-Plot ({dist_name})")
        ax2.set_xlabel("Theoretical Quantiles")
        ax2.set_ylabel("Sample Quantiles")

        # --- Panel 3: Tail Comparison (log-scale) ---
        ax3 = axes[1, 0]
        # Left tail: P(Z <= z) for z < 0
        left_mask = sorted_z < 0
        if np.sum(left_mask) > 10:
            z_left = sorted_z[left_mask]
            empirical_cdf_left = np.arange(1, len(z_left) + 1) / n
            fitted_cdf_left = fitted_dist.cdf(z_left)

            ax3.semilogy(
                z_left,
                empirical_cdf_left,
                color=theme.colors.get("primary", "#1f4e79"),
                linewidth=theme.line_widths.get("primary", 1.5),
                label="Empirical",
            )
            ax3.semilogy(
                z_left,
                fitted_cdf_left,
                color=theme.colors.get("accent", "#c00000"),
                linewidth=theme.line_widths.get("primary", 1.5),
                linestyle="--",
                label=f"Fitted ({dist_name})",
            )
            ax3.semilogy(
                z_left,
                stats.norm.cdf(z_left),
                color=theme.colors.get("grid", "#cccccc"),
                linewidth=theme.line_widths.get("secondary", 0.8),
                linestyle=":",
                label="Normal",
            )

        ax3.set_title("Left Tail Comparison")
        ax3.set_xlabel(r"$z_t$")
        ax3.set_ylabel("P(Z \u2264 z) [log scale]")
        ax3.legend(loc="upper left", fontsize=8, framealpha=0.8)

        # --- Panel 4: CDF Comparison ---
        ax4 = axes[1, 1]
        empirical_cdf = np.arange(1, n + 1) / n
        fitted_cdf = fitted_dist.cdf(sorted_z)

        ax4.plot(
            sorted_z,
            empirical_cdf,
            color=theme.colors.get("primary", "#1f4e79"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label="Empirical CDF",
        )
        ax4.plot(
            sorted_z,
            fitted_cdf,
            color=theme.colors.get("accent", "#c00000"),
            linewidth=theme.line_widths.get("primary", 1.5),
            linestyle="--",
            label=f"Fitted ({dist_name})",
        )

        ax4.set_title("CDF Comparison")
        ax4.set_xlabel(r"$z_t$")
        ax4.set_ylabel("Cumulative Probability")
        ax4.legend(loc="lower right", fontsize=8, framealpha=0.8)

        fig.suptitle(
            title or "Distribution Fit Analysis",
            fontsize=theme.font_sizes.get("title", 14),
            y=1.02,
        )
        fig.tight_layout()
        return fig


def _fit_distribution(z: NDArray[np.float64], dist_name: str) -> Any:
    """Fit a distribution to standardized residuals.

    Parameters
    ----------
    z : ndarray
        Standardized residuals.
    dist_name : str
        Distribution name.

    Returns
    -------
    scipy.stats.rv_frozen
        Fitted distribution object.
    """
    if dist_name == "normal":
        loc, scale = stats.norm.fit(z)
        return stats.norm(loc=loc, scale=scale)
    elif dist_name == "studentt":
        df, loc, scale = stats.t.fit(z)
        return stats.t(df=df, loc=loc, scale=scale)
    elif dist_name == "skewt":
        # Use skewnorm as approximation for skew-t
        a, loc, scale = stats.skewnorm.fit(z)
        return stats.skewnorm(a=a, loc=loc, scale=scale)
    else:
        msg = f"Unknown distribution: {dist_name}. Use 'normal', 'studentt', 'skewt'."
        raise ValueError(msg)
