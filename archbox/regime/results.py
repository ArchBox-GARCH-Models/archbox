"""Results container for Markov-Switching models."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray


class RegimeResults:
    """Container for Markov-Switching model results.

    Attributes
    ----------
    params : NDArray[np.float64]
        All estimated parameters, shape (n_params,).
    regime_params : dict[int, dict[str, float]]
        Parameters organized by regime.
    transition_matrix : NDArray[np.float64]
        Transition matrix P, shape (k, k). p_{ij} = P(S_t=j | S_{t-1}=i).
    filtered_probs : NDArray[np.float64]
        Filtered probabilities P(S_t=j | Y_t), shape (T, k).
    smoothed_probs : NDArray[np.float64]
        Smoothed probabilities P(S_t=j | Y_T), shape (T, k).
    predicted_probs : NDArray[np.float64]
        Predicted probabilities P(S_t=j | Y_{t-1}), shape (T, k).
    loglike : float
        Total log-likelihood.
    aic : float
        Akaike Information Criterion.
    bic : float
        Bayesian Information Criterion.
    nobs : int
        Number of observations.
    k_regimes : int
        Number of regimes.
    n_params : int
        Number of estimated parameters.
    model_name : str
        Name of the fitted model.
    param_names : list[str]
        Names of all parameters.
    converged : bool
        Whether estimation converged.
    n_iter : int
        Number of iterations to convergence.
    """

    def __init__(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def summary(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def expected_durations(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def ergodic_probabilities(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def classify(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(self.smoothed_probs, axis=1).astype(np.int64)

    def plot_regimes(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def plot_probabilities(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax
