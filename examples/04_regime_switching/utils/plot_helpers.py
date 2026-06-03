"""
Plot helpers for regime-switching model visualization.

Provides specialized plotting functions for Markov-Switching models:
- Regime probability plots with shading
- Regime-dependent mean plots
- MS-GARCH volatility plots
- Transition matrix heatmaps
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_regime_probabilities(
    dates,
    series,
    probabilities,
    regime_labels=None,
    title="Smoothed Regime Probabilities",
    figsize=(14, 8),
    colors=None,
):
    """Plot a time series with regime probability shading.

    Parameters
    ----------
    dates : array-like
        Date index for the x-axis.
    series : array-like
        The observed time series (e.g., GDP growth, returns).
    probabilities : array-like
        Smoothed probabilities for regime 2 (or the 'event' regime).
        Shape (n,) for 2-regime or (n, k) for k-regime models.
    regime_labels : list of str, optional
        Labels for each regime (default: ["Regime 1", "Regime 2"]).
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    colors : list of str, optional
        Colors for regime shading.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    if regime_labels is None:
        regime_labels = ["Regime 1", "Regime 2"]
    if colors is None:
        colors = ["#2ecc71", "#e74c3c"]

    probs = np.asarray(probabilities)
    if probs.ndim == 1:
        probs = np.column_stack([1 - probs, probs])

    fig, axes = plt.subplots(
        2, 1, figsize=figsize, sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )

    # Top: series with regime shading
    ax1 = axes[0]
    ax1.plot(dates, series, color="black", linewidth=0.8, alpha=0.9)
    for j in range(probs.shape[1]):
        ax1.fill_between(
            dates,
            np.min(series),
            np.max(series),
            where=probs[:, j] > 0.5,
            alpha=0.15,
            color=colors[j % len(colors)],
            label=regime_labels[j],
        )
    ax1.set_title(title, fontsize=13)
    ax1.legend(loc="upper right", fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Bottom: regime probabilities
    ax2 = axes[1]
    for j in range(probs.shape[1]):
        ax2.plot(
            dates, probs[:, j], color=colors[j % len(colors)], linewidth=1.2, label=regime_labels[j]
        )
    ax2.set_ylabel("Probability")
    ax2.set_ylim(-0.05, 1.05)
    ax2.legend(loc="upper right", fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_regime_means(
    dates,
    series,
    regimes,
    mu,
    regime_labels=None,
    title="Regime-Dependent Means",
    figsize=(14, 5),
    colors=None,
):
    """Plot series with estimated regime-dependent means overlaid.

    Parameters
    ----------
    dates : array-like
        Date index.
    series : array-like
        Observed time series.
    regimes : array-like
        Estimated regime assignments (integer, 1-based or 0-based).
    mu : dict or list
        Mean for each regime. If dict, keys are regime values.
        If list, index corresponds to regime number.
    regime_labels : list of str, optional
        Labels for regimes.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    colors : list of str, optional
        Colors for each regime.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    if colors is None:
        colors = ["#2ecc71", "#e74c3c", "#3498db", "#f39c12"]
    if regime_labels is None:
        unique_reg = sorted(np.unique(regimes))
        regime_labels = [f"Regime {r}" for r in unique_reg]

    regimes = np.asarray(regimes)
    unique_reg = sorted(np.unique(regimes))

    # Build mean mapping
    if isinstance(mu, list | np.ndarray):
        mu_map = {r: mu[i] for i, r in enumerate(unique_reg)}
    else:
        mu_map = mu

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(dates, series, color="gray", linewidth=0.7, alpha=0.7, label="Observed")

    # Overlay regime means
    mean_line = np.array([mu_map[r] for r in regimes])
    for i, r in enumerate(unique_reg):
        mask = regimes == r
        regime_labels[i] if i < len(regime_labels) else f"Regime {r}"
        ax.fill_between(
            dates,
            np.min(series),
            np.max(series),
            where=mask,
            alpha=0.12,
            color=colors[i % len(colors)],
        )
    ax.plot(dates, mean_line, color="darkblue", linewidth=1.5, linestyle="--", label="Regime mean")

    ax.set_title(title, fontsize=13)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_ms_volatility(
    dates,
    returns,
    volatility,
    regimes=None,
    title="MS-GARCH Volatility",
    figsize=(14, 8),
    colors=None,
):
    """Plot returns and MS-GARCH conditional volatility with regime shading.

    Parameters
    ----------
    dates : array-like
        Date index.
    returns : array-like
        Return series.
    volatility : array-like
        Conditional volatility (standard deviation).
    regimes : array-like, optional
        Regime assignments for shading.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    colors : list of str, optional
        Colors for regime shading.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    if colors is None:
        colors = ["#2ecc71", "#e74c3c"]

    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)

    # Top: returns
    ax1 = axes[0]
    ax1.plot(dates, returns, color="black", linewidth=0.5, alpha=0.8)
    if regimes is not None:
        regimes = np.asarray(regimes)
        unique_reg = sorted(np.unique(regimes))
        for i, r in enumerate(unique_reg):
            ax1.fill_between(
                dates,
                np.min(returns),
                np.max(returns),
                where=regimes == r,
                alpha=0.1,
                color=colors[i % len(colors)],
                label=f"Regime {r}",
            )
        ax1.legend(loc="upper right", fontsize=9)
    ax1.set_title(f"{title} - Returns", fontsize=12)
    ax1.grid(True, alpha=0.3)

    # Bottom: volatility
    ax2 = axes[1]
    ax2.plot(dates, volatility, color="darkred", linewidth=1.0)
    if regimes is not None:
        for i, r in enumerate(unique_reg):
            ax2.fill_between(
                dates,
                0,
                np.max(volatility),
                where=regimes == r,
                alpha=0.1,
                color=colors[i % len(colors)],
            )
    ax2.set_title("Conditional Volatility", fontsize=12)
    ax2.set_ylabel("Volatility (std dev)")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_transition_matrix(
    P,
    regime_labels=None,
    title="Estimated Transition Matrix",
    figsize=(6, 5),
    cmap="Blues",
    annot_fontsize=14,
):
    """Plot a transition probability matrix as a heatmap.

    Parameters
    ----------
    P : array-like
        Transition probability matrix (k x k).
    regime_labels : list of str, optional
        Labels for regimes.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    cmap : str
        Colormap name.
    annot_fontsize : int
        Font size for cell annotations.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    P = np.asarray(P)
    k = P.shape[0]

    if regime_labels is None:
        regime_labels = [f"Regime {i + 1}" for i in range(k)]

    fig, ax = plt.subplots(figsize=figsize)

    im = ax.imshow(P, cmap=cmap, vmin=0, vmax=1, aspect="equal")

    # Annotate cells
    for i in range(k):
        for j in range(k):
            color = "white" if P[i, j] > 0.5 else "black"
            ax.text(
                j,
                i,
                f"{P[i, j]:.3f}",
                ha="center",
                va="center",
                fontsize=annot_fontsize,
                color=color,
                fontweight="bold",
            )

    ax.set_xticks(range(k))
    ax.set_yticks(range(k))
    ax.set_xticklabels(regime_labels, fontsize=11)
    ax.set_yticklabels(regime_labels, fontsize=11)
    ax.set_xlabel("To", fontsize=12)
    ax.set_ylabel("From", fontsize=12)
    ax.set_title(title, fontsize=13)

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    return fig
