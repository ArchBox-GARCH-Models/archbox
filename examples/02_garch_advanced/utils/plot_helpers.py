"""Plotting utilities for advanced GARCH examples.

Provides specialized visualization functions for FIGARCH long memory,
realized vs conditional volatility comparison, HAR-RV components,
and GARCH-M risk premium analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import acf


def plot_long_memory_acf(
    squared_returns,
    max_lags: int = 200,
    title: str = "Long Memory in Squared Returns - ACF",
    figsize: tuple = (12, 5),
    save_path: str = None,
):
    """Plot ACF of squared returns showing long memory (slow hyperbolic decay).

    Useful for diagnosing FIGARCH-type long memory in volatility. The ACF
    of squared returns from a long memory process decays hyperbolically
    (slowly) rather than exponentially (fast) as in standard GARCH.

    Parameters
    ----------
    squared_returns : array-like
        Squared return series.
    max_lags : int
        Maximum number of lags to display.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save the figure.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    acf_values = acf(squared_returns, nlags=max_lags, fft=True)
    n = len(squared_returns)
    conf_bound = 1.96 / np.sqrt(n)

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Linear scale
    axes[0].bar(range(len(acf_values)), acf_values, width=1.0, color="steelblue", alpha=0.7)
    axes[0].axhline(y=conf_bound, color="red", linestyle="--", alpha=0.5)
    axes[0].axhline(y=-conf_bound, color="red", linestyle="--", alpha=0.5)
    axes[0].set_xlabel("Lag")
    axes[0].set_ylabel("ACF")
    axes[0].set_title("ACF (linear scale)")

    # Log-log scale to verify hyperbolic decay
    positive_lags = np.arange(1, len(acf_values))
    positive_acf = acf_values[1:]
    mask = positive_acf > 0
    if np.any(mask):
        axes[1].scatter(
            np.log(positive_lags[mask]),
            np.log(positive_acf[mask]),
            s=10,
            color="steelblue",
            alpha=0.7,
        )
        # Fit line to show decay rate
        x = np.log(positive_lags[mask])
        y = np.log(positive_acf[mask])
        if len(x) > 2:
            coeffs = np.polyfit(x, y, 1)
            axes[1].plot(
                x, np.polyval(coeffs, x), "r--", alpha=0.7, label=f"slope = {coeffs[0]:.3f}"
            )
            axes[1].legend()
    axes[1].set_xlabel("log(Lag)")
    axes[1].set_ylabel("log(ACF)")
    axes[1].set_title("ACF (log-log scale)")

    fig.suptitle(title, fontsize=13)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_realized_vs_conditional(
    dates,
    rv_daily,
    conditional_vol,
    title: str = "Realized vs Conditional Volatility",
    figsize: tuple = (14, 6),
    save_path: str = None,
):
    """Plot realized volatility against model-implied conditional volatility.

    Compares the ex-post realized volatility (from intraday data) with
    the conditional volatility from a fitted GARCH-type model.

    Parameters
    ----------
    dates : array-like
        Date index.
    rv_daily : array-like
        Daily realized volatility.
    conditional_vol : array-like
        Model-implied conditional volatility (sigma_t).
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save the figure.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)

    rv_sqrt = np.sqrt(np.asarray(rv_daily))

    axes[0].plot(
        dates, rv_sqrt, color="steelblue", alpha=0.6, linewidth=0.8, label="Realized Vol (sqrt RV)"
    )
    axes[0].plot(
        dates, conditional_vol, color="red", alpha=0.8, linewidth=0.8, label="Conditional Vol"
    )
    axes[0].set_ylabel("Volatility")
    axes[0].legend()
    axes[0].set_title(title)

    # Scatter
    axes[1].scatter(rv_sqrt, conditional_vol, s=5, alpha=0.3, color="steelblue")
    min_val = min(rv_sqrt.min(), np.asarray(conditional_vol).min())
    max_val = max(rv_sqrt.max(), np.asarray(conditional_vol).max())
    axes[1].plot([min_val, max_val], [min_val, max_val], "r--", alpha=0.5, label="45-degree line")
    axes[1].set_xlabel("Realized Vol")
    axes[1].set_ylabel("Conditional Vol")
    axes[1].legend()

    correlation = np.corrcoef(rv_sqrt, np.asarray(conditional_vol))[0, 1]
    axes[1].set_title(f"Scatter (corr = {correlation:.4f})")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_har_components(
    dates,
    rv_daily,
    rv_weekly,
    rv_monthly,
    title: str = "HAR-RV Components",
    figsize: tuple = (14, 8),
    save_path: str = None,
):
    """Plot HAR-RV components: daily, weekly, and monthly realized volatility.

    Visualizes the three time horizons of the Heterogeneous Autoregressive
    model: daily RV, weekly RV (5-day average), and monthly RV (22-day average).

    Parameters
    ----------
    dates : array-like
        Date index.
    rv_daily : array-like
        Daily realized volatility.
    rv_weekly : array-like
        Weekly (5-day average) realized volatility.
    rv_monthly : array-like
        Monthly (22-day average) realized volatility.
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save the figure.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)

    axes[0].plot(dates, rv_daily, color="steelblue", alpha=0.7, linewidth=0.8)
    axes[0].set_ylabel("RV Daily")
    axes[0].set_title(f"{title} - Daily Component")

    axes[1].plot(dates, rv_weekly, color="darkorange", alpha=0.8, linewidth=1.0)
    axes[1].set_ylabel("RV Weekly")
    axes[1].set_title("Weekly Component (5-day avg)")

    axes[2].plot(dates, rv_monthly, color="darkgreen", alpha=0.8, linewidth=1.0)
    axes[2].set_ylabel("RV Monthly")
    axes[2].set_title("Monthly Component (22-day avg)")
    axes[2].set_xlabel("Date")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_garchm_risk_premium(
    dates,
    returns,
    conditional_vol,
    risk_premium,
    title: str = "GARCH-M Risk Premium",
    figsize: tuple = (14, 8),
    save_path: str = None,
):
    """Plot GARCH-M returns, conditional volatility, and risk premium.

    Shows the relationship between returns, conditional volatility, and
    the time-varying risk premium (lambda * sigma_t) from a GARCH-M model.

    Parameters
    ----------
    dates : array-like
        Date index.
    returns : array-like
        Return series.
    conditional_vol : array-like
        Conditional volatility (sigma_t).
    risk_premium : array-like
        Risk premium component (lambda * sigma_t).
    title : str
        Plot title.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save the figure.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)

    axes[0].plot(dates, returns, color="steelblue", alpha=0.5, linewidth=0.5)
    axes[0].set_ylabel("Returns")
    axes[0].set_title(f"{title} - Returns")

    axes[1].plot(dates, conditional_vol, color="red", alpha=0.8, linewidth=0.8)
    axes[1].set_ylabel("Conditional Vol")
    axes[1].set_title("Conditional Volatility (sigma_t)")

    axes[2].plot(dates, risk_premium, color="darkgreen", alpha=0.8, linewidth=0.8)
    axes[2].axhline(
        y=np.mean(risk_premium),
        color="black",
        linestyle="--",
        alpha=0.5,
        label=f"Mean = {np.mean(risk_premium):.6f}",
    )
    axes[2].set_ylabel("Risk Premium")
    axes[2].set_xlabel("Date")
    axes[2].set_title("Risk Premium (lambda * sigma_t)")
    axes[2].legend()

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig
