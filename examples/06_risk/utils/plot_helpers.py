"""Plotting utilities for risk management examples.

Functions for visualizing VaR, ES, EWMA, backtesting results,
and PIT (Probability Integral Transform) diagnostics.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_var_exceedances(
    returns: pd.Series,
    var_series: pd.Series,
    level: float = 0.05,
    title: str = "VaR Exceedances",
    figsize: tuple = (14, 6),
) -> plt.Figure:
    """Plot return series with VaR and violation points.

    Parameters
    ----------
    returns : pd.Series
        Return series (negative values = losses).
    var_series : pd.Series
        VaR series (negative values, same sign convention as returns).
    level : float
        Confidence level (e.g., 0.05 for 95% VaR).
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(
        returns.index, returns.values, color="steelblue", alpha=0.6, linewidth=0.8, label="Returns"
    )
    ax.plot(
        var_series.index,
        var_series.values,
        color="red",
        linewidth=1.2,
        label=f"VaR ({(1-level)*100:.0f}%)",
    )

    # Highlight exceedances
    violations = returns < var_series
    if violations.any():
        ax.scatter(
            returns.index[violations],
            returns.values[violations],
            color="red",
            s=15,
            zorder=5,
            label=f"Violations ({violations.sum()})",
        )

    n_violations = violations.sum()
    expected = level * len(returns)
    ax.set_title(
        f"{title}\nViolations: {n_violations} (expected: {expected:.0f}, rate: {n_violations/len(returns):.4f})"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Returns")
    ax.legend(loc="lower left")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_var_comparison(
    returns: pd.Series,
    var_dict: dict,
    title: str = "VaR Model Comparison",
    figsize: tuple = (14, 7),
) -> plt.Figure:
    """Plot multiple VaR series on the same chart for comparison.

    Parameters
    ----------
    returns : pd.Series
        Return series.
    var_dict : dict
        Dictionary {model_name: var_series} with VaR from different models.
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.fill_between(returns.index, returns.values, 0, alpha=0.2, color="gray", label="Returns")

    colors = ["red", "blue", "green", "orange", "purple", "brown"]
    for i, (name, var_s) in enumerate(var_dict.items()):
        color = colors[i % len(colors)]
        violations = (returns < var_s).sum()
        rate = violations / len(returns)
        ax.plot(
            var_s.index,
            var_s.values,
            color=color,
            linewidth=1.2,
            label=f"{name} (violations: {violations}, rate: {rate:.4f})",
        )

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Returns / VaR")
    ax.legend(loc="lower left", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_es_visualization(
    returns: pd.Series,
    var_series: pd.Series,
    es_series: pd.Series,
    title: str = "VaR and Expected Shortfall",
    figsize: tuple = (14, 7),
) -> plt.Figure:
    """Visualize VaR and ES with shaded area between them.

    Parameters
    ----------
    returns : pd.Series
        Return series.
    var_series : pd.Series
        VaR series.
    es_series : pd.Series
        Expected Shortfall series.
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, axes = plt.subplots(2, 1, figsize=figsize, height_ratios=[3, 1])

    # Top panel: time series
    ax = axes[0]
    ax.plot(
        returns.index, returns.values, color="steelblue", alpha=0.5, linewidth=0.7, label="Returns"
    )
    ax.plot(var_series.index, var_series.values, color="red", linewidth=1.0, label="VaR")
    ax.plot(
        es_series.index,
        es_series.values,
        color="darkred",
        linewidth=1.0,
        linestyle="--",
        label="ES",
    )
    ax.fill_between(
        var_series.index,
        var_series.values,
        es_series.values,
        alpha=0.2,
        color="red",
        label="ES region",
    )
    ax.set_title(title)
    ax.set_ylabel("Returns")
    ax.legend(loc="lower left")
    ax.grid(True, alpha=0.3)

    # Bottom panel: distribution of returns vs VaR/ES
    ax2 = axes[1]
    ax2.hist(
        returns.values, bins=80, density=True, alpha=0.6, color="steelblue", label="Returns dist."
    )
    var_mean = var_series.mean()
    es_mean = es_series.mean()
    ax2.axvline(var_mean, color="red", linewidth=2, label=f"Mean VaR: {var_mean:.4f}")
    ax2.axvline(
        es_mean, color="darkred", linewidth=2, linestyle="--", label=f"Mean ES: {es_mean:.4f}"
    )
    ax2.set_xlabel("Returns")
    ax2.set_ylabel("Density")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


def plot_backtest_summary(
    backtest_results: dict,
    title: str = "Backtesting Summary",
    figsize: tuple = (12, 8),
) -> plt.Figure:
    """Visual summary of backtesting results across models.

    Parameters
    ----------
    backtest_results : dict
        Dictionary with structure:
        {model_name: {"violations": int, "expected": float, "ratio": float,
                       "pvalue_uc": float, "pvalue_cc": float}}
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    models = list(backtest_results.keys())
    n = len(models)

    fig, axes = plt.subplots(1, 3, figsize=figsize)

    # Panel 1: Violation ratio (actual/expected)
    ax = axes[0]
    ratios = [backtest_results[m].get("ratio", 0) for m in models]
    colors = [
        "green" if 0.8 <= r <= 1.2 else "orange" if 0.5 <= r <= 1.5 else "red" for r in ratios
    ]
    ax.barh(models, ratios, color=colors, alpha=0.7)
    ax.axvline(1.0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("Violation Ratio (actual/expected)")
    ax.set_title("Violation Ratio")
    ax.grid(True, alpha=0.3, axis="x")

    # Panel 2: p-values
    ax = axes[1]
    pv_uc = [backtest_results[m].get("pvalue_uc", np.nan) for m in models]
    pv_cc = [backtest_results[m].get("pvalue_cc", np.nan) for m in models]
    x = np.arange(n)
    width = 0.35
    ax.barh(x - width / 2, pv_uc, width, label="Unconditional", alpha=0.7, color="steelblue")
    ax.barh(x + width / 2, pv_cc, width, label="Conditional", alpha=0.7, color="coral")
    ax.axvline(0.05, color="red", linestyle="--", linewidth=1, label="5% threshold")
    ax.set_yticks(x)
    ax.set_yticklabels(models)
    ax.set_xlabel("p-value")
    ax.set_title("Kupiec & Christoffersen Tests")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="x")

    # Panel 3: Violation counts
    ax = axes[2]
    violations = [backtest_results[m].get("violations", 0) for m in models]
    expected = [backtest_results[m].get("expected", 0) for m in models]
    ax.barh(x - width / 2, violations, width, label="Actual", alpha=0.7, color="red")
    ax.barh(x + width / 2, expected, width, label="Expected", alpha=0.7, color="green")
    ax.set_yticks(x)
    ax.set_yticklabels(models)
    ax.set_xlabel("Count")
    ax.set_title("Violations: Actual vs Expected")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="x")

    fig.suptitle(title, fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    return fig


def plot_ewma_lambda(
    returns: pd.Series,
    lambdas: list[float] = None,
    title: str = "EWMA Volatility for Different Lambdas",
    figsize: tuple = (14, 6),
) -> plt.Figure:
    """Plot EWMA volatility for different decay factors.

    Parameters
    ----------
    returns : pd.Series
        Return series.
    lambdas : list of float
        Decay factors to compare.
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    if lambdas is None:
        lambdas = [0.9, 0.94, 0.97]
    fig, axes = plt.subplots(2, 1, figsize=figsize, height_ratios=[1, 2])

    # Top: returns
    ax = axes[0]
    ax.plot(returns.index, returns.values, color="steelblue", alpha=0.6, linewidth=0.7)
    ax.set_ylabel("Returns")
    ax.set_title("Returns")
    ax.grid(True, alpha=0.3)

    # Bottom: EWMA volatilities
    ax = axes[1]
    colors = ["red", "blue", "green", "orange", "purple"]
    for i, lam in enumerate(lambdas):
        # Compute EWMA variance
        r = returns.values
        var_ewma = np.empty(len(r))
        var_ewma[0] = r[0] ** 2
        for t in range(1, len(r)):
            var_ewma[t] = lam * var_ewma[t - 1] + (1 - lam) * r[t - 1] ** 2
        vol_ewma = np.sqrt(var_ewma)
        ax.plot(
            returns.index,
            vol_ewma,
            color=colors[i % len(colors)],
            linewidth=1.2,
            label=f"λ = {lam}",
        )

    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_pit_histogram(
    pit_values: np.ndarray,
    bins: int = 20,
    title: str = "PIT Histogram (Probability Integral Transform)",
    figsize: tuple = (10, 5),
) -> plt.Figure:
    """Plot PIT histogram for model validation.

    If the model is correctly specified, PIT values should be
    uniformly distributed on [0, 1].

    Parameters
    ----------
    pit_values : np.ndarray
        PIT values in [0, 1].
    bins : int
        Number of histogram bins.
    title : str
        Plot title.
    figsize : tuple
        Figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.hist(pit_values, bins=bins, density=True, alpha=0.7, color="steelblue", edgecolor="white")
    ax.axhline(1.0, color="red", linestyle="--", linewidth=2, label="Uniform reference")

    # Add confidence band (approximate 95% for uniform)
    n = len(pit_values)
    np.sqrt(1.0 / (bins * n))  # approx standard error per bin
    ax.axhline(
        1.0 + 1.96 * np.sqrt(bins / n), color="red", linestyle=":", alpha=0.5, label="95% band"
    )
    ax.axhline(max(0, 1.0 - 1.96 * np.sqrt(bins / n)), color="red", linestyle=":", alpha=0.5)

    ax.set_xlabel("PIT Value")
    ax.set_ylabel("Density")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig
