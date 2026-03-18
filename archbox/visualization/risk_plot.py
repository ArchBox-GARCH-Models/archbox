"""Risk management visualization for archbox.

Provides plots for VaR backtesting, traffic light assessment,
and comparison of different VaR estimation methods.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from archbox.visualization.themes import Theme, get_theme


def plot_var_backtest(
    backtest_results: Any,
    theme: str | Theme = "risk",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot VaR backtest: returns + VaR line + violations.

    Parameters
    ----------
    backtest_results : BacktestResults
        Results with:
        - returns: (T,) realized returns
        - var: (T,) Value-at-Risk series
        - es: (T,) Expected Shortfall series (optional)
        - violations: (T,) boolean mask of VaR violations
        - confidence_level: float (e.g. 0.99)
    theme : str or Theme
        Visual theme (defaults to 'risk').
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

        returns = np.asarray(backtest_results.returns, dtype=np.float64)
        var = np.asarray(backtest_results.var, dtype=np.float64)
        violations = np.asarray(backtest_results.violations, dtype=bool)
        cl = getattr(backtest_results, "confidence_level", 0.99)

        n_obs = len(returns)
        t_axis = np.arange(n_obs)

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        # Returns
        ax.plot(
            t_axis,
            returns,
            color=theme.colors.get("returns", "#7f7f7f"),
            linewidth=theme.line_widths.get("secondary", 0.8),
            alpha=0.7,
            label="Returns",
        )

        # VaR line
        ax.plot(
            t_axis,
            var,
            color=theme.colors.get("var_line", "#c00000"),
            linewidth=theme.line_widths.get("primary", 1.5),
            label=f"VaR ({cl:.0%})",
        )

        # ES line (if available)
        if hasattr(backtest_results, "es") and backtest_results.es is not None:
            es = np.asarray(backtest_results.es, dtype=np.float64)
            ax.plot(
                t_axis,
                es,
                color=theme.colors.get("es_line", "#ff6600"),
                linewidth=theme.line_widths.get("secondary", 1.0),
                linestyle="--",
                label="ES",
            )

        # Violations (marked as red circles)
        violation_idx = np.where(violations)[0]
        if len(violation_idx) > 0:
            ax.scatter(
                violation_idx,
                returns[violations],
                color=theme.colors.get("negative", "#c00000"),
                s=30,
                zorder=5,
                marker="o",
                edgecolors="white",
                linewidths=0.5,
                label=f"Violations ({len(violation_idx)})",
            )

        ax.axhline(y=0, color=theme.colors.get("grid", "#cccccc"), linewidth=0.5)

        n_violations = int(np.sum(violations))
        expected = n_obs * (1 - cl)
        ratio = n_violations / expected if expected > 0 else 0

        ax.set_xlabel("Observation")
        ax.set_ylabel("Return / VaR")
        ax.set_title(
            title
            or f"VaR Backtest (Violations: {n_violations}, "
            f"Expected: {expected:.1f}, Ratio: {ratio:.2f})"
        )
        ax.legend(loc="lower left", framealpha=0.8)

        fig.tight_layout()
        return fig


def plot_traffic_light(
    backtest_results: Any,
    window: int = 250,
    theme: str | Theme = "risk",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot traffic light test with rolling violation count.

    Parameters
    ----------
    backtest_results : BacktestResults
        Results with violations and confidence_level.
    window : int
        Rolling window size (default 250 ~ 1 year).
    theme : str or Theme
        Visual theme.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom title.

    Returns
    -------
    matplotlib.figure.Figure
        Traffic light figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size

        violations = np.asarray(backtest_results.violations, dtype=np.float64)
        cl = getattr(backtest_results, "confidence_level", 0.99)

        # Rolling violation count
        rolling_count = np.convolve(violations, np.ones(window), mode="valid")
        t_axis = np.arange(len(rolling_count)) + window - 1

        # Traffic light zones (Basel II guidelines for 99% VaR, 250 obs window)
        expected = window * (1 - cl)
        green_upper = expected * 1.5  # green zone
        yellow_upper = expected * 2.5  # yellow zone
        # above yellow = red

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        # Shaded zones
        zone_green = theme.colors.get("zone_green", theme.colors.get("positive", "#548235"))
        zone_yellow = theme.colors.get("zone_yellow", theme.colors.get("secondary", "#ffc000"))
        zone_red = theme.colors.get("zone_red", theme.colors.get("negative", "#c00000"))

        ax.axhspan(0, green_upper, color=zone_green, alpha=0.1)
        ax.axhspan(green_upper, yellow_upper, color=zone_yellow, alpha=0.1)
        ax.axhspan(
            yellow_upper,
            max(rolling_count.max() * 1.1, yellow_upper + 2),
            color=zone_red,
            alpha=0.1,
        )

        # Rolling count line
        ax.plot(
            t_axis,
            rolling_count,
            color=theme.colors.get("primary", "#1f4e79"),
            linewidth=theme.line_widths.get("primary", 1.5),
        )

        # Zone boundaries
        ax.axhline(
            y=green_upper,
            color=zone_green,
            linewidth=0.8,
            linestyle="--",
            alpha=0.6,
            label="Green/Yellow",
        )
        ax.axhline(
            y=yellow_upper,
            color=zone_red,
            linewidth=0.8,
            linestyle="--",
            alpha=0.6,
            label="Yellow/Red",
        )
        ax.axhline(
            y=expected,
            color=theme.colors.get("grid", "#cccccc"),
            linewidth=0.7,
            linestyle=":",
            label=f"Expected ({expected:.1f})",
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel(f"Violations (rolling {window})")
        ax.set_title(title or "Traffic Light Test")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def plot_var_comparison(
    var_dict: dict[str, NDArray[np.float64]],
    returns: NDArray[np.float64],
    theme: str | Theme = "risk",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    """Plot multiple VaR methods for comparison.

    Parameters
    ----------
    var_dict : dict
        Dictionary mapping method name to VaR series.
        E.g. {'Parametric': var_param, 'HS': var_hs, 'FHS': var_fhs}
    returns : ndarray
        Realized returns.
    theme : str or Theme
        Visual theme.
    figsize : tuple, optional
        Figure size override.
    title : str, optional
        Custom title.

    Returns
    -------
    matplotlib.figure.Figure
        Comparison figure.
    """
    if isinstance(theme, str):
        theme = get_theme(theme)

    rc_params = theme.to_matplotlib_rcparams()
    with plt.rc_context(rc_params):
        fig_size = figsize or theme.figure_size

        returns_arr = np.asarray(returns, dtype=np.float64)
        n_obs = len(returns_arr)
        t_axis = np.arange(n_obs)

        color_cycle = [
            theme.colors.get("var_line", "#c00000"),
            theme.colors.get("primary", "#1f4e79"),
            theme.colors.get("positive", "#548235"),
            theme.colors.get("secondary", "#ffc000"),
        ]
        linestyles = ["-", "--", "-.", ":"]

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        # Returns in background
        ax.fill_between(
            t_axis,
            returns_arr,
            0,
            color=theme.colors.get("returns", "#7f7f7f"),
            alpha=0.15,
        )
        ax.plot(
            t_axis,
            returns_arr,
            color=theme.colors.get("returns", "#7f7f7f"),
            linewidth=0.5,
            alpha=0.4,
        )

        # VaR lines
        for idx, (name, var_series) in enumerate(var_dict.items()):
            var_arr = np.asarray(var_series, dtype=np.float64)
            color = color_cycle[idx % len(color_cycle)]
            ls = linestyles[idx % len(linestyles)]
            ax.plot(
                t_axis[: len(var_arr)],
                var_arr,
                color=color,
                linewidth=theme.line_widths.get("primary", 1.5),
                linestyle=ls,
                label=name,
            )

        ax.axhline(y=0, color=theme.colors.get("grid", "#cccccc"), linewidth=0.5)

        ax.set_xlabel("Observation")
        ax.set_ylabel("Return / VaR")
        ax.set_title(title or "VaR Method Comparison")
        ax.legend(loc="lower left", framealpha=0.8)

        fig.tight_layout()
        return fig
