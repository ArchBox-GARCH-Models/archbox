"""News Impact Curve for asymmetric volatility models.

The news impact curve shows how past shocks eps_{t-1} affect the current
conditional variance sigma^2_t, holding all else constant.

References
----------
- Engle, R.F. & Ng, V.K. (1993). Measuring and Testing the Impact of News on Volatility.
  Journal of Finance, 48(5), 1749-1778.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray


def news_impact_curve(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def plot_news_impact(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def compare_news_impact(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax
