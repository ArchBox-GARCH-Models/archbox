"""Base class for threshold and STAR models.

All threshold models (TAR, SETAR, LSTAR, ESTAR) inherit from ThresholdModel.

References
----------
- Tong, H. (1978). On a Threshold Model.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from numpy.typing import NDArray


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
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

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
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names."""

    # --- Concrete methods ---

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
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def forecast(self, results: Any, horizon: int = 10) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def simulate(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
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
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

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
        beta = np.linalg.lstsq(x_mat, y, rcond=None)[0]
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
