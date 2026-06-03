"""Visualization helpers for diagnostics examples.

Provides plotting functions for residual analysis, news impact curves,
sign bias, and parameter stability diagnostics.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def plot_standardized_residuals(
    residuals: np.ndarray,
    title: str = "Standardized Residuals",
    figsize: tuple = (12, 4),
    save_path: str | None = None,
) -> plt.Figure:
    """Plot standardized residuals over time.

    Parameters
    ----------
    residuals : np.ndarray
        Standardized residual series.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str or None
        If provided, save figure to this path.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(residuals, linewidth=0.5, color="steelblue")
    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.axhline(y=2, color="red", linewidth=0.5, linestyle="--", alpha=0.7)
    ax.axhline(y=-2, color="red", linewidth=0.5, linestyle="--", alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel("Observation")
    ax.set_ylabel("Standardized Residual")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_residual_diagnostics(
    residuals: np.ndarray,
    lags: int = 40,
    title: str = "Residual Diagnostics",
    figsize: tuple = (12, 12),
    save_path: str | None = None,
) -> plt.Figure:
    """Plot a 4-panel residual diagnostic: series, ACF, PACF, QQ-plot.

    Parameters
    ----------
    residuals : np.ndarray
        Standardized residual series.
    lags : int
        Number of lags for ACF/PACF.
    title : str
        Overall figure title.
    figsize : tuple
        Figure size.
    save_path : str or None
        If provided, save figure to this path.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, axes = plt.subplots(4, 1, figsize=figsize)
    fig.suptitle(title, fontsize=14, y=1.02)

    # Panel 1: Standardized residuals
    axes[0].plot(residuals, linewidth=0.5, color="steelblue")
    axes[0].axhline(y=0, color="black", linewidth=0.5)
    axes[0].set_title("Standardized Residuals")
    axes[0].set_ylabel("Value")

    # Panel 2: ACF of squared residuals
    plot_acf(residuals**2, lags=lags, ax=axes[1], title="ACF of Squared Residuals")

    # Panel 3: PACF of squared residuals
    plot_pacf(residuals**2, lags=lags, ax=axes[2], title="PACF of Squared Residuals")

    # Panel 4: QQ-plot
    stats.probplot(residuals, dist="norm", plot=axes[3])
    axes[3].set_title("Normal Q-Q Plot")
    axes[3].get_lines()[0].set(marker="o", markersize=2, color="steelblue")
    axes[3].get_lines()[1].set(color="red")

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_news_impact_curve(
    model_results: list,
    labels: list[str],
    shock_range: tuple = (-3, 3),
    n_points: int = 200,
    title: str = "News Impact Curve",
    figsize: tuple = (10, 6),
    save_path: str | None = None,
) -> plt.Figure:
    """Plot news impact curves for multiple GARCH-family models.

    Each model_result dict should contain the keys needed to compute
    the NIC for that model type:
    - 'type': one of 'garch', 'egarch', 'gjr'
    - 'omega', 'alpha', 'beta': common parameters
    - 'gamma': asymmetry parameter (for egarch/gjr)
    - 'sigma2_bar': long-run variance (used as sigma2_{t-1})

    Parameters
    ----------
    model_results : list of dict
        Each dict contains model parameters for NIC computation.
    labels : list of str
        Labels for each model curve.
    shock_range : tuple
        Range of standardized shocks (min, max).
    n_points : int
        Number of points in the curve.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str or None
        If provided, save figure to this path.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    z = np.linspace(shock_range[0], shock_range[1], n_points)

    colors = ["steelblue", "darkorange", "green", "red", "purple"]

    for i, (params, label) in enumerate(zip(model_results, labels, strict=False)):
        model_type = params.get("type", "garch")
        omega = params["omega"]
        alpha = params["alpha"]
        beta = params["beta"]
        sigma2_bar = params.get("sigma2_bar", omega / (1 - alpha - beta))

        eps = z * np.sqrt(sigma2_bar)

        if model_type == "garch":
            sigma2_next = omega + alpha * eps**2 + beta * sigma2_bar
        elif model_type == "gjr":
            gamma = params.get("gamma", 0.0)
            indicator = (eps < 0).astype(float)
            sigma2_next = omega + alpha * eps**2 + gamma * indicator * eps**2 + beta * sigma2_bar
        elif model_type == "egarch":
            gamma = params.get("gamma", 0.0)
            log_sigma2_bar = np.log(sigma2_bar)
            log_sigma2_next = omega + alpha * np.abs(z) + gamma * z + beta * log_sigma2_bar
            sigma2_next = np.exp(log_sigma2_next)
        else:
            sigma2_next = omega + alpha * eps**2 + beta * sigma2_bar

        color = colors[i % len(colors)]
        ax.plot(eps * 100, sigma2_next, label=label, color=color, linewidth=2)

    ax.axvline(x=0, color="gray", linewidth=0.5, linestyle="--")
    ax.set_xlabel("Shock (return in %)")
    ax.set_ylabel(r"$\sigma^2_{t+1}$")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_sign_bias_scatter(
    returns: np.ndarray,
    volatility: np.ndarray,
    title: str = "Sign Bias: Returns vs Conditional Volatility",
    figsize: tuple = (10, 6),
    save_path: str | None = None,
) -> plt.Figure:
    """Scatter plot of lagged returns vs conditional volatility for sign bias.

    Separates positive and negative lagged returns to visually detect
    asymmetric volatility response (leverage effect).

    Parameters
    ----------
    returns : np.ndarray
        Return series.
    volatility : np.ndarray
        Conditional volatility series (same length as returns).
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str or None
        If provided, save figure to this path.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    lagged_returns = returns[:-1]
    current_vol = volatility[1:]

    pos_mask = lagged_returns >= 0
    neg_mask = lagged_returns < 0

    ax.scatter(
        lagged_returns[pos_mask],
        current_vol[pos_mask],
        alpha=0.3,
        s=10,
        color="steelblue",
        label=f"Positive shocks (n={pos_mask.sum()})",
    )
    ax.scatter(
        lagged_returns[neg_mask],
        current_vol[neg_mask],
        alpha=0.3,
        s=10,
        color="red",
        label=f"Negative shocks (n={neg_mask.sum()})",
    )

    # Fit separate linear trends
    if pos_mask.sum() > 1:
        z_pos = np.polyfit(lagged_returns[pos_mask], current_vol[pos_mask], 1)
        p_pos = np.poly1d(z_pos)
        x_pos = np.linspace(0, lagged_returns[pos_mask].max(), 50)
        ax.plot(x_pos, p_pos(x_pos), color="steelblue", linewidth=2, linestyle="--")

    if neg_mask.sum() > 1:
        z_neg = np.polyfit(lagged_returns[neg_mask], current_vol[neg_mask], 1)
        p_neg = np.poly1d(z_neg)
        x_neg = np.linspace(lagged_returns[neg_mask].min(), 0, 50)
        ax.plot(x_neg, p_neg(x_neg), color="red", linewidth=2, linestyle="--")

    ax.axvline(x=0, color="gray", linewidth=0.5, linestyle="--")
    ax.set_xlabel("Lagged Return")
    ax.set_ylabel("Conditional Volatility")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_nyblom_recursive(
    params_recursive: dict[str, np.ndarray],
    title: str = "Recursive Parameter Estimates (Nyblom Stability)",
    figsize: tuple = (12, 8),
    save_path: str | None = None,
) -> plt.Figure:
    """Plot recursive parameter estimates over time for stability analysis.

    Visualizes how GARCH parameter estimates evolve as the sample grows.
    Structural breaks will appear as shifts in the recursive estimates.

    Parameters
    ----------
    params_recursive : dict of str -> np.ndarray
        Dictionary mapping parameter names to arrays of recursive estimates.
        Each array has length equal to the number of recursive windows.
    title : str
        Overall figure title.
    figsize : tuple
        Figure size.
    save_path : str or None
        If provided, save figure to this path.

    Returns
    -------
    matplotlib.figure.Figure
    """
    n_params = len(params_recursive)
    fig, axes = plt.subplots(n_params, 1, figsize=figsize, sharex=True)
    if n_params == 1:
        axes = [axes]

    fig.suptitle(title, fontsize=14)

    colors = ["steelblue", "darkorange", "green", "red", "purple"]

    for i, (name, values) in enumerate(params_recursive.items()):
        color = colors[i % len(colors)]
        ax = axes[i]
        x = np.arange(len(values))
        ax.plot(x, values, color=color, linewidth=1.5)

        # Add mean line
        mean_val = np.mean(values)
        ax.axhline(y=mean_val, color="gray", linewidth=0.8, linestyle="--", alpha=0.7)

        # Mark midpoint (potential break)
        mid = len(values) // 2
        ax.axvline(x=mid, color="red", linewidth=0.8, linestyle=":", alpha=0.7)

        ax.set_ylabel(name)
        ax.set_title(f"Recursive estimate: {name}", fontsize=10)

    axes[-1].set_xlabel("Window end observation")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
