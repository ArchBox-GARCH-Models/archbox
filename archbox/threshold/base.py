"""Base class for threshold and STAR models.

All threshold models (TAR, SETAR, LSTAR, ESTAR) inherit from ThresholdModel.

References
----------
- Tong, H. (1978). On a Threshold Model.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

import numpy as np
from numpy.typing import NDArray


def count_params(
    n_regimes: int,
    order: int,
    n_transition: int,
    n_variances: int,
    include_delay: bool = False,
) -> int:
    """Count estimated parameters of a threshold model (for AIC/BIC).

    Parameters
    ----------
    n_regimes : int
        Number of regimes (each contributing ``order + 1`` AR coefficients).
    order : int
        AR order p.
    n_transition : int
        Number of transition parameters (thresholds for TAR/SETAR,
        gamma and c for LSTAR/ESTAR).
    n_variances : int
        Number of estimated innovation variances (one per regime for
        hard-threshold models, one in total for the homoskedastic STAR models).
    include_delay : bool
        Whether the delay d was estimated from the data (adds one parameter).

    Returns
    -------
    int
        Total number of estimated parameters.
    """
    return n_regimes * (order + 1) + n_transition + n_variances + (1 if include_delay else 0)


class ThresholdModel(ABC):
    """Abstract base class for threshold and smooth transition AR models.

    Parameters
    ----------
    endog : array-like
        Endogenous time series (1D).
    order : int
        AR order p.
    delay : int
        Delay parameter d for the transition variable s_t = y_{t-d}.
    n_regimes : int
        Number of regimes (2 or 3).

    Attributes
    ----------
    endog : NDArray[np.float64]
        Endogenous time series.
    nobs : int
        Number of observations.
    order : int
        AR order p.
    delay : int
        Delay parameter d.
    n_regimes : int
        Number of regimes.
    """

    model_name: str = "ThresholdModel"

    def __init__(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes
        # Exogenous threshold variable (set by TAR when threshold_var is given).
        self._threshold_var: NDArray[np.float64] | None = None

        if not np.all(np.isfinite(self.endog)):
            n_bad = int(np.sum(~np.isfinite(self.endog)))
            msg = (
                f"endog contains {n_bad} non-finite value(s) (NaN or inf); "
                "threshold models require a complete series."
            )
            raise ValueError(msg)

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def _build_matrices(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        return self._build_for_delay(self.delay)

    def _build_for_delay(
        self, d: int, start: int | None = None
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build (y, X, s) for a given delay and (optionally) a fixed start index.

        Parameters
        ----------
        d : int
            Delay parameter.
        start : int, optional
            First time index of the effective sample. Default ``max(order, d)``.
            Passing a common start makes samples for different delays
            comparable (same effective length).

        Returns
        -------
        y, X, s : tuple of ndarrays
        """
        p = self.order
        if start is None:
            start = max(p, d)
        if start < max(p, d):
            msg = f"start={start} is too small for order={p}, delay={d}"
            raise ValueError(msg)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        if self._threshold_var is not None:
            s = self._threshold_var[start - d : self.nobs - d]
        else:
            s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute transition function G(s; params).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Transition function parameters (e.g., gamma, c).

        Returns
        -------
        ndarray
            Transition values in [0, 1], same shape as s.
        """

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names."""

    # --- Concrete methods ---

    def regime_weights(self, g_values: NDArray[np.float64]) -> NDArray[np.float64]:
        """Convert transition values G(s_t) into per-regime weights.

        For two regimes the weights are ``[1 - G, G]``. For three regimes the
        weights are the piecewise-linear "tent" functions of G, so that
        G = 0, 0.5, 1 select regime 1, 2, 3 exactly (this is the convention
        used by the indicator transition of SETAR/TAR with two thresholds).

        Parameters
        ----------
        g_values : ndarray, shape (n,)
            Transition values in [0, 1].

        Returns
        -------
        ndarray, shape (n, n_regimes)
            Non-negative weights summing to one along axis 1.
        """
        g = np.asarray(g_values, dtype=np.float64).ravel()
        if self.n_regimes == 2:
            return np.column_stack([1.0 - g, g])
        w1 = np.clip(1.0 - 2.0 * g, 0.0, 1.0)
        w3 = np.clip(2.0 * g - 1.0, 0.0, 1.0)
        w2 = 1.0 - w1 - w3
        return np.column_stack([w1, w2, w3])

    def fitted_values(
        self,
        x_mat: NDArray[np.float64],
        g_values: NDArray[np.float64],
        params_regimes: Sequence[NDArray[np.float64]],
    ) -> NDArray[np.float64]:
        """Conditional mean implied by regime parameters and transition values.

        Parameters
        ----------
        x_mat : ndarray, shape (n, p+1)
            Design matrix.
        g_values : ndarray, shape (n,)
            Transition values G(s_t).
        params_regimes : sequence of ndarray
            AR parameters per regime.

        Returns
        -------
        ndarray, shape (n,)
            Fitted values.
        """
        weights = self.regime_weights(g_values)
        fitted = np.zeros(x_mat.shape[0])
        for i, beta in enumerate(params_regimes):
            fitted += weights[:, i] * (x_mat @ np.asarray(beta, dtype=np.float64))
        return fitted

    def fit(self, method: str = "cls") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "cls":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(msg)

        return self._fit_cls()

    @abstractmethod
    def _fit_cls(self) -> Any:
        """Conditional Least Squares estimation (subclass implements)."""

    def loglike(
        self,
        params_regimes: Sequence[NDArray[np.float64]],
        sigma2: Sequence[float],
        g_values: NDArray[np.float64],
    ) -> float:
        """Gaussian log-likelihood of the threshold model on the fitted sample.

        Parameters
        ----------
        params_regimes : sequence of ndarray
            AR parameters per regime (length ``n_regimes``).
        sigma2 : sequence of float
            Innovation variance per regime (length ``n_regimes``). For a
            homoskedastic model pass the same value for every regime.
        g_values : ndarray, shape (T_eff,)
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        weights = self.regime_weights(g_values)
        fitted = self.fitted_values(self._X, g_values, params_regimes)
        resid = y - fitted

        sig = np.asarray(sigma2, dtype=np.float64).ravel()
        if sig.size != weights.shape[1]:
            msg = f"sigma2 must have {weights.shape[1]} entries, got {sig.size}"
            raise ValueError(msg)
        sigma2_t = np.maximum(weights @ sig, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2_t) + resid**2 / sigma2_t)
        return float(ll)

    def _threshold_value_at(self, y_path: NDArray[np.float64], t: int) -> float:
        """Value of the transition variable used to predict observation ``t``.

        Parameters
        ----------
        y_path : ndarray
            Series (history extended by already-computed forecasts).
        t : int
            Time index of the observation being predicted.

        Returns
        -------
        float
            s_t.
        """
        idx = t - self.delay
        if self._threshold_var is not None:
            # Exogenous threshold variable: use its own (possibly future) value
            # when available, otherwise hold the last observed value.
            if idx >= len(self._threshold_var):
                idx = len(self._threshold_var) - 1
            return float(self._threshold_var[idx])
        return float(y_path[idx])

    def forecast(self, results: Any, horizon: int = 10) -> NDArray[np.float64]:
        """Point forecasts by deterministic (skeleton) iteration.

        The regime used at each step is the one implied by the transition
        variable of the forecast path, so a three-regime model uses the
        third regime's coefficients whenever the threshold variable is above
        the upper threshold.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        ndarray, shape (horizon,)
            Point forecasts.
        """
        if horizon < 1:
            msg = f"horizon must be >= 1, got {horizon}"
            raise ValueError(msg)

        if self._threshold_var is not None and horizon > self.delay:
            warnings.warn(
                "Forecast horizon exceeds the delay of the exogenous threshold "
                "variable; its last observed value is held constant beyond that "
                "point.",
                UserWarning,
                stacklevel=2,
            )

        y_path = np.concatenate([self.endog, np.zeros(horizon)])
        params_regimes = results.params_regimes

        for h in range(horizon):
            t = self.nobs + h
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                x[lag] = y_path[t - lag]

            s_val = self._threshold_value_at(y_path, t)
            g_val = self._transition_function(np.array([s_val]), results.transition_params_array)
            weights = self.regime_weights(g_val)[0]
            y_path[t] = float(
                sum(
                    weights[i] * float(x @ np.asarray(beta, dtype=np.float64))
                    for i, beta in enumerate(params_regimes)
                )
            )

        return y_path[self.nobs :].copy()

    def forecast_intervals(
        self,
        results: Any,
        horizon: int = 10,
        n_sims: int = 1000,
        alpha: float = 0.05,
        seed: int | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Simulation-based predictive distribution of future values.

        Future paths are generated by iterating the fitted model with Gaussian
        innovations whose variance is the (regime-weighted) fitted variance.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.
        n_sims : int
            Number of simulated paths.
        alpha : float
            Two-sided interval level (0.05 -> 95% interval).
        seed : int, optional
            Random seed.

        Returns
        -------
        dict
            Keys 'mean', 'median', 'lower', 'upper' (shape (horizon,)) and
            'paths' (shape (n_sims, horizon)).
        """
        if horizon < 1:
            msg = f"horizon must be >= 1, got {horizon}"
            raise ValueError(msg)
        if not 0.0 < alpha < 1.0:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        rng = np.random.default_rng(seed)
        sigma2 = np.array(
            [results.sigma2[f"regime_{i + 1}"] for i in range(self.n_regimes)],
            dtype=np.float64,
        )
        params_regimes = results.params_regimes
        paths = np.empty((n_sims, horizon))

        for sim in range(n_sims):
            y_path = np.concatenate([self.endog, np.zeros(horizon)])
            for h in range(horizon):
                t = self.nobs + h
                x = np.ones(self.order + 1)
                for lag in range(1, self.order + 1):
                    x[lag] = y_path[t - lag]
                s_val = self._threshold_value_at(y_path, t)
                g_val = self._transition_function(
                    np.array([s_val]), results.transition_params_array
                )
                weights = self.regime_weights(g_val)[0]
                mean = sum(
                    weights[i] * float(x @ np.asarray(beta, dtype=np.float64))
                    for i, beta in enumerate(params_regimes)
                )
                sd = float(np.sqrt(max(float(weights @ sigma2), 1e-12)))
                y_path[t] = mean + sd * rng.standard_normal()
            paths[sim] = y_path[self.nobs :]

        return {
            "mean": paths.mean(axis=0),
            "median": np.median(paths, axis=0),
            "lower": np.quantile(paths, alpha / 2.0, axis=0),
            "upper": np.quantile(paths, 1.0 - alpha / 2.0, axis=0),
            "paths": paths,
        }

    def simulate(
        self,
        n: int,
        params_regimes: Sequence[NDArray[np.float64]],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regimes : sequence of ndarray
            AR parameters per regime, each [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        if len(params_regimes) != self.n_regimes:
            msg = f"params_regimes must have {self.n_regimes} entries, got {len(params_regimes)}"
            raise ValueError(msg)

        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma
        betas = [np.asarray(b, dtype=np.float64) for b in params_regimes]

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            g_val = self._transition_function(np.array([y[t - d]]), transition_params)
            weights = self.regime_weights(g_val)[0]
            y[t] = sum(weights[i] * float(x @ beta) for i, beta in enumerate(betas)) + eps[t]

        return y[burn:]

    def plot_transition(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def plot_phase_diagram(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    @staticmethod
    def _ols_fit(
        y: NDArray[np.float64], x_mat: NDArray[np.float64]
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS regression returning coefficients, residuals, and RSS.

        Parameters
        ----------
        y : ndarray, shape (n,)
            Dependent variable.
        x_mat : ndarray, shape (n, k)
            Regressors.

        Returns
        -------
        beta : ndarray, shape (k,)
            OLS coefficients.
        resid : ndarray, shape (n,)
            Residuals.
        rss : float
            Residual sum of squares.
        """
        beta = np.linalg.lstsq(x_mat, y, rcond=None)[0].astype(np.float64)
        resid = y - x_mat @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    @staticmethod
    def _ols_rss(y: NDArray[np.float64], x_mat: NDArray[np.float64]) -> float:
        """Compute RSS from OLS regression.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Regressors.

        Returns
        -------
        float
            Residual sum of squares.
        """
        beta = np.linalg.lstsq(x_mat, y, rcond=None)[0]
        resid = y - x_mat @ beta
        return float(np.sum(resid**2))
