"""
Plot helpers for Threshold and STAR model examples.

Provides visualization functions for:
- Threshold regime identification
- Smooth transition functions
- STAR model surfaces
- Linearity test power analysis
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_threshold_regimes(y, threshold=0.0, delay=1, ax=None, title="SETAR Regime Classification"):
    """
    Scatter plot of y_t vs y_{t-d} colored by regime.

    Parameters
    ----------
    y : array-like
        Time series values.
    threshold : float
        Threshold value c (default: 0.0).
    delay : int
        Delay parameter d (default: 1).
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. If None, creates new figure.
    title : str
        Plot title.

    Returns
    -------
    matplotlib.axes.Axes
    """
    y = np.asarray(y)
    y_lag = y[:-delay]
    y_cur = y[delay:]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    regime1 = y_lag <= threshold
    regime2 = y_lag > threshold

    ax.scatter(
        y_lag[regime1],
        y_cur[regime1],
        alpha=0.5,
        s=15,
        label=f"Regime 1 (y_{{t-{delay}}} <= {threshold})",
        color="steelblue",
    )
    ax.scatter(
        y_lag[regime2],
        y_cur[regime2],
        alpha=0.5,
        s=15,
        label=f"Regime 2 (y_{{t-{delay}}} > {threshold})",
        color="coral",
    )
    ax.axvline(
        x=threshold,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label=f"Threshold c = {threshold}",
    )
    ax.set_xlabel(f"$y_{{t-{delay}}}$", fontsize=12)
    ax.set_ylabel("$y_t$", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def plot_transition_function(y, gamma, c, model_type="LSTAR", ax=None, title=None):
    """
    Plot the transition function G(y_{t-1}) against lagged values.

    Parameters
    ----------
    y : array-like
        Time series values (used to compute G over observed range).
    gamma : float
        Smoothness/speed parameter.
    c : float
        Location parameter (threshold).
    model_type : str
        'LSTAR' for logistic or 'ESTAR' for exponential.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on.
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.axes.Axes
    """
    y = np.asarray(y)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    s_grid = np.linspace(y.min() - 0.5, y.max() + 0.5, 500)

    if model_type.upper() == "LSTAR":
        G = 1.0 / (1.0 + np.exp(-gamma * (s_grid - c)))
        label = f"$G(s; \\gamma={gamma}, c={c}) = \\frac{{1}}{{1+e^{{-\\gamma(s-c)}}}}$"
    elif model_type.upper() == "ESTAR":
        G = 1.0 - np.exp(-gamma * (s_grid - c) ** 2)
        label = f"$G(s; \\gamma={gamma}, c={c}) = 1 - e^{{-\\gamma(s-c)^2}}$"
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    ax.plot(s_grid, G, linewidth=2, color="darkblue", label=label)
    ax.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)
    ax.axvline(x=c, color="red", linestyle="--", alpha=0.7, label=f"c = {c}")
    ax.set_xlabel("$s = y_{t-1}$", fontsize=12)
    ax.set_ylabel("$G(s)$", fontsize=12)

    if title is None:
        title = f"{model_type} Transition Function"
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    return ax


def plot_star_surface(gamma_range, c, phi_1, phi_2, model_type="LSTAR", ax=None, title=None):
    """
    3D surface of conditional mean as function of y_{t-1} and gamma.

    Parameters
    ----------
    gamma_range : tuple
        (min_gamma, max_gamma) range to plot.
    c : float
        Location parameter.
    phi_1 : float
        AR coefficient for regime 1.
    phi_2 : float
        AR coefficient for regime 2.
    model_type : str
        'LSTAR' or 'ESTAR'.
    ax : matplotlib.axes.Axes3D, optional
        3D axes to plot on.
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.axes.Axes3D
    """
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    y_grid = np.linspace(-4, 4, 100)
    gamma_grid = np.linspace(gamma_range[0], gamma_range[1], 100)
    Y, GAMMA = np.meshgrid(y_grid, gamma_grid)

    if model_type.upper() == "LSTAR":
        G = 1.0 / (1.0 + np.exp(-GAMMA * (Y - c)))
    elif model_type.upper() == "ESTAR":
        G = 1.0 - np.exp(-GAMMA * (Y - c) ** 2)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    E_y = phi_1 * Y * (1 - G) + phi_2 * Y * G

    if ax is None:
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(Y, GAMMA, E_y, cmap="coolwarm", alpha=0.8, edgecolor="none")
    ax.set_xlabel("$y_{t-1}$", fontsize=11)
    ax.set_ylabel("$\\gamma$", fontsize=11)
    ax.set_zlabel("$E[y_t | y_{t-1}]$", fontsize=11)

    if title is None:
        title = f"{model_type} Conditional Mean Surface"
    ax.set_title(title, fontsize=14)

    plt.colorbar(surf, ax=ax, shrink=0.5, pad=0.1)

    return ax


def plot_linearity_test_power(sample_sizes, powers, test_name="LM Test", ax=None, title=None):
    """
    Plot power curve of linearity test across sample sizes.

    Parameters
    ----------
    sample_sizes : array-like
        Sample sizes tested.
    powers : dict
        Dictionary mapping model names to arrays of rejection rates.
        Example: {'SETAR': [0.3, 0.5, 0.8], 'LSTAR': [0.4, 0.6, 0.9]}
    test_name : str
        Name of the test being analyzed.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on.
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    colors = ["steelblue", "coral", "forestgreen", "darkorange", "purple"]

    for i, (model_name, power_vals) in enumerate(powers.items()):
        color = colors[i % len(colors)]
        ax.plot(
            sample_sizes, power_vals, "o-", linewidth=2, markersize=6, color=color, label=model_name
        )

    ax.axhline(y=0.05, color="red", linestyle="--", alpha=0.7, label="Nominal size (5%)")
    ax.set_xlabel("Sample Size (n)", fontsize=12)
    ax.set_ylabel("Rejection Rate", fontsize=12)
    ax.set_ylim(0, 1.05)

    if title is None:
        title = f"{test_name} - Power Analysis"
    ax.set_title(title, fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax
