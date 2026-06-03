"""Plotting helpers for GARCH univariate examples.

Provides reusable visualisation functions used across the tutorial notebooks.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def plot_returns(returns: pd.Series, title: str = "Returns") -> plt.Figure:
    """Plot a time-series of returns.

    Parameters
    ----------
    returns : pd.Series
        Return series (index should be date-like or integer).
    title : str
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(returns.index, returns.values, linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Return")
    ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
    fig.tight_layout()
    return fig


def plot_volatility(volatility: pd.Series, title: str = "Conditional Volatility") -> plt.Figure:
    """Plot conditional volatility over time.

    Parameters
    ----------
    volatility : pd.Series
        Volatility (standard deviation) series.
    title : str
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(volatility.index, volatility.values, linewidth=0.8, color="darkorange")
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    fig.tight_layout()
    return fig


def plot_acf_pacf(residuals: np.ndarray, lags: int = 40) -> plt.Figure:
    """Plot ACF and PACF of standardised residuals.

    Parameters
    ----------
    residuals : array-like
        Standardised residuals.
    lags : int
        Number of lags to display.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    plot_acf(residuals, lags=lags, ax=axes[0], title="ACF of Std. Residuals")
    plot_pacf(residuals, lags=lags, ax=axes[1], title="PACF of Std. Residuals")
    fig.tight_layout()
    return fig


def plot_news_impact(model_result, title: str = "News Impact Curve") -> plt.Figure:
    """Plot the news impact curve from a fitted GARCH-type model.

    The news impact curve shows how past shocks (z_{t-1}) map into current
    conditional variance (sigma^2_t), holding all other information constant.

    Parameters
    ----------
    model_result : object
        A fitted archbox model result that exposes ``params`` and model
        specification attributes (omega, alpha, beta, gamma, etc.).
    title : str
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    params = model_result.params
    omega = params.get("omega", 0)
    alpha = params.get("alpha1", params.get("alpha", 0))
    beta = params.get("beta1", params.get("beta", 0))
    gamma = params.get("gamma1", params.get("gamma", 0))

    unconditional_var = omega / (1 - alpha - beta) if (alpha + beta) < 1 else omega
    z = np.linspace(-4, 4, 200)
    shock = z * np.sqrt(unconditional_var)

    # Standard GARCH news impact: sigma2_t = omega + alpha * shock^2 + beta * sigma2_{t-1}
    sigma2 = omega + alpha * shock**2 + beta * unconditional_var

    # If asymmetric (GJR-GARCH style), add leverage term
    if gamma != 0:
        sigma2 = sigma2 + gamma * (shock < 0) * shock**2

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(shock, sigma2, linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel(r"$\epsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.axvline(0, color="grey", linewidth=0.5, linestyle="--")
    fig.tight_layout()
    return fig


def plot_qq(residuals: np.ndarray, distribution: str = "normal") -> plt.Figure:
    """QQ-plot of residuals against a theoretical distribution.

    Parameters
    ----------
    residuals : array-like
        Residuals (ideally standardised).
    distribution : str
        Reference distribution: ``'normal'`` or ``'t'``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    if distribution == "t":
        # Fit degrees of freedom from data
        df_est = max(stats.t.fit(residuals)[0], 2.1)
        stats.probplot(residuals, dist=stats.t(df_est), plot=ax)
    else:
        stats.probplot(residuals, dist="norm", plot=ax)
    ax.set_title(f"QQ-Plot ({distribution})")
    fig.tight_layout()
    return fig


def plot_model_comparison(results_dict: dict) -> plt.Figure:
    """Bar-chart comparing information criteria across models.

    Parameters
    ----------
    results_dict : dict
        Mapping ``{model_name: result_object}``.  Each result object must
        expose ``aic``, ``bic``, and ``hqic`` attributes (or a dict with
        those keys).

    Returns
    -------
    matplotlib.figure.Figure
    """
    names = list(results_dict.keys())
    aic_vals, bic_vals, hqic_vals = [], [], []
    for res in results_dict.values():
        if isinstance(res, dict):
            aic_vals.append(res["aic"])
            bic_vals.append(res["bic"])
            hqic_vals.append(res.get("hqic", np.nan))
        else:
            aic_vals.append(getattr(res, "aic", np.nan))
            bic_vals.append(getattr(res, "bic", np.nan))
            hqic_vals.append(getattr(res, "hqic", np.nan))

    x = np.arange(len(names))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width, aic_vals, width, label="AIC")
    ax.bar(x, bic_vals, width, label="BIC")
    ax.bar(x + width, hqic_vals, width, label="HQIC")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=30, ha="right")
    ax.set_ylabel("Information Criterion")
    ax.set_title("Model Comparison")
    ax.legend()
    fig.tight_layout()
    return fig
