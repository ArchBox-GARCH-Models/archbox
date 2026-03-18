"""Results container for threshold and STAR models.

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Annotated, Any

import numpy as np
from numpy.typing import NDArray

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


@dataclass
class TestResult:
    """Container for statistical test results."""

    statistic: float
    pvalue: float
    test_name: str
    detail: str = ""


@dataclass
class ThresholdResults:
    """Results container for threshold and STAR models.

    Attributes
    ----------
    model_name : str
        Name of the fitted model (e.g., 'TAR', 'LSTAR').
    params : dict[str, NDArray[np.float64]]
        Parameters per regime {'regime_1': array, 'regime_2': array}.
    threshold : float | list[float]
        Estimated threshold value(s) c.
    delay : int
        Delay parameter d.
    transition_params : dict[str, float]
        Transition parameters (e.g., {'gamma': ..., 'c': ...}).
    transition_params_array : NDArray[np.float64]
        Transition parameters as array for _transition_function.
    params_regime1 : NDArray[np.float64]
        AR parameters for regime 1.
    params_regime2 : NDArray[np.float64]
        AR parameters for regime 2.
    regime_assignments : NDArray[np.float64]
        Regime assignment for each observation (0 or 1 for hard, continuous for STAR).
    transition_values : NDArray[np.float64]
        G(s_t) for each observation t.
    resid : NDArray[np.float64]
        Residuals.
    sigma2 : dict[str, float]
        Variance per regime {'regime_1': sigma2_1, 'regime_2': sigma2_2}.
    loglike : float
        Log-likelihood.
    aic : float
        Akaike Information Criterion.
    bic : float
        Bayesian Information Criterion.
    nobs : int
        Number of effective observations.
    order : int
        AR order p.
    n_regimes : int
        Number of regimes.
    endog : NDArray[np.float64]
        Original endogenous series.
    linearity_test : TestResult | None
        Result of linearity test (if computed).
    """

    model_name: str
    params: dict[str, NDArray[np.float64]]
    threshold: float | list[float]
    delay: int
    transition_params: dict[str, float]
    transition_params_array: NDArray[np.float64]
    params_regime1: NDArray[np.float64]
    params_regime2: NDArray[np.float64]
    regime_assignments: NDArray[np.float64]
    transition_values: NDArray[np.float64]
    resid: NDArray[np.float64]
    sigma2: dict[str, float]
    loglike: float
    aic: float
    bic: float
    nobs: int
    order: int
    n_regimes: int
    endog: NDArray[np.float64]
    linearity_test: TestResult | None = None
    _model: Any = field(default=None, repr=False)

    def summary(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"{'Model':>35}: {self.model_name}")
        lines.append(f"{'Observations':>35}: {self.nobs}")
        lines.append(f"{'AR Order (p)':>35}: {self.order}")
        lines.append(f"{'Delay (d)':>35}: {self.delay}")
        lines.append(f"{'Number of Regimes':>35}: {self.n_regimes}")
        lines.append(f"{'Log-Likelihood':>35}: {self.loglike:.4f}")
        lines.append(f"{'AIC':>35}: {self.aic:.4f}")
        lines.append(f"{'BIC':>35}: {self.bic:.4f}")
        lines.append("-" * 70)

        # Threshold
        if isinstance(self.threshold, list):
            for i, c in enumerate(self.threshold):
                lines.append(f"{'Threshold c_' + str(i + 1):>35}: {c:.6f}")
        else:
            lines.append(f"{'Threshold (c)':>35}: {self.threshold:.6f}")

        # Transition parameters
        if self.transition_params:
            lines.append("-" * 70)
            lines.append("Transition Parameters:")
            for name, val in self.transition_params.items():
                lines.append(f"  {name:>30}: {val:.6f}")

        # Parameters per regime
        lines.append("-" * 70)
        for regime_name, regime_params in self.params.items():
            lines.append(f"{regime_name}:")
            param_labels = ["const"] + [f"phi_{i}" for i in range(1, len(regime_params))]
            for label, val in zip(param_labels, regime_params, strict=False):
                lines.append(f"  {label:>30}: {val:.6f}")

        # Variance per regime
        lines.append("-" * 70)
        lines.append("Variance per Regime:")
        for regime_name, s2 in self.sigma2.items():
            lines.append(f"  {regime_name:>30}: {s2:.6f}")

        # Linearity test
        if self.linearity_test is not None:
            lines.append("-" * 70)
            lines.append(f"Linearity Test ({self.linearity_test.test_name}):")
            lines.append(f"  {'Statistic':>30}: {self.linearity_test.statistic:.4f}")
            lines.append(f"  {'p-value':>30}: {self.linearity_test.pvalue:.4f}")

        lines.append("=" * 70)
        return "\n".join(lines)

    def plot_transition(self) -> Any:
        """Plot the estimated transition function G(s) vs s.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))

        g_vals = self.transition_values

        ax.scatter(range(len(g_vals)), g_vals, c="blue", alpha=0.3, s=5)
        ax.set_xlabel("Observation index")
        ax.set_ylabel("G(s_t)")
        ax.set_title(f"{self.model_name} - Transition Values Over Time")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def plot_regimes(self) -> Any:
        """Plot time series with regime coloring.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        # Top: time series with regime coloring
        ax1 = axes[0]
        n_obs = len(self.resid)
        y_fitted = self.endog[-n_obs:] - self.resid
        ax1.plot(
            range(n_obs),
            self.endog[-n_obs:],
            "k-",
            alpha=0.5,
            linewidth=0.8,
            label="Observed",
        )
        ax1.plot(range(n_obs), y_fitted, "b-", linewidth=1.0, label="Fitted")

        g_vals = self.transition_values
        for t in range(n_obs):
            if g_vals[t] > 0.5:
                ax1.axvspan(t - 0.5, t + 0.5, alpha=0.1, color="red")

        ax1.set_ylabel("y_t")
        ax1.set_title(f"{self.model_name} - Observed vs Fitted with Regime Coloring")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Bottom: transition values
        ax2 = axes[1]
        ax2.plot(range(n_obs), g_vals, "b-", linewidth=1.0)
        ax2.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("G(s_t)")
        ax2.set_title("Transition Values")
        ax2.set_ylim(-0.05, 1.05)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_phase_diagram(self) -> Any:
        """Plot y_t vs y_{t-1} colored by regime.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        n_obs = len(self.resid)
        y = self.endog[-n_obs:]
        y_lag = self.endog[-(n_obs + 1) : -1] if len(self.endog) > n_obs else y

        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(
            y_lag[:n_obs],
            y[:n_obs],
            c=self.transition_values[:n_obs],
            cmap="coolwarm",
            alpha=0.6,
            s=15,
        )
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def plot_fit(self) -> Any:
        """Plot observed vs fitted values.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        n_obs = len(self.resid)
        y_obs = self.endog[-n_obs:]
        y_fitted = y_obs - self.resid

        fig, axes = plt.subplots(2, 1, figsize=(12, 8))

        # Top: observed vs fitted
        ax1 = axes[0]
        ax1.plot(range(n_obs), y_obs, "k-", alpha=0.5, linewidth=0.8, label="Observed")
        ax1.plot(range(n_obs), y_fitted, "b-", linewidth=1.0, label="Fitted")
        ax1.set_ylabel("y_t")
        ax1.set_title(f"{self.model_name} - Observed vs Fitted")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Bottom: residuals
        ax2 = axes[1]
        ax2.plot(range(n_obs), self.resid, "r-", linewidth=0.8)
        ax2.axhline(y=0, color="gray", linestyle="--")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Residual")
        ax2.set_title("Residuals")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def forecast(self, horizon: int = 10) -> dict[str, NDArray[np.float64]]:
        """Generate forecasts using the fitted model.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast.
        """
        if self._model is not None:
            return self._model.forecast(self, horizon)
        msg = "Model reference not available for forecasting"
        raise RuntimeError(msg)
