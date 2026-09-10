"""Base class for Markov-Switching models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

from archbox.regime.hamilton_filter import HamiltonFilter

if TYPE_CHECKING:
    from archbox.regime.results import RegimeResults


class MarkovSwitchingModel(ABC):
    """Abstract base class for Markov-Switching models.

    All Markov-Switching models (MS-AR, MS-GARCH, MS-VAR, etc.) inherit
    from this class.

    Notes
    -----
    The transition matrix is parameterised by a multinomial logit
    (softmax) on each row, with the diagonal element as the reference
    category::

        p_{ij} = exp(z_{ij}) / (1 + sum_{l != i} exp(z_{il})),  j != i
        p_{ii} = 1 / (1 + sum_{l != i} exp(z_{il}))

    This gives ``k * (k - 1)`` unconstrained parameters and a valid
    stochastic matrix for any number of regimes (the earlier
    element-wise logistic parametrisation could produce negative
    diagonals for ``k >= 3``).

    Models whose conditional density is undefined for the first
    ``_t_start`` observations (e.g. MS-AR(p) needs p pre-sample lags)
    condition on them: the filter, the likelihood and the M-step all
    start at ``t = _t_start`` and ``nobs_effective`` observations are
    used.

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

        # Number of initial observations that are conditioned on
        # (their conditional density is not part of the likelihood).
        self._t_start = 0

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None
        self._init_probs: NDArray[np.float64] | None = None
        self._params: NDArray[np.float64] | None = None
        self._last_filtered_probs: NDArray[np.float64] | None = None

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t = regime, Y_{t-1}, theta) for all t.

        Entries for ``t < self._t_start`` are undefined (they are set to
        zero and excluded from the likelihood).

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

    @property
    def nobs_effective(self) -> int:
        """Number of observations entering the likelihood."""
        return self.nobs - self._t_start

    def _regime_loglikes(self, params: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute the (T, k) matrix of regime conditional log-densities.

        Subclasses whose regimes share expensive intermediate quantities
        (e.g. MS-GARCH) should override this for efficiency.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        ndarray
            Log densities, shape (T, k).
        """
        out = np.empty((self.nobs, self.k_regimes))
        for s in range(self.k_regimes):
            out[:, s] = self._regime_loglike(params, s)
        return out

    def fit(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
        compute_se: bool = True,
        disp: bool | None = None,
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
        compute_se : bool
            Compute numerical-Hessian standard errors at the final params.
        disp : bool, optional
            Alias for ``verbose`` (kept for API consistency with the
            univariate models). Overrides ``verbose`` when given.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        if disp is not None:
            verbose = bool(disp)

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
            compute_se=compute_se,
        )
        self._is_fitted = True
        return results

    def loglike(
        self,
        params: NDArray[np.float64],
        init_probs: NDArray[np.float64] | None = None,
    ) -> float:
        """Compute total log-likelihood via the Hamilton filter.

        The first ``_t_start`` observations are conditioned on.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        init_probs : ndarray, optional
            Initial state distribution. Defaults to the distribution
            estimated by EM (when the model has been fitted) and to the
            ergodic distribution otherwise.

        Returns
        -------
        float
            Total log-likelihood.
        """
        params = np.asarray(params, dtype=np.float64)
        transition_matrix = self._extract_transition_matrix(params)
        regime_loglikes = self._regime_loglikes(params)[self._t_start :]

        if init_probs is None:
            init_probs = self._init_probs

        hfilter = HamiltonFilter()
        _, _, loglike, _ = hfilter.filter_vectorized(regime_loglikes, transition_matrix, init_probs)
        return loglike

    # --- Forecasting ---

    def _regime_forecast_moments(
        self,
        params: NDArray[np.float64],
        horizon: int,
        regime_probs: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Regime-conditional forecast moments.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        horizon : int
            Forecast horizon.
        regime_probs : ndarray
            Predicted regime probabilities, shape (horizon, k). Used by
            models that need the mixture path (iterated forecasts).

        Returns
        -------
        tuple
            (means, variances). For univariate models the shapes are
            (horizon, k) and (horizon, k); for multivariate models they
            are (horizon, k, n) and (horizon, k, n, n).
        """
        msg = f"{type(self).__name__} does not implement forecasting"
        raise NotImplementedError(msg)

    def forecast(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Regime probabilities are propagated with the transition matrix
        starting from the last filtered probabilities; the predictive
        mean and variance are the corresponding mixture moments of the
        regime-conditional forecasts.

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
            - 'mean': forecast mean, shape (horizon,) or (horizon, n)
            - 'variance': forecast variance, shape (horizon,) or
              (horizon, n, n)
            - 'regime_probs': regime probabilities, shape (horizon, k)
        """
        if horizon < 1:
            msg = f"horizon must be >= 1, got {horizon}"
            raise ValueError(msg)

        if params is None:
            params = self._params
        if params is None:
            msg = "No parameters available. Fit the model first or pass params."
            raise RuntimeError(msg)
        params = np.asarray(params, dtype=np.float64)

        if transition_matrix is None:
            transition_matrix = self._transition_matrix
        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = np.asarray(transition_matrix, dtype=np.float64)

        if last_probs is None:
            last_probs = self._last_filtered_probs
        if last_probs is None:
            last_probs = HamiltonFilter.ergodic_probabilities(trans)
        probs = np.asarray(last_probs, dtype=np.float64).copy()
        probs = np.maximum(probs, 0.0)
        probs /= max(float(probs.sum()), 1e-300)

        regime_probs = np.zeros((horizon, k))
        for h in range(horizon):
            probs = trans.T @ probs
            probs = np.maximum(probs, 0.0)
            probs /= max(float(probs.sum()), 1e-300)
            regime_probs[h] = probs

        means, variances = self._regime_forecast_moments(params, horizon, regime_probs)

        if means.ndim == 2:
            mean = np.einsum("hk,hk->h", regime_probs, means)
            second = np.einsum("hk,hk->h", regime_probs, variances + means**2)
            variance = np.maximum(second - mean**2, 0.0)
        else:
            mean = np.einsum("hk,hkn->hn", regime_probs, means)
            outer = np.einsum("hkn,hkm->hknm", means, means)
            second = np.einsum("hk,hknm->hnm", regime_probs, variances + outer)
            variance = second - np.einsum("hn,hm->hnm", mean, mean)

        return {"mean": mean, "variance": variance, "regime_probs": regime_probs}

    # --- Simulation ---

    def _simulate_observations(
        self,
        params: NDArray[np.float64],
        regimes: NDArray[np.int64],
        rng: np.random.Generator,
    ) -> NDArray[np.float64]:
        """Draw observations given a simulated regime path.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        regimes : ndarray
            Simulated regime path, shape (n,).
        rng : numpy Generator
            Random number generator.

        Returns
        -------
        ndarray
            Simulated observations, shape (n,) or (n, n_vars).
        """
        msg = f"{type(self).__name__} does not implement simulation"
        raise NotImplementedError(msg)

    def simulate(
        self,
        n: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.int64], NDArray[np.float64]]:
        """Simulate data from the model.

        The regime path is drawn from the Markov chain (started from its
        ergodic distribution) and the observations are drawn from the
        regime-conditional distribution implied by ``params``.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,) or (n, n_vars)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime indicators, shape (n, k)
        """
        if n < 1:
            msg = f"n must be >= 1, got {n}"
            raise ValueError(msg)

        rng = np.random.default_rng(seed)

        if params is None:
            params = self._params
        if params is None:
            msg = "No parameters available. Fit the model first or pass params."
            raise RuntimeError(msg)
        params = np.asarray(params, dtype=np.float64)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = np.asarray(transition_matrix, dtype=np.float64)
        ergodic = HamiltonFilter.ergodic_probabilities(trans)

        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = int(rng.choice(k, p=ergodic))
        for t in range(1, n):
            regimes[t] = int(rng.choice(k, p=trans[regimes[t - 1]]))

        y = self._simulate_observations(params, regimes, rng)

        probs = np.zeros((n, k))
        probs[np.arange(n), regimes] = 1.0

        return y, regimes, probs

    # --- Transition matrix parametrisation ---

    @staticmethod
    def _transition_matrix_from_logits(
        logits: NDArray[np.float64],
        k: int,
    ) -> NDArray[np.float64]:
        """Build a stochastic matrix from multinomial-logit row parameters.

        Parameters
        ----------
        logits : ndarray
            Row logits, shape (k*(k-1),), ordered as
            (i, j) for i in 0..k-1, j != i.
        k : int
            Number of regimes.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            z = np.zeros(k)
            for j in range(k):
                if j != i:
                    z[j] = np.clip(float(logits[idx]), -30.0, 30.0)
                    idx += 1
            z -= z.max()
            e = np.exp(z)
            p_mat[i] = e / e.sum()
        return p_mat

    @staticmethod
    def _transition_matrix_to_logits(
        p_mat: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Invert :meth:`_transition_matrix_from_logits`.

        Parameters
        ----------
        p_mat : ndarray
            Transition matrix, shape (k, k).

        Returns
        -------
        ndarray
            Row logits, shape (k*(k-1),).
        """
        k = p_mat.shape[0]
        logits: list[float] = []
        for i in range(k):
            p_ii = max(float(p_mat[i, i]), 1e-12)
            for j in range(k):
                if j != i:
                    p_ij = max(float(p_mat[i, j]), 1e-12)
                    logits.append(float(np.clip(np.log(p_ij / p_ii), -30.0, 30.0)))
        return np.array(logits, dtype=np.float64)

    def _extract_transition_matrix(self, params: NDArray[np.float64]) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        The last ``k*(k-1)`` parameters are the multinomial-logit row
        parameters of P (diagonal = reference category).

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
        return self._transition_matrix_from_logits(np.asarray(params[-n_trans:]), k)

    def _set_transition_params(
        self,
        params: NDArray[np.float64],
        p_mat: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Write a transition matrix back into a parameter vector.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        p_mat : ndarray
            Transition matrix, shape (k, k).

        Returns
        -------
        ndarray
            Parameter vector with updated transition block.
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        new_params = np.asarray(params, dtype=np.float64).copy()
        new_params[-n_trans:] = self._transition_matrix_to_logits(p_mat)
        return new_params

    def _regime_coefficients(
        self,
        params: NDArray[np.float64],
    ) -> tuple[list[NDArray[np.float64]], list[NDArray[np.float64]]] | None:
        """Regime-specific (coefficients, intercepts), or None.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        tuple or None
            (coefficients, intercepts) per regime when the model has
            autoregressive coefficients, else None.
        """
        return None

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
