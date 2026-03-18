"""EM Algorithm for Markov-Switching models.

Implements the Expectation-Maximization algorithm for parameter estimation
in Markov-Switching models. The E-step uses the Hamilton filter and Kim
smoother; the M-step updates the transition matrix and regime parameters.

References
----------
Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle.
Econometrica, 57(2), 357-384.

Hamilton, J.D. (1994). Time Series Analysis. Princeton University Press.
Chapter 22.

Kim, C.-J. & Nelson, C.R. (1999). State-Space Models with Regime Switching.
MIT Press.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from archbox.regime.hamilton_filter import HamiltonFilter
from archbox.regime.kim_smoother import KimSmoother
from archbox.regime.results import RegimeResults

if TYPE_CHECKING:
    from archbox.regime.base import MarkovSwitchingModel


class EMEstimator:
    """EM estimator for Markov-Switching models.

    Alternates between E-step (Hamilton filter + Kim smoother)
    and M-step (update parameters) until convergence.
    """

    def __init__(self) -> None:
        """Initialize EM estimator with Hamilton filter and Kim smoother."""
        self.hamilton_filter = HamiltonFilter()
        self.kim_smoother = KimSmoother()
        self.loglike_history: list[float] = []

    def fit(
        self,
        model: MarkovSwitchingModel,
        maxiter: int = 500,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit a Markov-Switching model using the EM algorithm.

        Parameters
        ----------
        model : MarkovSwitchingModel
            The model to fit.
        maxiter : int
            Maximum number of EM iterations.
        tol : float
            Convergence tolerance (relative change in log-likelihood).
        verbose : bool
            Print progress information.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        params = model.start_params.copy()
        k = model.k_regimes

        # Initialize transition matrix and initial state probs
        transition_matrix = model._extract_transition_matrix(params)
        init_probs: NDArray[np.float64] | None = None

        loglike_old = -np.inf
        converged = False
        self.loglike_history = []
        iteration = 0

        for iteration in range(maxiter):
            # === E-step ===
            # Compute regime log-likelihoods for all t, s
            t_obs = model.nobs
            regime_loglikes = np.zeros((t_obs, k))
            for s in range(k):
                regime_loglikes[:, s] = model._regime_loglike(params, s)

            # Hamilton filter (use consistent init_probs)
            filtered, predicted, loglike, _marginal = self.hamilton_filter.filter_vectorized(
                regime_loglikes, transition_matrix, init_probs
            )

            self.loglike_history.append(loglike)

            # Kim smoother (unnormalized for EM monotonicity)
            smoothed = self._smooth_unnormalized(filtered, predicted, transition_matrix)

            # Joint smoothed probabilities (unnormalized for EM monotonicity)
            joint_smoothed = self._compute_joint_smoothed(
                filtered, predicted, smoothed, transition_matrix
            )

            # === Check convergence ===
            if abs(loglike_old) > 1e-12:
                rel_change = abs(loglike - loglike_old) / abs(loglike_old)
            else:
                rel_change = abs(loglike - loglike_old)

            if verbose and iteration % 10 == 0:
                print(
                    f"  EM iter {iteration:4d}: "
                    f"loglike = {loglike:12.4f}, "
                    f"rel_change = {rel_change:.2e}"
                )

            if iteration > 0 and rel_change < tol:
                converged = True
                if verbose:
                    print(
                        f"  EM converged at iteration {iteration} (rel_change = {rel_change:.2e})"
                    )
                break

            loglike_old = loglike

            # === M-step ===
            # Update transition matrix
            transition_matrix = self._update_transition_matrix(joint_smoothed, smoothed)

            # Update initial state probabilities from smoothed[0]
            init_probs = smoothed[0].copy()
            assert init_probs is not None
            init_sum = float(init_probs.sum())
            if init_sum > 0.0:
                init_probs /= init_sum
            else:
                init_probs = np.ones(k) / k
            init_probs = np.maximum(init_probs, 1e-12)
            init_probs /= float(init_probs.sum())  # type: ignore[union-attr]

            # Update regime-specific parameters
            params = self._m_step(model, params, smoothed, joint_smoothed)

        # Final E-step for results
        t_obs = model.nobs
        regime_loglikes = np.zeros((t_obs, k))
        for s in range(k):
            regime_loglikes[:, s] = model._regime_loglike(params, s)

        filtered, predicted, loglike, _ = self.hamilton_filter.filter_vectorized(
            regime_loglikes, transition_matrix
        )
        smoothed = self.kim_smoother.smooth_vectorized(filtered, predicted, transition_matrix)

        # Build regime params dict
        regime_params = self._extract_regime_params(model, params)

        # Store transition matrix on model
        model._transition_matrix = transition_matrix

        return RegimeResults(
            params=params,
            regime_params=regime_params,
            transition_matrix=transition_matrix,
            filtered_probs=filtered,
            smoothed_probs=smoothed,
            predicted_probs=predicted,
            loglike=loglike,
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    @staticmethod
    def _smooth_unnormalized(
        filtered_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute smoothed probabilities without per-step normalization.

        Avoids the normalization step that can break EM monotonicity
        by introducing bias in the M-step weights.

        Parameters
        ----------
        filtered_probs : ndarray
            Shape (T, k).
        predicted_probs : ndarray
            Shape (T, k).
        transition_matrix : ndarray
            Shape (k, k).

        Returns
        -------
        ndarray
            Smoothed probabilities, shape (T, k).
        """
        n_obs, k = filtered_probs.shape
        trans = transition_matrix
        smoothed = np.zeros((n_obs, k))
        smoothed[-1] = filtered_probs[-1]

        for t in range(n_obs - 2, -1, -1):
            pred_safe = np.maximum(predicted_probs[t + 1], 1e-300)
            ratio = smoothed[t + 1] / pred_safe
            correction = trans @ ratio
            smoothed[t] = filtered_probs[t] * correction

        return smoothed

    @staticmethod
    def _compute_joint_smoothed(
        filtered_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute joint smoothed probabilities without normalization.

        Preserves EM monotonicity by avoiding the per-timestep normalization
        that can introduce numerical errors in the M-step.

        Parameters
        ----------
        filtered_probs : ndarray
            Shape (T, k).
        predicted_probs : ndarray
            Shape (T, k).
        smoothed_probs : ndarray
            Shape (T, k).
        transition_matrix : ndarray
            Shape (k, k).

        Returns
        -------
        ndarray
            Joint smoothed probabilities, shape (T-1, k, k).
        """
        n_obs, k = filtered_probs.shape
        trans = transition_matrix
        joint = np.zeros((n_obs - 1, k, k))

        for t in range(n_obs - 1):
            pred_safe = np.maximum(predicted_probs[t + 1], 1e-300)
            for i in range(k):
                for j in range(k):
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_safe[j]
                    )

        return joint

    def _update_transition_matrix(
        self,
        joint_smoothed: NDArray[np.float64],
        smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Update transition matrix in M-step.

        p_{ij} = sum_{t=1}^{T-1} P(S_t=i, S_{t+1}=j | Y_T)
                 / sum_{t=1}^{T-1} P(S_t=i | Y_T)

        Parameters
        ----------
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).

        Returns
        -------
        ndarray
            Updated transition matrix, shape (k, k).
        """
        k = smoothed.shape[1]
        p_new = np.zeros((k, k))

        for i in range(k):
            denom = smoothed[:-1, i].sum()
            if denom > 1e-12:
                for j in range(k):
                    p_new[i, j] = joint_smoothed[:, i, j].sum() / denom
            else:
                p_new[i] = 1.0 / k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def _m_step(
        self,
        model: MarkovSwitchingModel,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """M-step: update regime-specific parameters.

        If the model has a custom _m_step method, use it.
        Otherwise, use a generic M-step for mean/variance models.

        Parameters
        ----------
        model : MarkovSwitchingModel
            The model being estimated.
        params : ndarray
            Current parameter vector.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameter vector.
        """
        if hasattr(model, "_m_step_update"):
            return model._m_step_update(params, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def _generic_m_step(
        self,
        model: MarkovSwitchingModel,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Generic M-step for mean/variance switching models.

        Updates regime means and variances using weighted least squares
        with smoothed probabilities as weights.

        Parameters
        ----------
        model : MarkovSwitchingModel
            The model.
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = model.k_regimes
        y = model.endog
        new_params = params.copy()

        # Update means
        if model.switching_mean:
            for s in range(k):
                weights = smoothed[:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[s] = np.sum(weights * y) / w_sum

        # Update variances
        if model.switching_variance:
            for s in range(k):
                weights = smoothed[:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    mu_s = new_params[s]
                    resid2 = (y - mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def _extract_regime_params(
        self,
        model: MarkovSwitchingModel,
        params: NDArray[np.float64],
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific parameters from the parameter vector.

        Parameters
        ----------
        model : MarkovSwitchingModel
            The model.
        params : ndarray
            Parameter vector.

        Returns
        -------
        dict
            Parameters organized by regime.
        """
        k = model.k_regimes

        if hasattr(model, "_extract_regime_params"):
            return model._extract_regime_params(params)  # type: ignore[attr-defined]

        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            rp: dict[str, float] = {}
            if model.switching_mean:
                rp["mu"] = float(params[s])
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params
