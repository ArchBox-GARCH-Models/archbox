"""Base class for volatility models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

from archbox.utils.validation import validate_returns

if TYPE_CHECKING:
    from archbox.distributions.base import Distribution


class VolatilityModel(ABC):
    """Abstract base class for volatility models.

    All volatility models (GARCH, EGARCH, GJR-GARCH, etc.) inherit from this class.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' (demean) or 'zero'.
    dist : str
        Conditional distribution: 'normal', 'studentt', 'skewt'.

    Attributes
    ----------
    endog : NDArray[np.float64]
        Returns (demeaned if mean='constant').
    nobs : int
        Number of observations.
    dist : Distribution
        Conditional distribution instance.
    volatility_process : str
        Name of the volatility process.
    mu : float
        Estimated mean (0 if mean='zero').
    """

    volatility_process: str = "Unknown"

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    @staticmethod
    def _build_distribution(dist: str) -> Distribution:
        """Build a distribution instance from name."""
        from archbox.distributions.normal import Normal

        if dist == "normal":
            return Normal()
        msg = f"Unknown distribution: {dist}. Available: 'normal'."
        raise ValueError(msg)

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series.

        Parameters
        ----------
        params : ndarray
            Model parameters (omega, alpha, beta, ...).
        resids : ndarray
            Residuals (eps_t = r_t - mu).
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t, shape (T,).
        """

    @property
    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names."""

    @abstractmethod
    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained parameters to constrained space."""

    @abstractmethod
    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained parameters to unconstrained space."""

    @abstractmethod
    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer [(lower, upper), ...]."""

    @property
    @abstractmethod
    def num_params(self) -> int:
        """Number of model parameters."""

    # --- Concrete methods ---

    def fit(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    def loglike(self, params: NDArray[np.float64], backcast: float | None = None) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def loglike_per_obs(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def simulate(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def _backcast(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)
