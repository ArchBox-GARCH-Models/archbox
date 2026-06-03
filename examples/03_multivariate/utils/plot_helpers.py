"""
Visualization helpers for multivariate GARCH examples.

Provides functions for plotting correlation heatmaps, dynamic correlations,
portfolio weights, covariance eigenvalues, and conditional covariances.
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


def plot_correlation_heatmap(
    corr_matrix: np.ndarray,
    labels: list[str],
    title: str = "Correlation Matrix",
    ax=None,
    cmap: str = "RdBu_r",
    vmin: float = -1.0,
    vmax: float = 1.0,
    annot: bool = True,
    save_path: str | None = None,
):
    """
    Plot a correlation matrix as a heatmap with annotations.

    Parameters
    ----------
    corr_matrix : np.ndarray
        Square correlation matrix (k x k).
    labels : list[str]
        Asset/series names for axis labels.
    title : str
        Plot title.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on; creates new figure if None.
    cmap : str
        Colormap name.
    vmin, vmax : float
        Color range bounds.
    annot : bool
        Whether to annotate cells with values.
    save_path : str, optional
        If provided, save figure to this path.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.figure

    k = len(labels)
    im = ax.imshow(corr_matrix, cmap=cmap, vmin=vmin, vmax=vmax, aspect="equal")

    ax.set_xticks(range(k))
    ax.set_yticks(range(k))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_title(title)

    fig.colorbar(im, ax=ax, shrink=0.8)

    if annot:
        for i in range(k):
            for j in range(k):
                color = "white" if abs(corr_matrix[i, j]) > 0.6 else "black"
                ax.text(
                    j,
                    i,
                    f"{corr_matrix[i, j]:.2f}",
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=10,
                )

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig, ax


def plot_dynamic_correlations(
    dates,
    correlations: dict[str, np.ndarray],
    title: str = "Dynamic Conditional Correlations",
    figsize: tuple = (14, 6),
    save_path: str | None = None,
):
    """
    Plot time-varying correlations from a DCC or similar model.

    Parameters
    ----------
    dates : array-like
        Date index for x-axis.
    correlations : dict[str, np.ndarray]
        Mapping from pair label (e.g., "EUR/USD-GBP/USD") to correlation time series.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        If provided, save figure to this path.
    """
    fig, ax = plt.subplots(figsize=figsize)

    for label, corr in correlations.items():
        ax.plot(dates, corr, label=label, alpha=0.8, linewidth=0.8)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Correlation")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color="black", linewidth=0.5, linestyle="--")

    if hasattr(dates[0], "strftime"):
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        fig.autofmt_xdate()

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig, ax


def plot_portfolio_weights(
    dates,
    weights: np.ndarray,
    labels: list[str],
    title: str = "Portfolio Weights Over Time",
    figsize: tuple = (14, 6),
    save_path: str | None = None,
):
    """
    Plot portfolio weight allocations as a stacked area chart.

    Parameters
    ----------
    dates : array-like
        Date index for x-axis.
    weights : np.ndarray
        Array of shape (T, k) with portfolio weights.
    labels : list[str]
        Asset names.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        If provided, save figure to this path.
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.stackplot(dates, weights.T, labels=labels, alpha=0.8)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)

    if hasattr(dates[0], "strftime"):
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        fig.autofmt_xdate()

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig, ax


def plot_covariance_eigenvalues(
    dates,
    eigenvalues: np.ndarray,
    title: str = "Eigenvalues of Conditional Covariance Matrix",
    figsize: tuple = (14, 6),
    save_path: str | None = None,
):
    """
    Plot eigenvalues of the conditional covariance matrix over time.

    Useful for monitoring concentration of risk and detecting periods
    where variance is dominated by a single factor.

    Parameters
    ----------
    dates : array-like
        Date index for x-axis.
    eigenvalues : np.ndarray
        Array of shape (T, k) with eigenvalues sorted descending.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        If provided, save figure to this path.
    """
    fig, ax = plt.subplots(figsize=figsize)

    k = eigenvalues.shape[1]
    for i in range(k):
        ax.plot(dates, eigenvalues[:, i], label=f"Eigenvalue {i + 1}", alpha=0.8, linewidth=0.8)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Eigenvalue")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_yscale("log")

    if hasattr(dates[0], "strftime"):
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        fig.autofmt_xdate()

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig, ax


def plot_conditional_covariance(
    dates,
    covariances: dict[str, np.ndarray],
    title: str = "Conditional Covariances",
    figsize: tuple = (14, 8),
    save_path: str | None = None,
):
    """
    Plot conditional variances (diagonal) and covariances (off-diagonal) over time.

    Parameters
    ----------
    dates : array-like
        Date index for x-axis.
    covariances : dict[str, np.ndarray]
        Mapping from element label (e.g., "Var(EUR/USD)" or "Cov(EUR,GBP)")
        to time series of length T.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        If provided, save figure to this path.
    """
    # Separate variances from covariances
    var_items = {k: v for k, v in covariances.items() if k.startswith("Var")}
    cov_items = {k: v for k, v in covariances.items() if k.startswith("Cov")}

    n_panels = 1 + (1 if cov_items else 0)
    fig, axes = plt.subplots(n_panels, 1, figsize=figsize, sharex=True)
    if n_panels == 1:
        axes = [axes]

    # Variances
    for label, series in var_items.items():
        axes[0].plot(dates, series, label=label, alpha=0.8, linewidth=0.8)
    axes[0].set_title("Conditional Variances")
    axes[0].set_ylabel("Variance")
    axes[0].legend(loc="best", fontsize=8)
    axes[0].grid(True, alpha=0.3)

    # Covariances
    if cov_items:
        for label, series in cov_items.items():
            axes[1].plot(dates, series, label=label, alpha=0.8, linewidth=0.8)
        axes[1].set_title("Conditional Covariances")
        axes[1].set_ylabel("Covariance")
        axes[1].legend(loc="best", fontsize=8)
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=0, color="black", linewidth=0.5, linestyle="--")

    axes[-1].set_xlabel("Date")

    if hasattr(dates[0], "strftime"):
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        fig.autofmt_xdate()

    fig.suptitle(title, fontsize=14, y=1.02)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig, axes
