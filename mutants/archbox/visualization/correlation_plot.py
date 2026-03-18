"""Correlation visualization for multivariate GARCH models.

Provides plots for dynamic correlations (DCC), correlation heatmaps,
and covariance decomposition.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

from archbox.visualization.themes import Theme, get_theme

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


def plot_dynamic_correlation(
    results: Any,
    i: int = 0,
    j: int = 1,
    ccc_reference: bool = True,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    args = [results, i, j, ccc_reference, theme, figsize, title]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_plot_dynamic_correlation__mutmut_orig,
        x_plot_dynamic_correlation__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_plot_dynamic_correlation__mutmut_orig(
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


def x_plot_dynamic_correlation__mutmut_1(
    results: Any,
    i: int = 1,
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


def x_plot_dynamic_correlation__mutmut_2(
    results: Any,
    i: int = 0,
    j: int = 2,
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


def x_plot_dynamic_correlation__mutmut_3(
    results: Any,
    i: int = 0,
    j: int = 1,
    ccc_reference: bool = False,
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


def x_plot_dynamic_correlation__mutmut_4(
    results: Any,
    i: int = 0,
    j: int = 1,
    ccc_reference: bool = True,
    theme: str | Theme = "XXprofessionalXX",
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


def x_plot_dynamic_correlation__mutmut_5(
    results: Any,
    i: int = 0,
    j: int = 1,
    ccc_reference: bool = True,
    theme: str | Theme = "PROFESSIONAL",
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


def x_plot_dynamic_correlation__mutmut_6(
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
        theme = None

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


def x_plot_dynamic_correlation__mutmut_7(
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
        theme = get_theme(None)

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


def x_plot_dynamic_correlation__mutmut_8(
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

    rc_params = None
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


def x_plot_dynamic_correlation__mutmut_9(
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
    with plt.rc_context(None):
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


def x_plot_dynamic_correlation__mutmut_10(
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
        fig_size = None

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


def x_plot_dynamic_correlation__mutmut_11(
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
        fig_size = figsize and theme.figure_size

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


def x_plot_dynamic_correlation__mutmut_12(
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
        rho_t: NDArray[np.float64] = None
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


def x_plot_dynamic_correlation__mutmut_13(
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
        rho_t: NDArray[np.float64] = np.asarray(None, dtype=np.float64)
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


def x_plot_dynamic_correlation__mutmut_14(
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
        rho_t: NDArray[np.float64] = np.asarray(results.dynamic_correlations[:, i, j], dtype=None)
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


def x_plot_dynamic_correlation__mutmut_15(
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
        rho_t: NDArray[np.float64] = np.asarray(dtype=np.float64)
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


def x_plot_dynamic_correlation__mutmut_16(
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
            results.dynamic_correlations[:, i, j],
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


def x_plot_dynamic_correlation__mutmut_17(
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
        n_obs = None
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


def x_plot_dynamic_correlation__mutmut_18(
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
        t_axis = None

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


def x_plot_dynamic_correlation__mutmut_19(
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
        t_axis = np.arange(None)

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


def x_plot_dynamic_correlation__mutmut_20(
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

        fig, ax = None

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


def x_plot_dynamic_correlation__mutmut_21(
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

        fig, ax = plt.subplots(None, 1, figsize=fig_size)

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


def x_plot_dynamic_correlation__mutmut_22(
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

        fig, ax = plt.subplots(1, None, figsize=fig_size)

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


def x_plot_dynamic_correlation__mutmut_23(
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

        fig, ax = plt.subplots(1, 1, figsize=None)

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


def x_plot_dynamic_correlation__mutmut_24(
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

        fig, ax = plt.subplots(1, figsize=fig_size)

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


def x_plot_dynamic_correlation__mutmut_25(
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

        fig, ax = plt.subplots(1, figsize=fig_size)

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


def x_plot_dynamic_correlation__mutmut_26(
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

        fig, ax = plt.subplots(
            1,
            1,
        )

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


def x_plot_dynamic_correlation__mutmut_27(
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

        fig, ax = plt.subplots(2, 1, figsize=fig_size)

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


def x_plot_dynamic_correlation__mutmut_28(
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

        fig, ax = plt.subplots(1, 2, figsize=fig_size)

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


def x_plot_dynamic_correlation__mutmut_29(
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
            None,
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


def x_plot_dynamic_correlation__mutmut_30(
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
            None,
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


def x_plot_dynamic_correlation__mutmut_31(
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
            color=None,
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


def x_plot_dynamic_correlation__mutmut_32(
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
            linewidth=None,
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


def x_plot_dynamic_correlation__mutmut_33(
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
            label=None,
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


def x_plot_dynamic_correlation__mutmut_34(
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


def x_plot_dynamic_correlation__mutmut_35(
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


def x_plot_dynamic_correlation__mutmut_36(
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


def x_plot_dynamic_correlation__mutmut_37(
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


def x_plot_dynamic_correlation__mutmut_38(
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


def x_plot_dynamic_correlation__mutmut_39(
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
            color=theme.colors.get(None, "#1f4e79"),
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


def x_plot_dynamic_correlation__mutmut_40(
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
            color=theme.colors.get("primary", None),
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


def x_plot_dynamic_correlation__mutmut_41(
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
            color=theme.colors.get("#1f4e79"),
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


def x_plot_dynamic_correlation__mutmut_42(
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
            color=theme.colors.get(
                "primary",
            ),
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


def x_plot_dynamic_correlation__mutmut_43(
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
            color=theme.colors.get("XXprimaryXX", "#1f4e79"),
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


def x_plot_dynamic_correlation__mutmut_44(
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
            color=theme.colors.get("PRIMARY", "#1f4e79"),
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


def x_plot_dynamic_correlation__mutmut_45(
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
            color=theme.colors.get("primary", "XX#1f4e79XX"),
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


def x_plot_dynamic_correlation__mutmut_46(
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
            color=theme.colors.get("primary", "#1F4E79"),
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


def x_plot_dynamic_correlation__mutmut_47(
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
            linewidth=theme.line_widths.get(None, 1.5),
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


def x_plot_dynamic_correlation__mutmut_48(
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
            linewidth=theme.line_widths.get("primary", None),
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


def x_plot_dynamic_correlation__mutmut_49(
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
            linewidth=theme.line_widths.get(1.5),
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


def x_plot_dynamic_correlation__mutmut_50(
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
            linewidth=theme.line_widths.get(
                "primary",
            ),
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


def x_plot_dynamic_correlation__mutmut_51(
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
            linewidth=theme.line_widths.get("XXprimaryXX", 1.5),
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


def x_plot_dynamic_correlation__mutmut_52(
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
            linewidth=theme.line_widths.get("PRIMARY", 1.5),
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


def x_plot_dynamic_correlation__mutmut_53(
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
            linewidth=theme.line_widths.get("primary", 2.5),
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


def x_plot_dynamic_correlation__mutmut_54(
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
            label=r"XX$\rho_{ij,t}$ (DCC)XX",
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


def x_plot_dynamic_correlation__mutmut_55(
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
            label=r"$\rho_{ij,t}$ (dcc)",
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


def x_plot_dynamic_correlation__mutmut_56(
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
            label=r"$\rHO_{IJ,T}$ (DCC)",
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


def x_plot_dynamic_correlation__mutmut_57(
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
        rho_mean = None
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


def x_plot_dynamic_correlation__mutmut_58(
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
        rho_mean = float(None)
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


def x_plot_dynamic_correlation__mutmut_59(
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
        rho_mean = float(np.mean(None))
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


def x_plot_dynamic_correlation__mutmut_60(
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
        rho_std = None
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


def x_plot_dynamic_correlation__mutmut_61(
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
        rho_std = float(None)
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


def x_plot_dynamic_correlation__mutmut_62(
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
        rho_std = float(np.std(None))
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


def x_plot_dynamic_correlation__mutmut_63(
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
            None,
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


def x_plot_dynamic_correlation__mutmut_64(
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
            None,
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


def x_plot_dynamic_correlation__mutmut_65(
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
            None,
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


def x_plot_dynamic_correlation__mutmut_66(
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
            color=None,
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


def x_plot_dynamic_correlation__mutmut_67(
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
            alpha=None,
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


def x_plot_dynamic_correlation__mutmut_68(
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


def x_plot_dynamic_correlation__mutmut_69(
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


def x_plot_dynamic_correlation__mutmut_70(
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


def x_plot_dynamic_correlation__mutmut_71(
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


def x_plot_dynamic_correlation__mutmut_72(
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


def x_plot_dynamic_correlation__mutmut_73(
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
            rho_t + 1.96 * rho_std * 0.1,
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


def x_plot_dynamic_correlation__mutmut_74(
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
            rho_t - 1.96 * rho_std / 0.1,
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


def x_plot_dynamic_correlation__mutmut_75(
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
            rho_t - 1.96 / rho_std * 0.1,
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


def x_plot_dynamic_correlation__mutmut_76(
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
            rho_t - 2.96 * rho_std * 0.1,
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


def x_plot_dynamic_correlation__mutmut_77(
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
            rho_t - 1.96 * rho_std * 1.1,
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


def x_plot_dynamic_correlation__mutmut_78(
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
            rho_t - 1.96 * rho_std * 0.1,
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


def x_plot_dynamic_correlation__mutmut_79(
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
            rho_t + 1.96 * rho_std / 0.1,
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


def x_plot_dynamic_correlation__mutmut_80(
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
            rho_t + 1.96 / rho_std * 0.1,
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


def x_plot_dynamic_correlation__mutmut_81(
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
            rho_t + 2.96 * rho_std * 0.1,
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


def x_plot_dynamic_correlation__mutmut_82(
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
            rho_t + 1.96 * rho_std * 1.1,
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


def x_plot_dynamic_correlation__mutmut_83(
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
            color=theme.colors.get(None, "#2e75b6"),
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


def x_plot_dynamic_correlation__mutmut_84(
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
            color=theme.colors.get("confidence_band", None),
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


def x_plot_dynamic_correlation__mutmut_85(
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
            color=theme.colors.get("#2e75b6"),
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


def x_plot_dynamic_correlation__mutmut_86(
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
            color=theme.colors.get(
                "confidence_band",
            ),
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


def x_plot_dynamic_correlation__mutmut_87(
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
            color=theme.colors.get("XXconfidence_bandXX", "#2e75b6"),
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


def x_plot_dynamic_correlation__mutmut_88(
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
            color=theme.colors.get("CONFIDENCE_BAND", "#2e75b6"),
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


def x_plot_dynamic_correlation__mutmut_89(
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
            color=theme.colors.get("confidence_band", "XX#2e75b6XX"),
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


def x_plot_dynamic_correlation__mutmut_90(
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
            color=theme.colors.get("confidence_band", "#2E75B6"),
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


def x_plot_dynamic_correlation__mutmut_91(
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
            alpha=1.1,
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


def x_plot_dynamic_correlation__mutmut_92(
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
                y=None,
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


def x_plot_dynamic_correlation__mutmut_93(
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
                color=None,
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


def x_plot_dynamic_correlation__mutmut_94(
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
                linewidth=None,
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


def x_plot_dynamic_correlation__mutmut_95(
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
                linestyle=None,
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


def x_plot_dynamic_correlation__mutmut_96(
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
                label=None,
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


def x_plot_dynamic_correlation__mutmut_97(
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


def x_plot_dynamic_correlation__mutmut_98(
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


def x_plot_dynamic_correlation__mutmut_99(
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


def x_plot_dynamic_correlation__mutmut_100(
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


def x_plot_dynamic_correlation__mutmut_101(
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


def x_plot_dynamic_correlation__mutmut_102(
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
                color=theme.colors.get(None, "#c00000"),
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


def x_plot_dynamic_correlation__mutmut_103(
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
                color=theme.colors.get("accent", None),
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


def x_plot_dynamic_correlation__mutmut_104(
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
                color=theme.colors.get("#c00000"),
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


def x_plot_dynamic_correlation__mutmut_105(
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
                color=theme.colors.get(
                    "accent",
                ),
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


def x_plot_dynamic_correlation__mutmut_106(
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
                color=theme.colors.get("XXaccentXX", "#c00000"),
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


def x_plot_dynamic_correlation__mutmut_107(
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
                color=theme.colors.get("ACCENT", "#c00000"),
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


def x_plot_dynamic_correlation__mutmut_108(
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
                color=theme.colors.get("accent", "XX#c00000XX"),
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


def x_plot_dynamic_correlation__mutmut_109(
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
                color=theme.colors.get("accent", "#C00000"),
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


def x_plot_dynamic_correlation__mutmut_110(
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
                linewidth=theme.line_widths.get(None, 1.0),
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


def x_plot_dynamic_correlation__mutmut_111(
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
                linewidth=theme.line_widths.get("secondary", None),
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


def x_plot_dynamic_correlation__mutmut_112(
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
                linewidth=theme.line_widths.get(1.0),
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


def x_plot_dynamic_correlation__mutmut_113(
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
                linewidth=theme.line_widths.get(
                    "secondary",
                ),
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


def x_plot_dynamic_correlation__mutmut_114(
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
                linewidth=theme.line_widths.get("XXsecondaryXX", 1.0),
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


def x_plot_dynamic_correlation__mutmut_115(
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
                linewidth=theme.line_widths.get("SECONDARY", 1.0),
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


def x_plot_dynamic_correlation__mutmut_116(
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
                linewidth=theme.line_widths.get("secondary", 2.0),
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


def x_plot_dynamic_correlation__mutmut_117(
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
                linestyle="XX--XX",
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


def x_plot_dynamic_correlation__mutmut_118(
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

        series_names = None
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_119(
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

        series_names = getattr(None, "series_names", [f"Series {i}", f"Series {j}"])
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_120(
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

        series_names = getattr(results, None, [f"Series {i}", f"Series {j}"])
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_121(
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

        series_names = getattr(results, "series_names", None)
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_122(
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

        series_names = getattr("series_names", [f"Series {i}", f"Series {j}"])
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_123(
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

        series_names = getattr(results, [f"Series {i}", f"Series {j}"])
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_124(
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

        series_names = results.series_names
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_125(
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

        series_names = getattr(results, "XXseries_namesXX", [f"Series {i}", f"Series {j}"])
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_126(
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

        series_names = getattr(results, "SERIES_NAMES", [f"Series {i}", f"Series {j}"])
        name_i = series_names[i] if i < len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_127(
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
        name_i = None
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_128(
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
        name_i = series_names[i] if i <= len(series_names) else f"Series {i}"
        name_j = series_names[j] if j < len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_129(
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
        name_j = None

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_130(
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
        name_j = series_names[j] if j <= len(series_names) else f"Series {j}"

        ax.set_xlabel("Observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_131(
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

        ax.set_xlabel(None)
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_132(
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

        ax.set_xlabel("XXObservationXX")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_133(
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

        ax.set_xlabel("observation")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_134(
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

        ax.set_xlabel("OBSERVATION")
        ax.set_ylabel("Correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_135(
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
        ax.set_ylabel(None)
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_136(
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
        ax.set_ylabel("XXCorrelationXX")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_137(
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
        ax.set_ylabel("correlation")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_138(
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
        ax.set_ylabel("CORRELATION")
        ax.set_title(title or f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_139(
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
        ax.set_title(None)
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_140(
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
        ax.set_title(title and f"Dynamic Correlation: {name_i} - {name_j}")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_141(
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
        ax.set_ylim(None, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_142(
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
        ax.set_ylim(-1.05, None)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_143(
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
        ax.set_ylim(1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_144(
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
        ax.set_ylim(
            -1.05,
        )
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_145(
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
        ax.set_ylim(+1.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_146(
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
        ax.set_ylim(-2.05, 1.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_147(
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
        ax.set_ylim(-1.05, 2.05)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_148(
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
        ax.legend(loc=None, framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_149(
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
        ax.legend(loc="upper right", framealpha=None)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_150(
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
        ax.legend(framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_151(
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
        ax.legend(
            loc="upper right",
        )

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_152(
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
        ax.legend(loc="XXupper rightXX", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_153(
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
        ax.legend(loc="UPPER RIGHT", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_dynamic_correlation__mutmut_154(
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
        ax.legend(loc="upper right", framealpha=1.8)

        fig.tight_layout()
        return fig


x_plot_dynamic_correlation__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_plot_dynamic_correlation__mutmut_1": x_plot_dynamic_correlation__mutmut_1,
    "x_plot_dynamic_correlation__mutmut_2": x_plot_dynamic_correlation__mutmut_2,
    "x_plot_dynamic_correlation__mutmut_3": x_plot_dynamic_correlation__mutmut_3,
    "x_plot_dynamic_correlation__mutmut_4": x_plot_dynamic_correlation__mutmut_4,
    "x_plot_dynamic_correlation__mutmut_5": x_plot_dynamic_correlation__mutmut_5,
    "x_plot_dynamic_correlation__mutmut_6": x_plot_dynamic_correlation__mutmut_6,
    "x_plot_dynamic_correlation__mutmut_7": x_plot_dynamic_correlation__mutmut_7,
    "x_plot_dynamic_correlation__mutmut_8": x_plot_dynamic_correlation__mutmut_8,
    "x_plot_dynamic_correlation__mutmut_9": x_plot_dynamic_correlation__mutmut_9,
    "x_plot_dynamic_correlation__mutmut_10": x_plot_dynamic_correlation__mutmut_10,
    "x_plot_dynamic_correlation__mutmut_11": x_plot_dynamic_correlation__mutmut_11,
    "x_plot_dynamic_correlation__mutmut_12": x_plot_dynamic_correlation__mutmut_12,
    "x_plot_dynamic_correlation__mutmut_13": x_plot_dynamic_correlation__mutmut_13,
    "x_plot_dynamic_correlation__mutmut_14": x_plot_dynamic_correlation__mutmut_14,
    "x_plot_dynamic_correlation__mutmut_15": x_plot_dynamic_correlation__mutmut_15,
    "x_plot_dynamic_correlation__mutmut_16": x_plot_dynamic_correlation__mutmut_16,
    "x_plot_dynamic_correlation__mutmut_17": x_plot_dynamic_correlation__mutmut_17,
    "x_plot_dynamic_correlation__mutmut_18": x_plot_dynamic_correlation__mutmut_18,
    "x_plot_dynamic_correlation__mutmut_19": x_plot_dynamic_correlation__mutmut_19,
    "x_plot_dynamic_correlation__mutmut_20": x_plot_dynamic_correlation__mutmut_20,
    "x_plot_dynamic_correlation__mutmut_21": x_plot_dynamic_correlation__mutmut_21,
    "x_plot_dynamic_correlation__mutmut_22": x_plot_dynamic_correlation__mutmut_22,
    "x_plot_dynamic_correlation__mutmut_23": x_plot_dynamic_correlation__mutmut_23,
    "x_plot_dynamic_correlation__mutmut_24": x_plot_dynamic_correlation__mutmut_24,
    "x_plot_dynamic_correlation__mutmut_25": x_plot_dynamic_correlation__mutmut_25,
    "x_plot_dynamic_correlation__mutmut_26": x_plot_dynamic_correlation__mutmut_26,
    "x_plot_dynamic_correlation__mutmut_27": x_plot_dynamic_correlation__mutmut_27,
    "x_plot_dynamic_correlation__mutmut_28": x_plot_dynamic_correlation__mutmut_28,
    "x_plot_dynamic_correlation__mutmut_29": x_plot_dynamic_correlation__mutmut_29,
    "x_plot_dynamic_correlation__mutmut_30": x_plot_dynamic_correlation__mutmut_30,
    "x_plot_dynamic_correlation__mutmut_31": x_plot_dynamic_correlation__mutmut_31,
    "x_plot_dynamic_correlation__mutmut_32": x_plot_dynamic_correlation__mutmut_32,
    "x_plot_dynamic_correlation__mutmut_33": x_plot_dynamic_correlation__mutmut_33,
    "x_plot_dynamic_correlation__mutmut_34": x_plot_dynamic_correlation__mutmut_34,
    "x_plot_dynamic_correlation__mutmut_35": x_plot_dynamic_correlation__mutmut_35,
    "x_plot_dynamic_correlation__mutmut_36": x_plot_dynamic_correlation__mutmut_36,
    "x_plot_dynamic_correlation__mutmut_37": x_plot_dynamic_correlation__mutmut_37,
    "x_plot_dynamic_correlation__mutmut_38": x_plot_dynamic_correlation__mutmut_38,
    "x_plot_dynamic_correlation__mutmut_39": x_plot_dynamic_correlation__mutmut_39,
    "x_plot_dynamic_correlation__mutmut_40": x_plot_dynamic_correlation__mutmut_40,
    "x_plot_dynamic_correlation__mutmut_41": x_plot_dynamic_correlation__mutmut_41,
    "x_plot_dynamic_correlation__mutmut_42": x_plot_dynamic_correlation__mutmut_42,
    "x_plot_dynamic_correlation__mutmut_43": x_plot_dynamic_correlation__mutmut_43,
    "x_plot_dynamic_correlation__mutmut_44": x_plot_dynamic_correlation__mutmut_44,
    "x_plot_dynamic_correlation__mutmut_45": x_plot_dynamic_correlation__mutmut_45,
    "x_plot_dynamic_correlation__mutmut_46": x_plot_dynamic_correlation__mutmut_46,
    "x_plot_dynamic_correlation__mutmut_47": x_plot_dynamic_correlation__mutmut_47,
    "x_plot_dynamic_correlation__mutmut_48": x_plot_dynamic_correlation__mutmut_48,
    "x_plot_dynamic_correlation__mutmut_49": x_plot_dynamic_correlation__mutmut_49,
    "x_plot_dynamic_correlation__mutmut_50": x_plot_dynamic_correlation__mutmut_50,
    "x_plot_dynamic_correlation__mutmut_51": x_plot_dynamic_correlation__mutmut_51,
    "x_plot_dynamic_correlation__mutmut_52": x_plot_dynamic_correlation__mutmut_52,
    "x_plot_dynamic_correlation__mutmut_53": x_plot_dynamic_correlation__mutmut_53,
    "x_plot_dynamic_correlation__mutmut_54": x_plot_dynamic_correlation__mutmut_54,
    "x_plot_dynamic_correlation__mutmut_55": x_plot_dynamic_correlation__mutmut_55,
    "x_plot_dynamic_correlation__mutmut_56": x_plot_dynamic_correlation__mutmut_56,
    "x_plot_dynamic_correlation__mutmut_57": x_plot_dynamic_correlation__mutmut_57,
    "x_plot_dynamic_correlation__mutmut_58": x_plot_dynamic_correlation__mutmut_58,
    "x_plot_dynamic_correlation__mutmut_59": x_plot_dynamic_correlation__mutmut_59,
    "x_plot_dynamic_correlation__mutmut_60": x_plot_dynamic_correlation__mutmut_60,
    "x_plot_dynamic_correlation__mutmut_61": x_plot_dynamic_correlation__mutmut_61,
    "x_plot_dynamic_correlation__mutmut_62": x_plot_dynamic_correlation__mutmut_62,
    "x_plot_dynamic_correlation__mutmut_63": x_plot_dynamic_correlation__mutmut_63,
    "x_plot_dynamic_correlation__mutmut_64": x_plot_dynamic_correlation__mutmut_64,
    "x_plot_dynamic_correlation__mutmut_65": x_plot_dynamic_correlation__mutmut_65,
    "x_plot_dynamic_correlation__mutmut_66": x_plot_dynamic_correlation__mutmut_66,
    "x_plot_dynamic_correlation__mutmut_67": x_plot_dynamic_correlation__mutmut_67,
    "x_plot_dynamic_correlation__mutmut_68": x_plot_dynamic_correlation__mutmut_68,
    "x_plot_dynamic_correlation__mutmut_69": x_plot_dynamic_correlation__mutmut_69,
    "x_plot_dynamic_correlation__mutmut_70": x_plot_dynamic_correlation__mutmut_70,
    "x_plot_dynamic_correlation__mutmut_71": x_plot_dynamic_correlation__mutmut_71,
    "x_plot_dynamic_correlation__mutmut_72": x_plot_dynamic_correlation__mutmut_72,
    "x_plot_dynamic_correlation__mutmut_73": x_plot_dynamic_correlation__mutmut_73,
    "x_plot_dynamic_correlation__mutmut_74": x_plot_dynamic_correlation__mutmut_74,
    "x_plot_dynamic_correlation__mutmut_75": x_plot_dynamic_correlation__mutmut_75,
    "x_plot_dynamic_correlation__mutmut_76": x_plot_dynamic_correlation__mutmut_76,
    "x_plot_dynamic_correlation__mutmut_77": x_plot_dynamic_correlation__mutmut_77,
    "x_plot_dynamic_correlation__mutmut_78": x_plot_dynamic_correlation__mutmut_78,
    "x_plot_dynamic_correlation__mutmut_79": x_plot_dynamic_correlation__mutmut_79,
    "x_plot_dynamic_correlation__mutmut_80": x_plot_dynamic_correlation__mutmut_80,
    "x_plot_dynamic_correlation__mutmut_81": x_plot_dynamic_correlation__mutmut_81,
    "x_plot_dynamic_correlation__mutmut_82": x_plot_dynamic_correlation__mutmut_82,
    "x_plot_dynamic_correlation__mutmut_83": x_plot_dynamic_correlation__mutmut_83,
    "x_plot_dynamic_correlation__mutmut_84": x_plot_dynamic_correlation__mutmut_84,
    "x_plot_dynamic_correlation__mutmut_85": x_plot_dynamic_correlation__mutmut_85,
    "x_plot_dynamic_correlation__mutmut_86": x_plot_dynamic_correlation__mutmut_86,
    "x_plot_dynamic_correlation__mutmut_87": x_plot_dynamic_correlation__mutmut_87,
    "x_plot_dynamic_correlation__mutmut_88": x_plot_dynamic_correlation__mutmut_88,
    "x_plot_dynamic_correlation__mutmut_89": x_plot_dynamic_correlation__mutmut_89,
    "x_plot_dynamic_correlation__mutmut_90": x_plot_dynamic_correlation__mutmut_90,
    "x_plot_dynamic_correlation__mutmut_91": x_plot_dynamic_correlation__mutmut_91,
    "x_plot_dynamic_correlation__mutmut_92": x_plot_dynamic_correlation__mutmut_92,
    "x_plot_dynamic_correlation__mutmut_93": x_plot_dynamic_correlation__mutmut_93,
    "x_plot_dynamic_correlation__mutmut_94": x_plot_dynamic_correlation__mutmut_94,
    "x_plot_dynamic_correlation__mutmut_95": x_plot_dynamic_correlation__mutmut_95,
    "x_plot_dynamic_correlation__mutmut_96": x_plot_dynamic_correlation__mutmut_96,
    "x_plot_dynamic_correlation__mutmut_97": x_plot_dynamic_correlation__mutmut_97,
    "x_plot_dynamic_correlation__mutmut_98": x_plot_dynamic_correlation__mutmut_98,
    "x_plot_dynamic_correlation__mutmut_99": x_plot_dynamic_correlation__mutmut_99,
    "x_plot_dynamic_correlation__mutmut_100": x_plot_dynamic_correlation__mutmut_100,
    "x_plot_dynamic_correlation__mutmut_101": x_plot_dynamic_correlation__mutmut_101,
    "x_plot_dynamic_correlation__mutmut_102": x_plot_dynamic_correlation__mutmut_102,
    "x_plot_dynamic_correlation__mutmut_103": x_plot_dynamic_correlation__mutmut_103,
    "x_plot_dynamic_correlation__mutmut_104": x_plot_dynamic_correlation__mutmut_104,
    "x_plot_dynamic_correlation__mutmut_105": x_plot_dynamic_correlation__mutmut_105,
    "x_plot_dynamic_correlation__mutmut_106": x_plot_dynamic_correlation__mutmut_106,
    "x_plot_dynamic_correlation__mutmut_107": x_plot_dynamic_correlation__mutmut_107,
    "x_plot_dynamic_correlation__mutmut_108": x_plot_dynamic_correlation__mutmut_108,
    "x_plot_dynamic_correlation__mutmut_109": x_plot_dynamic_correlation__mutmut_109,
    "x_plot_dynamic_correlation__mutmut_110": x_plot_dynamic_correlation__mutmut_110,
    "x_plot_dynamic_correlation__mutmut_111": x_plot_dynamic_correlation__mutmut_111,
    "x_plot_dynamic_correlation__mutmut_112": x_plot_dynamic_correlation__mutmut_112,
    "x_plot_dynamic_correlation__mutmut_113": x_plot_dynamic_correlation__mutmut_113,
    "x_plot_dynamic_correlation__mutmut_114": x_plot_dynamic_correlation__mutmut_114,
    "x_plot_dynamic_correlation__mutmut_115": x_plot_dynamic_correlation__mutmut_115,
    "x_plot_dynamic_correlation__mutmut_116": x_plot_dynamic_correlation__mutmut_116,
    "x_plot_dynamic_correlation__mutmut_117": x_plot_dynamic_correlation__mutmut_117,
    "x_plot_dynamic_correlation__mutmut_118": x_plot_dynamic_correlation__mutmut_118,
    "x_plot_dynamic_correlation__mutmut_119": x_plot_dynamic_correlation__mutmut_119,
    "x_plot_dynamic_correlation__mutmut_120": x_plot_dynamic_correlation__mutmut_120,
    "x_plot_dynamic_correlation__mutmut_121": x_plot_dynamic_correlation__mutmut_121,
    "x_plot_dynamic_correlation__mutmut_122": x_plot_dynamic_correlation__mutmut_122,
    "x_plot_dynamic_correlation__mutmut_123": x_plot_dynamic_correlation__mutmut_123,
    "x_plot_dynamic_correlation__mutmut_124": x_plot_dynamic_correlation__mutmut_124,
    "x_plot_dynamic_correlation__mutmut_125": x_plot_dynamic_correlation__mutmut_125,
    "x_plot_dynamic_correlation__mutmut_126": x_plot_dynamic_correlation__mutmut_126,
    "x_plot_dynamic_correlation__mutmut_127": x_plot_dynamic_correlation__mutmut_127,
    "x_plot_dynamic_correlation__mutmut_128": x_plot_dynamic_correlation__mutmut_128,
    "x_plot_dynamic_correlation__mutmut_129": x_plot_dynamic_correlation__mutmut_129,
    "x_plot_dynamic_correlation__mutmut_130": x_plot_dynamic_correlation__mutmut_130,
    "x_plot_dynamic_correlation__mutmut_131": x_plot_dynamic_correlation__mutmut_131,
    "x_plot_dynamic_correlation__mutmut_132": x_plot_dynamic_correlation__mutmut_132,
    "x_plot_dynamic_correlation__mutmut_133": x_plot_dynamic_correlation__mutmut_133,
    "x_plot_dynamic_correlation__mutmut_134": x_plot_dynamic_correlation__mutmut_134,
    "x_plot_dynamic_correlation__mutmut_135": x_plot_dynamic_correlation__mutmut_135,
    "x_plot_dynamic_correlation__mutmut_136": x_plot_dynamic_correlation__mutmut_136,
    "x_plot_dynamic_correlation__mutmut_137": x_plot_dynamic_correlation__mutmut_137,
    "x_plot_dynamic_correlation__mutmut_138": x_plot_dynamic_correlation__mutmut_138,
    "x_plot_dynamic_correlation__mutmut_139": x_plot_dynamic_correlation__mutmut_139,
    "x_plot_dynamic_correlation__mutmut_140": x_plot_dynamic_correlation__mutmut_140,
    "x_plot_dynamic_correlation__mutmut_141": x_plot_dynamic_correlation__mutmut_141,
    "x_plot_dynamic_correlation__mutmut_142": x_plot_dynamic_correlation__mutmut_142,
    "x_plot_dynamic_correlation__mutmut_143": x_plot_dynamic_correlation__mutmut_143,
    "x_plot_dynamic_correlation__mutmut_144": x_plot_dynamic_correlation__mutmut_144,
    "x_plot_dynamic_correlation__mutmut_145": x_plot_dynamic_correlation__mutmut_145,
    "x_plot_dynamic_correlation__mutmut_146": x_plot_dynamic_correlation__mutmut_146,
    "x_plot_dynamic_correlation__mutmut_147": x_plot_dynamic_correlation__mutmut_147,
    "x_plot_dynamic_correlation__mutmut_148": x_plot_dynamic_correlation__mutmut_148,
    "x_plot_dynamic_correlation__mutmut_149": x_plot_dynamic_correlation__mutmut_149,
    "x_plot_dynamic_correlation__mutmut_150": x_plot_dynamic_correlation__mutmut_150,
    "x_plot_dynamic_correlation__mutmut_151": x_plot_dynamic_correlation__mutmut_151,
    "x_plot_dynamic_correlation__mutmut_152": x_plot_dynamic_correlation__mutmut_152,
    "x_plot_dynamic_correlation__mutmut_153": x_plot_dynamic_correlation__mutmut_153,
    "x_plot_dynamic_correlation__mutmut_154": x_plot_dynamic_correlation__mutmut_154,
}
x_plot_dynamic_correlation__mutmut_orig.__name__ = "x_plot_dynamic_correlation"


def plot_correlation_heatmap(
    results: Any,
    t: int | None = None,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    args = [results, t, theme, figsize, title]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_plot_correlation_heatmap__mutmut_orig,
        x_plot_correlation_heatmap__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_plot_correlation_heatmap__mutmut_orig(
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


def x_plot_correlation_heatmap__mutmut_1(
    results: Any,
    t: int | None = None,
    theme: str | Theme = "XXprofessionalXX",
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


def x_plot_correlation_heatmap__mutmut_2(
    results: Any,
    t: int | None = None,
    theme: str | Theme = "PROFESSIONAL",
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


def x_plot_correlation_heatmap__mutmut_3(
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
        theme = None

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


def x_plot_correlation_heatmap__mutmut_4(
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
        theme = get_theme(None)

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


def x_plot_correlation_heatmap__mutmut_5(
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

    rc_params = None
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


def x_plot_correlation_heatmap__mutmut_6(
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
    with plt.rc_context(None):
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


def x_plot_correlation_heatmap__mutmut_7(
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
        corr_matrices = None
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


def x_plot_correlation_heatmap__mutmut_8(
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
        corr_matrices = np.asarray(None, dtype=np.float64)
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


def x_plot_correlation_heatmap__mutmut_9(
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
        corr_matrices = np.asarray(results.dynamic_correlations, dtype=None)
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


def x_plot_correlation_heatmap__mutmut_10(
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
        corr_matrices = np.asarray(dtype=np.float64)
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


def x_plot_correlation_heatmap__mutmut_11(
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
        corr_matrices = np.asarray(
            results.dynamic_correlations,
        )
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


def x_plot_correlation_heatmap__mutmut_12(
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
        k = None

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


def x_plot_correlation_heatmap__mutmut_13(
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
        k = corr_matrices.shape[2]

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


def x_plot_correlation_heatmap__mutmut_14(
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

        if t is None:
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


def x_plot_correlation_heatmap__mutmut_15(
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
            corr_mat = None
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


def x_plot_correlation_heatmap__mutmut_16(
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
            subtitle = None
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


def x_plot_correlation_heatmap__mutmut_17(
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
            corr_mat = None
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


def x_plot_correlation_heatmap__mutmut_18(
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
            corr_mat = np.mean(None, axis=0)
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


def x_plot_correlation_heatmap__mutmut_19(
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
            corr_mat = np.mean(corr_matrices, axis=None)
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


def x_plot_correlation_heatmap__mutmut_20(
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
            corr_mat = np.mean(axis=0)
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


def x_plot_correlation_heatmap__mutmut_21(
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
            corr_mat = np.mean(
                corr_matrices,
            )
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


def x_plot_correlation_heatmap__mutmut_22(
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
            corr_mat = np.mean(corr_matrices, axis=1)
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


def x_plot_correlation_heatmap__mutmut_23(
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
            subtitle = None

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


def x_plot_correlation_heatmap__mutmut_24(
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
            subtitle = "XX(Mean)XX"

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


def x_plot_correlation_heatmap__mutmut_25(
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
            subtitle = "(mean)"

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


def x_plot_correlation_heatmap__mutmut_26(
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
            subtitle = "(MEAN)"

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


def x_plot_correlation_heatmap__mutmut_27(
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

        fig_size = None
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


def x_plot_correlation_heatmap__mutmut_28(
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

        fig_size = figsize and (max(6, k * 1.5), max(5, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_29(
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

        fig_size = figsize or (max(None, k * 1.5), max(5, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_30(
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

        fig_size = figsize or (max(6, None), max(5, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_31(
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

        fig_size = figsize or (max(k * 1.5), max(5, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_32(
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

        fig_size = figsize or (
            max(
                6,
            ),
            max(5, k * 1.3),
        )
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


def x_plot_correlation_heatmap__mutmut_33(
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

        fig_size = figsize or (max(7, k * 1.5), max(5, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_34(
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

        fig_size = figsize or (max(6, k / 1.5), max(5, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_35(
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

        fig_size = figsize or (max(6, k * 2.5), max(5, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_36(
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

        fig_size = figsize or (max(6, k * 1.5), max(None, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_37(
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

        fig_size = figsize or (max(6, k * 1.5), max(5, None))
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


def x_plot_correlation_heatmap__mutmut_38(
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

        fig_size = figsize or (max(6, k * 1.5), max(k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_39(
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

        fig_size = figsize or (
            max(6, k * 1.5),
            max(
                5,
            ),
        )
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


def x_plot_correlation_heatmap__mutmut_40(
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

        fig_size = figsize or (max(6, k * 1.5), max(6, k * 1.3))
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


def x_plot_correlation_heatmap__mutmut_41(
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

        fig_size = figsize or (max(6, k * 1.5), max(5, k / 1.3))
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


def x_plot_correlation_heatmap__mutmut_42(
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

        fig_size = figsize or (max(6, k * 1.5), max(5, k * 2.3))
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


def x_plot_correlation_heatmap__mutmut_43(
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
        fig, ax = None

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


def x_plot_correlation_heatmap__mutmut_44(
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
        fig, ax = plt.subplots(None, 1, figsize=fig_size)

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


def x_plot_correlation_heatmap__mutmut_45(
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
        fig, ax = plt.subplots(1, None, figsize=fig_size)

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


def x_plot_correlation_heatmap__mutmut_46(
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
        fig, ax = plt.subplots(1, 1, figsize=None)

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


def x_plot_correlation_heatmap__mutmut_47(
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
        fig, ax = plt.subplots(1, figsize=fig_size)

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


def x_plot_correlation_heatmap__mutmut_48(
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
        fig, ax = plt.subplots(1, figsize=fig_size)

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


def x_plot_correlation_heatmap__mutmut_49(
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
        fig, ax = plt.subplots(
            1,
            1,
        )

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


def x_plot_correlation_heatmap__mutmut_50(
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
        fig, ax = plt.subplots(2, 1, figsize=fig_size)

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


def x_plot_correlation_heatmap__mutmut_51(
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
        fig, ax = plt.subplots(1, 2, figsize=fig_size)

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


def x_plot_correlation_heatmap__mutmut_52(
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

        im = None
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


def x_plot_correlation_heatmap__mutmut_53(
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

        im = ax.imshow(None, cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_54(
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

        im = ax.imshow(corr_mat, cmap=None, vmin=-1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_55(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=None, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_56(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-1, vmax=None, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_57(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-1, vmax=1, aspect=None)
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


def x_plot_correlation_heatmap__mutmut_58(
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

        im = ax.imshow(cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_59(
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

        im = ax.imshow(corr_mat, vmin=-1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_60(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_61(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_62(
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

        im = ax.imshow(
            corr_mat,
            cmap="RdBu_r",
            vmin=-1,
            vmax=1,
        )
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


def x_plot_correlation_heatmap__mutmut_63(
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

        im = ax.imshow(corr_mat, cmap="XXRdBu_rXX", vmin=-1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_64(
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

        im = ax.imshow(corr_mat, cmap="rdbu_r", vmin=-1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_65(
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

        im = ax.imshow(corr_mat, cmap="RDBU_R", vmin=-1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_66(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=+1, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_67(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-2, vmax=1, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_68(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-1, vmax=2, aspect="equal")
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


def x_plot_correlation_heatmap__mutmut_69(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-1, vmax=1, aspect="XXequalXX")
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


def x_plot_correlation_heatmap__mutmut_70(
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

        im = ax.imshow(corr_mat, cmap="RdBu_r", vmin=-1, vmax=1, aspect="EQUAL")
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


def x_plot_correlation_heatmap__mutmut_71(
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
        fig.colorbar(None, ax=ax, label="Correlation")

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


def x_plot_correlation_heatmap__mutmut_72(
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
        fig.colorbar(im, ax=None, label="Correlation")

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


def x_plot_correlation_heatmap__mutmut_73(
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
        fig.colorbar(im, ax=ax, label=None)

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


def x_plot_correlation_heatmap__mutmut_74(
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
        fig.colorbar(ax=ax, label="Correlation")

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


def x_plot_correlation_heatmap__mutmut_75(
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
        fig.colorbar(im, label="Correlation")

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


def x_plot_correlation_heatmap__mutmut_76(
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
        fig.colorbar(
            im,
            ax=ax,
        )

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


def x_plot_correlation_heatmap__mutmut_77(
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
        fig.colorbar(im, ax=ax, label="XXCorrelationXX")

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


def x_plot_correlation_heatmap__mutmut_78(
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
        fig.colorbar(im, ax=ax, label="correlation")

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


def x_plot_correlation_heatmap__mutmut_79(
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
        fig.colorbar(im, ax=ax, label="CORRELATION")

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


def x_plot_correlation_heatmap__mutmut_80(
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
        for row in range(None):
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


def x_plot_correlation_heatmap__mutmut_81(
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
            for col in range(None):
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


def x_plot_correlation_heatmap__mutmut_82(
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
                color = None
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


def x_plot_correlation_heatmap__mutmut_83(
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
                color = "XXwhiteXX" if abs(corr_mat[row, col]) > 0.5 else "black"
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


def x_plot_correlation_heatmap__mutmut_84(
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
                color = "WHITE" if abs(corr_mat[row, col]) > 0.5 else "black"
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


def x_plot_correlation_heatmap__mutmut_85(
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
                color = "white" if abs(None) > 0.5 else "black"
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


def x_plot_correlation_heatmap__mutmut_86(
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
                color = "white" if abs(corr_mat[row, col]) >= 0.5 else "black"
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


def x_plot_correlation_heatmap__mutmut_87(
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
                color = "white" if abs(corr_mat[row, col]) > 1.5 else "black"
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


def x_plot_correlation_heatmap__mutmut_88(
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
                color = "white" if abs(corr_mat[row, col]) > 0.5 else "XXblackXX"
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


def x_plot_correlation_heatmap__mutmut_89(
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
                color = "white" if abs(corr_mat[row, col]) > 0.5 else "BLACK"
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


def x_plot_correlation_heatmap__mutmut_90(
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
                    None,
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


def x_plot_correlation_heatmap__mutmut_91(
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
                    None,
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


def x_plot_correlation_heatmap__mutmut_92(
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
                    None,
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


def x_plot_correlation_heatmap__mutmut_93(
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
                    ha=None,
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


def x_plot_correlation_heatmap__mutmut_94(
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
                    va=None,
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


def x_plot_correlation_heatmap__mutmut_95(
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
                    color=None,
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


def x_plot_correlation_heatmap__mutmut_96(
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
                    fontsize=None,
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_97(
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


def x_plot_correlation_heatmap__mutmut_98(
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


def x_plot_correlation_heatmap__mutmut_99(
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


def x_plot_correlation_heatmap__mutmut_100(
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


def x_plot_correlation_heatmap__mutmut_101(
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


def x_plot_correlation_heatmap__mutmut_102(
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


def x_plot_correlation_heatmap__mutmut_103(
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
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_104(
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
                    ha="XXcenterXX",
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


def x_plot_correlation_heatmap__mutmut_105(
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
                    ha="CENTER",
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


def x_plot_correlation_heatmap__mutmut_106(
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
                    va="XXcenterXX",
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


def x_plot_correlation_heatmap__mutmut_107(
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
                    va="CENTER",
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


def x_plot_correlation_heatmap__mutmut_108(
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
                    fontsize=theme.font_sizes.get(None, 9),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_109(
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
                    fontsize=theme.font_sizes.get("annotation", None),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_110(
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
                    fontsize=theme.font_sizes.get(9),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_111(
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
                    fontsize=theme.font_sizes.get(
                        "annotation",
                    ),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_112(
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
                    fontsize=theme.font_sizes.get("XXannotationXX", 9),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_113(
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
                    fontsize=theme.font_sizes.get("ANNOTATION", 9),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_114(
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
                    fontsize=theme.font_sizes.get("annotation", 10),
                )

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_115(
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

        series_names = None
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_116(
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

        series_names = getattr(None, "series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_117(
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

        series_names = getattr(results, None, [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_118(
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

        series_names = getattr(results, "series_names", None)
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_119(
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

        series_names = getattr("series_names", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_120(
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

        series_names = getattr(results, [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_121(
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

        series_names = results.series_names
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_122(
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

        series_names = getattr(results, "XXseries_namesXX", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_123(
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

        series_names = getattr(results, "SERIES_NAMES", [f"S{idx}" for idx in range(k)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_124(
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

        series_names = getattr(results, "series_names", [f"S{idx}" for idx in range(None)])
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_125(
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
        ax.set_xticks(None)
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_126(
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
        ax.set_xticks(range(None))
        ax.set_yticks(range(k))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_127(
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
        ax.set_yticks(None)
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_128(
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
        ax.set_yticks(range(None))
        ax.set_xticklabels(series_names[:k], rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_129(
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
        ax.set_xticklabels(None, rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_130(
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
        ax.set_xticklabels(series_names[:k], rotation=None, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_131(
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
        ax.set_xticklabels(series_names[:k], rotation=45, ha=None)
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_132(
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
        ax.set_xticklabels(rotation=45, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_133(
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
        ax.set_xticklabels(series_names[:k], ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_134(
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
        ax.set_xticklabels(
            series_names[:k],
            rotation=45,
        )
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_135(
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
        ax.set_xticklabels(series_names[:k], rotation=46, ha="right")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_136(
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
        ax.set_xticklabels(series_names[:k], rotation=45, ha="XXrightXX")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_137(
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
        ax.set_xticklabels(series_names[:k], rotation=45, ha="RIGHT")
        ax.set_yticklabels(series_names[:k])
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_138(
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
        ax.set_yticklabels(None)
        ax.set_title(title or f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_139(
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
        ax.set_title(None)

        fig.tight_layout()
        return fig


def x_plot_correlation_heatmap__mutmut_140(
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
        ax.set_title(title and f"Correlation Matrix {subtitle}")

        fig.tight_layout()
        return fig


x_plot_correlation_heatmap__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_plot_correlation_heatmap__mutmut_1": x_plot_correlation_heatmap__mutmut_1,
    "x_plot_correlation_heatmap__mutmut_2": x_plot_correlation_heatmap__mutmut_2,
    "x_plot_correlation_heatmap__mutmut_3": x_plot_correlation_heatmap__mutmut_3,
    "x_plot_correlation_heatmap__mutmut_4": x_plot_correlation_heatmap__mutmut_4,
    "x_plot_correlation_heatmap__mutmut_5": x_plot_correlation_heatmap__mutmut_5,
    "x_plot_correlation_heatmap__mutmut_6": x_plot_correlation_heatmap__mutmut_6,
    "x_plot_correlation_heatmap__mutmut_7": x_plot_correlation_heatmap__mutmut_7,
    "x_plot_correlation_heatmap__mutmut_8": x_plot_correlation_heatmap__mutmut_8,
    "x_plot_correlation_heatmap__mutmut_9": x_plot_correlation_heatmap__mutmut_9,
    "x_plot_correlation_heatmap__mutmut_10": x_plot_correlation_heatmap__mutmut_10,
    "x_plot_correlation_heatmap__mutmut_11": x_plot_correlation_heatmap__mutmut_11,
    "x_plot_correlation_heatmap__mutmut_12": x_plot_correlation_heatmap__mutmut_12,
    "x_plot_correlation_heatmap__mutmut_13": x_plot_correlation_heatmap__mutmut_13,
    "x_plot_correlation_heatmap__mutmut_14": x_plot_correlation_heatmap__mutmut_14,
    "x_plot_correlation_heatmap__mutmut_15": x_plot_correlation_heatmap__mutmut_15,
    "x_plot_correlation_heatmap__mutmut_16": x_plot_correlation_heatmap__mutmut_16,
    "x_plot_correlation_heatmap__mutmut_17": x_plot_correlation_heatmap__mutmut_17,
    "x_plot_correlation_heatmap__mutmut_18": x_plot_correlation_heatmap__mutmut_18,
    "x_plot_correlation_heatmap__mutmut_19": x_plot_correlation_heatmap__mutmut_19,
    "x_plot_correlation_heatmap__mutmut_20": x_plot_correlation_heatmap__mutmut_20,
    "x_plot_correlation_heatmap__mutmut_21": x_plot_correlation_heatmap__mutmut_21,
    "x_plot_correlation_heatmap__mutmut_22": x_plot_correlation_heatmap__mutmut_22,
    "x_plot_correlation_heatmap__mutmut_23": x_plot_correlation_heatmap__mutmut_23,
    "x_plot_correlation_heatmap__mutmut_24": x_plot_correlation_heatmap__mutmut_24,
    "x_plot_correlation_heatmap__mutmut_25": x_plot_correlation_heatmap__mutmut_25,
    "x_plot_correlation_heatmap__mutmut_26": x_plot_correlation_heatmap__mutmut_26,
    "x_plot_correlation_heatmap__mutmut_27": x_plot_correlation_heatmap__mutmut_27,
    "x_plot_correlation_heatmap__mutmut_28": x_plot_correlation_heatmap__mutmut_28,
    "x_plot_correlation_heatmap__mutmut_29": x_plot_correlation_heatmap__mutmut_29,
    "x_plot_correlation_heatmap__mutmut_30": x_plot_correlation_heatmap__mutmut_30,
    "x_plot_correlation_heatmap__mutmut_31": x_plot_correlation_heatmap__mutmut_31,
    "x_plot_correlation_heatmap__mutmut_32": x_plot_correlation_heatmap__mutmut_32,
    "x_plot_correlation_heatmap__mutmut_33": x_plot_correlation_heatmap__mutmut_33,
    "x_plot_correlation_heatmap__mutmut_34": x_plot_correlation_heatmap__mutmut_34,
    "x_plot_correlation_heatmap__mutmut_35": x_plot_correlation_heatmap__mutmut_35,
    "x_plot_correlation_heatmap__mutmut_36": x_plot_correlation_heatmap__mutmut_36,
    "x_plot_correlation_heatmap__mutmut_37": x_plot_correlation_heatmap__mutmut_37,
    "x_plot_correlation_heatmap__mutmut_38": x_plot_correlation_heatmap__mutmut_38,
    "x_plot_correlation_heatmap__mutmut_39": x_plot_correlation_heatmap__mutmut_39,
    "x_plot_correlation_heatmap__mutmut_40": x_plot_correlation_heatmap__mutmut_40,
    "x_plot_correlation_heatmap__mutmut_41": x_plot_correlation_heatmap__mutmut_41,
    "x_plot_correlation_heatmap__mutmut_42": x_plot_correlation_heatmap__mutmut_42,
    "x_plot_correlation_heatmap__mutmut_43": x_plot_correlation_heatmap__mutmut_43,
    "x_plot_correlation_heatmap__mutmut_44": x_plot_correlation_heatmap__mutmut_44,
    "x_plot_correlation_heatmap__mutmut_45": x_plot_correlation_heatmap__mutmut_45,
    "x_plot_correlation_heatmap__mutmut_46": x_plot_correlation_heatmap__mutmut_46,
    "x_plot_correlation_heatmap__mutmut_47": x_plot_correlation_heatmap__mutmut_47,
    "x_plot_correlation_heatmap__mutmut_48": x_plot_correlation_heatmap__mutmut_48,
    "x_plot_correlation_heatmap__mutmut_49": x_plot_correlation_heatmap__mutmut_49,
    "x_plot_correlation_heatmap__mutmut_50": x_plot_correlation_heatmap__mutmut_50,
    "x_plot_correlation_heatmap__mutmut_51": x_plot_correlation_heatmap__mutmut_51,
    "x_plot_correlation_heatmap__mutmut_52": x_plot_correlation_heatmap__mutmut_52,
    "x_plot_correlation_heatmap__mutmut_53": x_plot_correlation_heatmap__mutmut_53,
    "x_plot_correlation_heatmap__mutmut_54": x_plot_correlation_heatmap__mutmut_54,
    "x_plot_correlation_heatmap__mutmut_55": x_plot_correlation_heatmap__mutmut_55,
    "x_plot_correlation_heatmap__mutmut_56": x_plot_correlation_heatmap__mutmut_56,
    "x_plot_correlation_heatmap__mutmut_57": x_plot_correlation_heatmap__mutmut_57,
    "x_plot_correlation_heatmap__mutmut_58": x_plot_correlation_heatmap__mutmut_58,
    "x_plot_correlation_heatmap__mutmut_59": x_plot_correlation_heatmap__mutmut_59,
    "x_plot_correlation_heatmap__mutmut_60": x_plot_correlation_heatmap__mutmut_60,
    "x_plot_correlation_heatmap__mutmut_61": x_plot_correlation_heatmap__mutmut_61,
    "x_plot_correlation_heatmap__mutmut_62": x_plot_correlation_heatmap__mutmut_62,
    "x_plot_correlation_heatmap__mutmut_63": x_plot_correlation_heatmap__mutmut_63,
    "x_plot_correlation_heatmap__mutmut_64": x_plot_correlation_heatmap__mutmut_64,
    "x_plot_correlation_heatmap__mutmut_65": x_plot_correlation_heatmap__mutmut_65,
    "x_plot_correlation_heatmap__mutmut_66": x_plot_correlation_heatmap__mutmut_66,
    "x_plot_correlation_heatmap__mutmut_67": x_plot_correlation_heatmap__mutmut_67,
    "x_plot_correlation_heatmap__mutmut_68": x_plot_correlation_heatmap__mutmut_68,
    "x_plot_correlation_heatmap__mutmut_69": x_plot_correlation_heatmap__mutmut_69,
    "x_plot_correlation_heatmap__mutmut_70": x_plot_correlation_heatmap__mutmut_70,
    "x_plot_correlation_heatmap__mutmut_71": x_plot_correlation_heatmap__mutmut_71,
    "x_plot_correlation_heatmap__mutmut_72": x_plot_correlation_heatmap__mutmut_72,
    "x_plot_correlation_heatmap__mutmut_73": x_plot_correlation_heatmap__mutmut_73,
    "x_plot_correlation_heatmap__mutmut_74": x_plot_correlation_heatmap__mutmut_74,
    "x_plot_correlation_heatmap__mutmut_75": x_plot_correlation_heatmap__mutmut_75,
    "x_plot_correlation_heatmap__mutmut_76": x_plot_correlation_heatmap__mutmut_76,
    "x_plot_correlation_heatmap__mutmut_77": x_plot_correlation_heatmap__mutmut_77,
    "x_plot_correlation_heatmap__mutmut_78": x_plot_correlation_heatmap__mutmut_78,
    "x_plot_correlation_heatmap__mutmut_79": x_plot_correlation_heatmap__mutmut_79,
    "x_plot_correlation_heatmap__mutmut_80": x_plot_correlation_heatmap__mutmut_80,
    "x_plot_correlation_heatmap__mutmut_81": x_plot_correlation_heatmap__mutmut_81,
    "x_plot_correlation_heatmap__mutmut_82": x_plot_correlation_heatmap__mutmut_82,
    "x_plot_correlation_heatmap__mutmut_83": x_plot_correlation_heatmap__mutmut_83,
    "x_plot_correlation_heatmap__mutmut_84": x_plot_correlation_heatmap__mutmut_84,
    "x_plot_correlation_heatmap__mutmut_85": x_plot_correlation_heatmap__mutmut_85,
    "x_plot_correlation_heatmap__mutmut_86": x_plot_correlation_heatmap__mutmut_86,
    "x_plot_correlation_heatmap__mutmut_87": x_plot_correlation_heatmap__mutmut_87,
    "x_plot_correlation_heatmap__mutmut_88": x_plot_correlation_heatmap__mutmut_88,
    "x_plot_correlation_heatmap__mutmut_89": x_plot_correlation_heatmap__mutmut_89,
    "x_plot_correlation_heatmap__mutmut_90": x_plot_correlation_heatmap__mutmut_90,
    "x_plot_correlation_heatmap__mutmut_91": x_plot_correlation_heatmap__mutmut_91,
    "x_plot_correlation_heatmap__mutmut_92": x_plot_correlation_heatmap__mutmut_92,
    "x_plot_correlation_heatmap__mutmut_93": x_plot_correlation_heatmap__mutmut_93,
    "x_plot_correlation_heatmap__mutmut_94": x_plot_correlation_heatmap__mutmut_94,
    "x_plot_correlation_heatmap__mutmut_95": x_plot_correlation_heatmap__mutmut_95,
    "x_plot_correlation_heatmap__mutmut_96": x_plot_correlation_heatmap__mutmut_96,
    "x_plot_correlation_heatmap__mutmut_97": x_plot_correlation_heatmap__mutmut_97,
    "x_plot_correlation_heatmap__mutmut_98": x_plot_correlation_heatmap__mutmut_98,
    "x_plot_correlation_heatmap__mutmut_99": x_plot_correlation_heatmap__mutmut_99,
    "x_plot_correlation_heatmap__mutmut_100": x_plot_correlation_heatmap__mutmut_100,
    "x_plot_correlation_heatmap__mutmut_101": x_plot_correlation_heatmap__mutmut_101,
    "x_plot_correlation_heatmap__mutmut_102": x_plot_correlation_heatmap__mutmut_102,
    "x_plot_correlation_heatmap__mutmut_103": x_plot_correlation_heatmap__mutmut_103,
    "x_plot_correlation_heatmap__mutmut_104": x_plot_correlation_heatmap__mutmut_104,
    "x_plot_correlation_heatmap__mutmut_105": x_plot_correlation_heatmap__mutmut_105,
    "x_plot_correlation_heatmap__mutmut_106": x_plot_correlation_heatmap__mutmut_106,
    "x_plot_correlation_heatmap__mutmut_107": x_plot_correlation_heatmap__mutmut_107,
    "x_plot_correlation_heatmap__mutmut_108": x_plot_correlation_heatmap__mutmut_108,
    "x_plot_correlation_heatmap__mutmut_109": x_plot_correlation_heatmap__mutmut_109,
    "x_plot_correlation_heatmap__mutmut_110": x_plot_correlation_heatmap__mutmut_110,
    "x_plot_correlation_heatmap__mutmut_111": x_plot_correlation_heatmap__mutmut_111,
    "x_plot_correlation_heatmap__mutmut_112": x_plot_correlation_heatmap__mutmut_112,
    "x_plot_correlation_heatmap__mutmut_113": x_plot_correlation_heatmap__mutmut_113,
    "x_plot_correlation_heatmap__mutmut_114": x_plot_correlation_heatmap__mutmut_114,
    "x_plot_correlation_heatmap__mutmut_115": x_plot_correlation_heatmap__mutmut_115,
    "x_plot_correlation_heatmap__mutmut_116": x_plot_correlation_heatmap__mutmut_116,
    "x_plot_correlation_heatmap__mutmut_117": x_plot_correlation_heatmap__mutmut_117,
    "x_plot_correlation_heatmap__mutmut_118": x_plot_correlation_heatmap__mutmut_118,
    "x_plot_correlation_heatmap__mutmut_119": x_plot_correlation_heatmap__mutmut_119,
    "x_plot_correlation_heatmap__mutmut_120": x_plot_correlation_heatmap__mutmut_120,
    "x_plot_correlation_heatmap__mutmut_121": x_plot_correlation_heatmap__mutmut_121,
    "x_plot_correlation_heatmap__mutmut_122": x_plot_correlation_heatmap__mutmut_122,
    "x_plot_correlation_heatmap__mutmut_123": x_plot_correlation_heatmap__mutmut_123,
    "x_plot_correlation_heatmap__mutmut_124": x_plot_correlation_heatmap__mutmut_124,
    "x_plot_correlation_heatmap__mutmut_125": x_plot_correlation_heatmap__mutmut_125,
    "x_plot_correlation_heatmap__mutmut_126": x_plot_correlation_heatmap__mutmut_126,
    "x_plot_correlation_heatmap__mutmut_127": x_plot_correlation_heatmap__mutmut_127,
    "x_plot_correlation_heatmap__mutmut_128": x_plot_correlation_heatmap__mutmut_128,
    "x_plot_correlation_heatmap__mutmut_129": x_plot_correlation_heatmap__mutmut_129,
    "x_plot_correlation_heatmap__mutmut_130": x_plot_correlation_heatmap__mutmut_130,
    "x_plot_correlation_heatmap__mutmut_131": x_plot_correlation_heatmap__mutmut_131,
    "x_plot_correlation_heatmap__mutmut_132": x_plot_correlation_heatmap__mutmut_132,
    "x_plot_correlation_heatmap__mutmut_133": x_plot_correlation_heatmap__mutmut_133,
    "x_plot_correlation_heatmap__mutmut_134": x_plot_correlation_heatmap__mutmut_134,
    "x_plot_correlation_heatmap__mutmut_135": x_plot_correlation_heatmap__mutmut_135,
    "x_plot_correlation_heatmap__mutmut_136": x_plot_correlation_heatmap__mutmut_136,
    "x_plot_correlation_heatmap__mutmut_137": x_plot_correlation_heatmap__mutmut_137,
    "x_plot_correlation_heatmap__mutmut_138": x_plot_correlation_heatmap__mutmut_138,
    "x_plot_correlation_heatmap__mutmut_139": x_plot_correlation_heatmap__mutmut_139,
    "x_plot_correlation_heatmap__mutmut_140": x_plot_correlation_heatmap__mutmut_140,
}
x_plot_correlation_heatmap__mutmut_orig.__name__ = "x_plot_correlation_heatmap"


def plot_covariance_decomposition(
    results: Any,
    theme: str | Theme = "professional",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Figure:
    args = [results, theme, figsize, title]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_plot_covariance_decomposition__mutmut_orig,
        x_plot_covariance_decomposition__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_plot_covariance_decomposition__mutmut_orig(
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


def x_plot_covariance_decomposition__mutmut_1(
    results: Any,
    theme: str | Theme = "XXprofessionalXX",
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


def x_plot_covariance_decomposition__mutmut_2(
    results: Any,
    theme: str | Theme = "PROFESSIONAL",
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


def x_plot_covariance_decomposition__mutmut_3(
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
        theme = None

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


def x_plot_covariance_decomposition__mutmut_4(
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
        theme = get_theme(None)

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


def x_plot_covariance_decomposition__mutmut_5(
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

    rc_params = None
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


def x_plot_covariance_decomposition__mutmut_6(
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
    with plt.rc_context(None):
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


def x_plot_covariance_decomposition__mutmut_7(
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
        fig_size = None

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


def x_plot_covariance_decomposition__mutmut_8(
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
        fig_size = figsize and theme.figure_size

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


def x_plot_covariance_decomposition__mutmut_9(
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

        cov_array = None
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


def x_plot_covariance_decomposition__mutmut_10(
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

        cov_array = np.asarray(None, dtype=np.float64)
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


def x_plot_covariance_decomposition__mutmut_11(
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

        cov_array = np.asarray(results.dynamic_covariances, dtype=None)
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


def x_plot_covariance_decomposition__mutmut_12(
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

        cov_array = np.asarray(dtype=np.float64)
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


def x_plot_covariance_decomposition__mutmut_13(
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

        cov_array = np.asarray(
            results.dynamic_covariances,
        )
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


def x_plot_covariance_decomposition__mutmut_14(
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
        n_obs, k, _ = None
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


def x_plot_covariance_decomposition__mutmut_15(
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
        t_axis = None

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


def x_plot_covariance_decomposition__mutmut_16(
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
        t_axis = np.arange(None)

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


def x_plot_covariance_decomposition__mutmut_17(
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

        series_names = None

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


def x_plot_covariance_decomposition__mutmut_18(
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

        series_names = getattr(None, "series_names", [f"Series {idx}" for idx in range(k)])

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


def x_plot_covariance_decomposition__mutmut_19(
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

        series_names = getattr(results, None, [f"Series {idx}" for idx in range(k)])

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


def x_plot_covariance_decomposition__mutmut_20(
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

        series_names = getattr(results, "series_names", None)

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


def x_plot_covariance_decomposition__mutmut_21(
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

        series_names = getattr("series_names", [f"Series {idx}" for idx in range(k)])

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


def x_plot_covariance_decomposition__mutmut_22(
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

        series_names = getattr(results, [f"Series {idx}" for idx in range(k)])

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


def x_plot_covariance_decomposition__mutmut_23(
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

        series_names = results.series_names

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


def x_plot_covariance_decomposition__mutmut_24(
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

        series_names = getattr(results, "XXseries_namesXX", [f"Series {idx}" for idx in range(k)])

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


def x_plot_covariance_decomposition__mutmut_25(
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

        series_names = getattr(results, "SERIES_NAMES", [f"Series {idx}" for idx in range(k)])

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


def x_plot_covariance_decomposition__mutmut_26(
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

        series_names = getattr(results, "series_names", [f"Series {idx}" for idx in range(None)])

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


def x_plot_covariance_decomposition__mutmut_27(
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

        color_cycle = None

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


def x_plot_covariance_decomposition__mutmut_28(
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
            "XX#2e75b6XX",
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


def x_plot_covariance_decomposition__mutmut_29(
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
            "#2E75B6",
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


def x_plot_covariance_decomposition__mutmut_30(
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
            "XX#c00000XX",
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


def x_plot_covariance_decomposition__mutmut_31(
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
            "#C00000",
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


def x_plot_covariance_decomposition__mutmut_32(
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
            "XX#548235XX",
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


def x_plot_covariance_decomposition__mutmut_33(
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
            "XX#ffc000XX",
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


def x_plot_covariance_decomposition__mutmut_34(
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
            "#FFC000",
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


def x_plot_covariance_decomposition__mutmut_35(
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
            "XX#7030a0XX",
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


def x_plot_covariance_decomposition__mutmut_36(
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
            "#7030A0",
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


def x_plot_covariance_decomposition__mutmut_37(
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

        fig, ax = None

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


def x_plot_covariance_decomposition__mutmut_38(
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

        fig, ax = plt.subplots(None, 1, figsize=fig_size)

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


def x_plot_covariance_decomposition__mutmut_39(
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

        fig, ax = plt.subplots(1, None, figsize=fig_size)

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


def x_plot_covariance_decomposition__mutmut_40(
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

        fig, ax = plt.subplots(1, 1, figsize=None)

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


def x_plot_covariance_decomposition__mutmut_41(
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

        fig, ax = plt.subplots(1, figsize=fig_size)

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


def x_plot_covariance_decomposition__mutmut_42(
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

        fig, ax = plt.subplots(1, figsize=fig_size)

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


def x_plot_covariance_decomposition__mutmut_43(
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

        fig, ax = plt.subplots(
            1,
            1,
        )

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


def x_plot_covariance_decomposition__mutmut_44(
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

        fig, ax = plt.subplots(2, 1, figsize=fig_size)

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


def x_plot_covariance_decomposition__mutmut_45(
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

        fig, ax = plt.subplots(1, 2, figsize=fig_size)

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


def x_plot_covariance_decomposition__mutmut_46(
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
        variances = None

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


def x_plot_covariance_decomposition__mutmut_47(
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
        variances = np.array(None)

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


def x_plot_covariance_decomposition__mutmut_48(
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
        variances = np.array([cov_array[:, idx, idx] for idx in range(None)])

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


def x_plot_covariance_decomposition__mutmut_49(
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
            None,
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


def x_plot_covariance_decomposition__mutmut_50(
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
            labels=None,
            colors=color_cycle[:k],
            alpha=0.7,
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_51(
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
            colors=None,
            alpha=0.7,
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_52(
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
            alpha=None,
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_53(
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


def x_plot_covariance_decomposition__mutmut_54(
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


def x_plot_covariance_decomposition__mutmut_55(
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
            colors=color_cycle[:k],
            alpha=0.7,
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_56(
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
            alpha=0.7,
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_57(
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
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_58(
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
            alpha=1.7,
        )

        ax.set_xlabel("Observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_59(
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

        ax.set_xlabel(None)
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_60(
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

        ax.set_xlabel("XXObservationXX")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_61(
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

        ax.set_xlabel("observation")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_62(
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

        ax.set_xlabel("OBSERVATION")
        ax.set_ylabel("Variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_63(
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
        ax.set_ylabel(None)
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_64(
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
        ax.set_ylabel("XXVarianceXX")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_65(
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
        ax.set_ylabel("variance")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_66(
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
        ax.set_ylabel("VARIANCE")
        ax.set_title(title or "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_67(
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
        ax.set_title(None)
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_68(
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
        ax.set_title(title and "Covariance Decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_69(
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
        ax.set_title(title or "XXCovariance DecompositionXX")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_70(
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
        ax.set_title(title or "covariance decomposition")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_71(
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
        ax.set_title(title or "COVARIANCE DECOMPOSITION")
        ax.legend(loc="upper right", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_72(
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
        ax.legend(loc=None, framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_73(
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
        ax.legend(loc="upper right", framealpha=None)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_74(
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
        ax.legend(framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_75(
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
        ax.legend(
            loc="upper right",
        )

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_76(
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
        ax.legend(loc="XXupper rightXX", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_77(
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
        ax.legend(loc="UPPER RIGHT", framealpha=0.8)

        fig.tight_layout()
        return fig


def x_plot_covariance_decomposition__mutmut_78(
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
        ax.legend(loc="upper right", framealpha=1.8)

        fig.tight_layout()
        return fig


x_plot_covariance_decomposition__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_plot_covariance_decomposition__mutmut_1": x_plot_covariance_decomposition__mutmut_1,
    "x_plot_covariance_decomposition__mutmut_2": x_plot_covariance_decomposition__mutmut_2,
    "x_plot_covariance_decomposition__mutmut_3": x_plot_covariance_decomposition__mutmut_3,
    "x_plot_covariance_decomposition__mutmut_4": x_plot_covariance_decomposition__mutmut_4,
    "x_plot_covariance_decomposition__mutmut_5": x_plot_covariance_decomposition__mutmut_5,
    "x_plot_covariance_decomposition__mutmut_6": x_plot_covariance_decomposition__mutmut_6,
    "x_plot_covariance_decomposition__mutmut_7": x_plot_covariance_decomposition__mutmut_7,
    "x_plot_covariance_decomposition__mutmut_8": x_plot_covariance_decomposition__mutmut_8,
    "x_plot_covariance_decomposition__mutmut_9": x_plot_covariance_decomposition__mutmut_9,
    "x_plot_covariance_decomposition__mutmut_10": x_plot_covariance_decomposition__mutmut_10,
    "x_plot_covariance_decomposition__mutmut_11": x_plot_covariance_decomposition__mutmut_11,
    "x_plot_covariance_decomposition__mutmut_12": x_plot_covariance_decomposition__mutmut_12,
    "x_plot_covariance_decomposition__mutmut_13": x_plot_covariance_decomposition__mutmut_13,
    "x_plot_covariance_decomposition__mutmut_14": x_plot_covariance_decomposition__mutmut_14,
    "x_plot_covariance_decomposition__mutmut_15": x_plot_covariance_decomposition__mutmut_15,
    "x_plot_covariance_decomposition__mutmut_16": x_plot_covariance_decomposition__mutmut_16,
    "x_plot_covariance_decomposition__mutmut_17": x_plot_covariance_decomposition__mutmut_17,
    "x_plot_covariance_decomposition__mutmut_18": x_plot_covariance_decomposition__mutmut_18,
    "x_plot_covariance_decomposition__mutmut_19": x_plot_covariance_decomposition__mutmut_19,
    "x_plot_covariance_decomposition__mutmut_20": x_plot_covariance_decomposition__mutmut_20,
    "x_plot_covariance_decomposition__mutmut_21": x_plot_covariance_decomposition__mutmut_21,
    "x_plot_covariance_decomposition__mutmut_22": x_plot_covariance_decomposition__mutmut_22,
    "x_plot_covariance_decomposition__mutmut_23": x_plot_covariance_decomposition__mutmut_23,
    "x_plot_covariance_decomposition__mutmut_24": x_plot_covariance_decomposition__mutmut_24,
    "x_plot_covariance_decomposition__mutmut_25": x_plot_covariance_decomposition__mutmut_25,
    "x_plot_covariance_decomposition__mutmut_26": x_plot_covariance_decomposition__mutmut_26,
    "x_plot_covariance_decomposition__mutmut_27": x_plot_covariance_decomposition__mutmut_27,
    "x_plot_covariance_decomposition__mutmut_28": x_plot_covariance_decomposition__mutmut_28,
    "x_plot_covariance_decomposition__mutmut_29": x_plot_covariance_decomposition__mutmut_29,
    "x_plot_covariance_decomposition__mutmut_30": x_plot_covariance_decomposition__mutmut_30,
    "x_plot_covariance_decomposition__mutmut_31": x_plot_covariance_decomposition__mutmut_31,
    "x_plot_covariance_decomposition__mutmut_32": x_plot_covariance_decomposition__mutmut_32,
    "x_plot_covariance_decomposition__mutmut_33": x_plot_covariance_decomposition__mutmut_33,
    "x_plot_covariance_decomposition__mutmut_34": x_plot_covariance_decomposition__mutmut_34,
    "x_plot_covariance_decomposition__mutmut_35": x_plot_covariance_decomposition__mutmut_35,
    "x_plot_covariance_decomposition__mutmut_36": x_plot_covariance_decomposition__mutmut_36,
    "x_plot_covariance_decomposition__mutmut_37": x_plot_covariance_decomposition__mutmut_37,
    "x_plot_covariance_decomposition__mutmut_38": x_plot_covariance_decomposition__mutmut_38,
    "x_plot_covariance_decomposition__mutmut_39": x_plot_covariance_decomposition__mutmut_39,
    "x_plot_covariance_decomposition__mutmut_40": x_plot_covariance_decomposition__mutmut_40,
    "x_plot_covariance_decomposition__mutmut_41": x_plot_covariance_decomposition__mutmut_41,
    "x_plot_covariance_decomposition__mutmut_42": x_plot_covariance_decomposition__mutmut_42,
    "x_plot_covariance_decomposition__mutmut_43": x_plot_covariance_decomposition__mutmut_43,
    "x_plot_covariance_decomposition__mutmut_44": x_plot_covariance_decomposition__mutmut_44,
    "x_plot_covariance_decomposition__mutmut_45": x_plot_covariance_decomposition__mutmut_45,
    "x_plot_covariance_decomposition__mutmut_46": x_plot_covariance_decomposition__mutmut_46,
    "x_plot_covariance_decomposition__mutmut_47": x_plot_covariance_decomposition__mutmut_47,
    "x_plot_covariance_decomposition__mutmut_48": x_plot_covariance_decomposition__mutmut_48,
    "x_plot_covariance_decomposition__mutmut_49": x_plot_covariance_decomposition__mutmut_49,
    "x_plot_covariance_decomposition__mutmut_50": x_plot_covariance_decomposition__mutmut_50,
    "x_plot_covariance_decomposition__mutmut_51": x_plot_covariance_decomposition__mutmut_51,
    "x_plot_covariance_decomposition__mutmut_52": x_plot_covariance_decomposition__mutmut_52,
    "x_plot_covariance_decomposition__mutmut_53": x_plot_covariance_decomposition__mutmut_53,
    "x_plot_covariance_decomposition__mutmut_54": x_plot_covariance_decomposition__mutmut_54,
    "x_plot_covariance_decomposition__mutmut_55": x_plot_covariance_decomposition__mutmut_55,
    "x_plot_covariance_decomposition__mutmut_56": x_plot_covariance_decomposition__mutmut_56,
    "x_plot_covariance_decomposition__mutmut_57": x_plot_covariance_decomposition__mutmut_57,
    "x_plot_covariance_decomposition__mutmut_58": x_plot_covariance_decomposition__mutmut_58,
    "x_plot_covariance_decomposition__mutmut_59": x_plot_covariance_decomposition__mutmut_59,
    "x_plot_covariance_decomposition__mutmut_60": x_plot_covariance_decomposition__mutmut_60,
    "x_plot_covariance_decomposition__mutmut_61": x_plot_covariance_decomposition__mutmut_61,
    "x_plot_covariance_decomposition__mutmut_62": x_plot_covariance_decomposition__mutmut_62,
    "x_plot_covariance_decomposition__mutmut_63": x_plot_covariance_decomposition__mutmut_63,
    "x_plot_covariance_decomposition__mutmut_64": x_plot_covariance_decomposition__mutmut_64,
    "x_plot_covariance_decomposition__mutmut_65": x_plot_covariance_decomposition__mutmut_65,
    "x_plot_covariance_decomposition__mutmut_66": x_plot_covariance_decomposition__mutmut_66,
    "x_plot_covariance_decomposition__mutmut_67": x_plot_covariance_decomposition__mutmut_67,
    "x_plot_covariance_decomposition__mutmut_68": x_plot_covariance_decomposition__mutmut_68,
    "x_plot_covariance_decomposition__mutmut_69": x_plot_covariance_decomposition__mutmut_69,
    "x_plot_covariance_decomposition__mutmut_70": x_plot_covariance_decomposition__mutmut_70,
    "x_plot_covariance_decomposition__mutmut_71": x_plot_covariance_decomposition__mutmut_71,
    "x_plot_covariance_decomposition__mutmut_72": x_plot_covariance_decomposition__mutmut_72,
    "x_plot_covariance_decomposition__mutmut_73": x_plot_covariance_decomposition__mutmut_73,
    "x_plot_covariance_decomposition__mutmut_74": x_plot_covariance_decomposition__mutmut_74,
    "x_plot_covariance_decomposition__mutmut_75": x_plot_covariance_decomposition__mutmut_75,
    "x_plot_covariance_decomposition__mutmut_76": x_plot_covariance_decomposition__mutmut_76,
    "x_plot_covariance_decomposition__mutmut_77": x_plot_covariance_decomposition__mutmut_77,
    "x_plot_covariance_decomposition__mutmut_78": x_plot_covariance_decomposition__mutmut_78,
}
x_plot_covariance_decomposition__mutmut_orig.__name__ = "x_plot_covariance_decomposition"
