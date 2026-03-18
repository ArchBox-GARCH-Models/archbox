"""Markov-Switching Mean and Mean-Variance models.

Implements the simplest Markov-Switching models:
- MarkovSwitchingMean: only the mean switches between regimes
- MarkovSwitchingMeanVar: both mean and variance switch

These are simplified versions of Hamilton (1989) without AR dynamics.

References
----------
Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle.
Econometrica, 57(2), 357-384.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.regime.base import MarkovSwitchingModel


class MarkovSwitchingMean(MarkovSwitchingModel):
    """Markov-Switching Mean model.

    Only the mean switches between regimes. The variance is constant
    across all regimes.

    y_t | S_t = s ~ N(mu_s, sigma^2)

    Parameters
    ----------
    endog : array-like
        Time series of observations, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_mean import MarkovSwitchingMean
    >>> y = np.random.randn(200)
    >>> model = MarkovSwitchingMean(y, k_regimes=2)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-Mean"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            [mu_0, ..., mu_{k-1}, sigma, trans_params].
        """
        k = self.k_regimes
        y = self.endog

        # Initialize means using quantiles
        quantiles = np.linspace(0, 1, k + 2)[1:-1]
        mus = np.quantile(y, quantiles)

        # Single sigma
        sigma = np.array([np.std(y)])

        # Transition params (k*(k-1) logit values, initialized to 0 = p=0.5)
        trans = np.zeros(k * (k - 1))

        return np.concatenate([mus, sigma, trans])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        names = [f"mu_{i}" for i in range(k)]
        names.append("sigma")
        names += [f"p_{i}{j}" for i in range(k) for j in range(k) if i != j]
        return names

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params


class MarkovSwitchingMeanVar(MarkovSwitchingModel):
    """Markov-Switching Mean-Variance model.

    Both mean and variance switch between regimes.

    y_t | S_t = s ~ N(mu_s, sigma_s^2)

    Parameters
    ----------
    endog : array-like
        Time series of observations, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_mean import MarkovSwitchingMeanVar
    >>> y = np.random.randn(200)
    >>> model = MarkovSwitchingMeanVar(y, k_regimes=2)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-Mean-Var"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params].
        """
        k = self.k_regimes
        y = self.endog

        # Initialize means using quantiles
        quantiles = np.linspace(0, 1, k + 2)[1:-1]
        mus = np.quantile(y, quantiles)

        # Initialize sigmas
        sigmas = np.full(k, np.std(y))

        # Transition params
        trans = np.zeros(k * (k - 1))

        return np.concatenate([mus, sigmas, trans])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        names = [f"mu_{i}" for i in range(k)]
        names += [f"sigma_{i}" for i in range(k)]
        names += [f"p_{i}{j}" for i in range(k) for j in range(k) if i != j]
        return names

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params
