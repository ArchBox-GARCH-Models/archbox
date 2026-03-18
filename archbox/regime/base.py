"""Base class for Markov-Switching models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from archbox.regime.results import RegimeResults


class MarkovSwitchingModel(ABC):
    """Abstract base class for Markov-Switching models.

    All Markov-Switching models (MS-AR, MS-GARCH, MS-VAR, etc.) inherit
    from this class.

    Parameters
    ----------
    endog : array-like
        Time series of observations. Shape (T,) for univariate,
        (T, n) for multivariate.
    k_regimes : int
        Number of regimes (states). Default is 2.
    order : int
        Autoregressive order (number of lags). Default is 1.
    switching_mean : bool
        If True, the mean switches between regimes.
    switching_variance : bool
        If True, the variance switches between regimes.
    switching_ar : bool
        If True, the AR coefficients switch between regimes.

    Attributes
    ----------
    endog : NDArray[np.float64]
        Observations array.
    nobs : int
        Number of observations.
    k_regimes : int
        Number of regimes.
    order : int
        Autoregressive order.
    switching_mean : bool
        Whether the mean switches.
    switching_variance : bool
        Whether the variance switches.
    switching_ar : bool
        Whether AR coefficients switch.
    """

    model_name: str = "MarkovSwitching"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t = regime, Y_{t-1}, theta) for all t.

        Parameters
        ----------
        params : ndarray
            All model parameters.
        regime : int
            Regime index (0, 1, ..., k_regimes-1).

        Returns
        -------
        ndarray
            Log-likelihood per observation for the given regime, shape (T,).
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

    def fit(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    def loglike(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def forecast(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def simulate(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def _extract_transition_matrix(self, params: NDArray[np.float64]) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    @staticmethod
    def _build_transition_matrix_from_diag(
        stay_probs: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Build transition matrix from staying probabilities (diagonal).

        For k=2: P = [[p00, 1-p00], [1-p11, p11]]

        Parameters
        ----------
        stay_probs : ndarray
            Staying probabilities [p_00, p_11, ...], shape (k,).

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = len(stay_probs)
        p_mat = np.zeros((k, k))
        for i in range(k):
            p_mat[i, i] = stay_probs[i]
            off_diag = (1.0 - stay_probs[i]) / max(k - 1, 1)
            for j in range(k):
                if i != j:
                    p_mat[i, j] = off_diag
        return p_mat
