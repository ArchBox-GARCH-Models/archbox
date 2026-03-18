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
from collections.abc import Callable
from typing import Annotated, ClassVar

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


class EMEstimator:
    """EM estimator for Markov-Switching models.

    Alternates between E-step (Hamilton filter + Kim smoother)
    and M-step (update parameters) until convergence.
    """

    def __init__(self) -> None:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEMEstimatorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁEMEstimatorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEMEstimatorǁ__init____mutmut_orig(self) -> None:
        """Initialize EM estimator with Hamilton filter and Kim smoother."""
        self.hamilton_filter = HamiltonFilter()
        self.kim_smoother = KimSmoother()
        self.loglike_history: list[float] = []

    def xǁEMEstimatorǁ__init____mutmut_1(self) -> None:
        """Initialize EM estimator with Hamilton filter and Kim smoother."""
        self.hamilton_filter = None
        self.kim_smoother = KimSmoother()
        self.loglike_history: list[float] = []

    def xǁEMEstimatorǁ__init____mutmut_2(self) -> None:
        """Initialize EM estimator with Hamilton filter and Kim smoother."""
        self.hamilton_filter = HamiltonFilter()
        self.kim_smoother = None
        self.loglike_history: list[float] = []

    def xǁEMEstimatorǁ__init____mutmut_3(self) -> None:
        """Initialize EM estimator with Hamilton filter and Kim smoother."""
        self.hamilton_filter = HamiltonFilter()
        self.kim_smoother = KimSmoother()
        self.loglike_history: list[float] = None

    xǁEMEstimatorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEMEstimatorǁ__init____mutmut_1": xǁEMEstimatorǁ__init____mutmut_1,
        "xǁEMEstimatorǁ__init____mutmut_2": xǁEMEstimatorǁ__init____mutmut_2,
        "xǁEMEstimatorǁ__init____mutmut_3": xǁEMEstimatorǁ__init____mutmut_3,
    }
    xǁEMEstimatorǁ__init____mutmut_orig.__name__ = "xǁEMEstimatorǁ__init__"

    def fit(
        self,
        model: MarkovSwitchingModel,
        maxiter: int = 500,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        args = [model, maxiter, tol, verbose]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEMEstimatorǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁEMEstimatorǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEMEstimatorǁfit__mutmut_orig(
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

    def xǁEMEstimatorǁfit__mutmut_1(
        self,
        model: MarkovSwitchingModel,
        maxiter: int = 501,
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

    def xǁEMEstimatorǁfit__mutmut_2(
        self,
        model: MarkovSwitchingModel,
        maxiter: int = 500,
        tol: float = 1.00000001,
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

    def xǁEMEstimatorǁfit__mutmut_3(
        self,
        model: MarkovSwitchingModel,
        maxiter: int = 500,
        tol: float = 1e-8,
        verbose: bool = False,
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

    def xǁEMEstimatorǁfit__mutmut_4(
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
        params = None
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

    def xǁEMEstimatorǁfit__mutmut_5(
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
        k = None

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

    def xǁEMEstimatorǁfit__mutmut_6(
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
        transition_matrix = None
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

    def xǁEMEstimatorǁfit__mutmut_7(
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
        transition_matrix = model._extract_transition_matrix(None)
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

    def xǁEMEstimatorǁfit__mutmut_8(
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
        init_probs: NDArray[np.float64] | None = ""

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

    def xǁEMEstimatorǁfit__mutmut_9(
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

        loglike_old = None
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

    def xǁEMEstimatorǁfit__mutmut_10(
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

        loglike_old = +np.inf
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

    def xǁEMEstimatorǁfit__mutmut_11(
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
        converged = None
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

    def xǁEMEstimatorǁfit__mutmut_12(
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
        converged = True
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

    def xǁEMEstimatorǁfit__mutmut_13(
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
        self.loglike_history = None
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

    def xǁEMEstimatorǁfit__mutmut_14(
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
        iteration = None

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

    def xǁEMEstimatorǁfit__mutmut_15(
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
        iteration = 1

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

    def xǁEMEstimatorǁfit__mutmut_16(
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

        for iteration in range(None):
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

    def xǁEMEstimatorǁfit__mutmut_17(
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
            t_obs = None
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

    def xǁEMEstimatorǁfit__mutmut_18(
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
            regime_loglikes = None
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

    def xǁEMEstimatorǁfit__mutmut_19(
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
            regime_loglikes = np.zeros(None)
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

    def xǁEMEstimatorǁfit__mutmut_20(
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
            for s in range(None):
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

    def xǁEMEstimatorǁfit__mutmut_21(
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
                regime_loglikes[:, s] = None

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

    def xǁEMEstimatorǁfit__mutmut_22(
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
                regime_loglikes[:, s] = model._regime_loglike(None, s)

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

    def xǁEMEstimatorǁfit__mutmut_23(
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
                regime_loglikes[:, s] = model._regime_loglike(params, None)

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

    def xǁEMEstimatorǁfit__mutmut_24(
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
                regime_loglikes[:, s] = model._regime_loglike(s)

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

    def xǁEMEstimatorǁfit__mutmut_25(
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
                regime_loglikes[:, s] = model._regime_loglike(
                    params,
                )

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

    def xǁEMEstimatorǁfit__mutmut_26(
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
            filtered, predicted, loglike, _marginal = None

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

    def xǁEMEstimatorǁfit__mutmut_27(
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
                None, transition_matrix, init_probs
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

    def xǁEMEstimatorǁfit__mutmut_28(
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
                regime_loglikes, None, init_probs
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

    def xǁEMEstimatorǁfit__mutmut_29(
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
                regime_loglikes, transition_matrix, None
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

    def xǁEMEstimatorǁfit__mutmut_30(
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
                transition_matrix, init_probs
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

    def xǁEMEstimatorǁfit__mutmut_31(
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
                regime_loglikes, init_probs
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

    def xǁEMEstimatorǁfit__mutmut_32(
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
                regime_loglikes,
                transition_matrix,
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

    def xǁEMEstimatorǁfit__mutmut_33(
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

            self.loglike_history.append(None)

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

    def xǁEMEstimatorǁfit__mutmut_34(
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
            smoothed = None

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

    def xǁEMEstimatorǁfit__mutmut_35(
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
            smoothed = self._smooth_unnormalized(None, predicted, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_36(
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
            smoothed = self._smooth_unnormalized(filtered, None, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_37(
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
            smoothed = self._smooth_unnormalized(filtered, predicted, None)

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

    def xǁEMEstimatorǁfit__mutmut_38(
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
            smoothed = self._smooth_unnormalized(predicted, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_39(
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
            smoothed = self._smooth_unnormalized(filtered, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_40(
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
            smoothed = self._smooth_unnormalized(
                filtered,
                predicted,
            )

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

    def xǁEMEstimatorǁfit__mutmut_41(
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
            joint_smoothed = None

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

    def xǁEMEstimatorǁfit__mutmut_42(
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
                None, predicted, smoothed, transition_matrix
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

    def xǁEMEstimatorǁfit__mutmut_43(
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
                filtered, None, smoothed, transition_matrix
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

    def xǁEMEstimatorǁfit__mutmut_44(
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
                filtered, predicted, None, transition_matrix
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

    def xǁEMEstimatorǁfit__mutmut_45(
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
            joint_smoothed = self._compute_joint_smoothed(filtered, predicted, smoothed, None)

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

    def xǁEMEstimatorǁfit__mutmut_46(
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
            joint_smoothed = self._compute_joint_smoothed(predicted, smoothed, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_47(
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
            joint_smoothed = self._compute_joint_smoothed(filtered, smoothed, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_48(
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
            joint_smoothed = self._compute_joint_smoothed(filtered, predicted, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_49(
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
                filtered,
                predicted,
                smoothed,
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

    def xǁEMEstimatorǁfit__mutmut_50(
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
            if abs(None) > 1e-12:
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

    def xǁEMEstimatorǁfit__mutmut_51(
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
            if abs(loglike_old) >= 1e-12:
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

    def xǁEMEstimatorǁfit__mutmut_52(
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
            if abs(loglike_old) > 1.000000000001:
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

    def xǁEMEstimatorǁfit__mutmut_53(
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
                rel_change = None
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

    def xǁEMEstimatorǁfit__mutmut_54(
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
                rel_change = abs(loglike - loglike_old) * abs(loglike_old)
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

    def xǁEMEstimatorǁfit__mutmut_55(
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
                rel_change = abs(None) / abs(loglike_old)
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

    def xǁEMEstimatorǁfit__mutmut_56(
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
                rel_change = abs(loglike + loglike_old) / abs(loglike_old)
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

    def xǁEMEstimatorǁfit__mutmut_57(
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
                rel_change = abs(loglike - loglike_old) / abs(None)
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

    def xǁEMEstimatorǁfit__mutmut_58(
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
                rel_change = None

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

    def xǁEMEstimatorǁfit__mutmut_59(
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
                rel_change = abs(None)

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

    def xǁEMEstimatorǁfit__mutmut_60(
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
                rel_change = abs(loglike + loglike_old)

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

    def xǁEMEstimatorǁfit__mutmut_61(
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

            if verbose or iteration % 10 == 0:
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

    def xǁEMEstimatorǁfit__mutmut_62(
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

            if verbose and iteration / 10 == 0:
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

    def xǁEMEstimatorǁfit__mutmut_63(
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

            if verbose and iteration % 11 == 0:
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

    def xǁEMEstimatorǁfit__mutmut_64(
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

            if verbose and iteration % 10 != 0:
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

    def xǁEMEstimatorǁfit__mutmut_65(
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

            if verbose and iteration % 10 == 1:
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

    def xǁEMEstimatorǁfit__mutmut_66(
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
                print(None)

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

    def xǁEMEstimatorǁfit__mutmut_67(
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

            if iteration > 0 or rel_change < tol:
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

    def xǁEMEstimatorǁfit__mutmut_68(
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

            if iteration >= 0 and rel_change < tol:
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

    def xǁEMEstimatorǁfit__mutmut_69(
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

            if iteration > 1 and rel_change < tol:
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

    def xǁEMEstimatorǁfit__mutmut_70(
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

            if iteration > 0 and rel_change <= tol:
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

    def xǁEMEstimatorǁfit__mutmut_71(
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
                converged = None
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

    def xǁEMEstimatorǁfit__mutmut_72(
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
                converged = False
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

    def xǁEMEstimatorǁfit__mutmut_73(
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
                    print(None)
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

    def xǁEMEstimatorǁfit__mutmut_74(
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
                return

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

    def xǁEMEstimatorǁfit__mutmut_75(
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

            loglike_old = None

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

    def xǁEMEstimatorǁfit__mutmut_76(
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
            transition_matrix = None

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

    def xǁEMEstimatorǁfit__mutmut_77(
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
            transition_matrix = self._update_transition_matrix(None, smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_78(
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
            transition_matrix = self._update_transition_matrix(joint_smoothed, None)

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

    def xǁEMEstimatorǁfit__mutmut_79(
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
            transition_matrix = self._update_transition_matrix(smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_80(
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
            transition_matrix = self._update_transition_matrix(
                joint_smoothed,
            )

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

    def xǁEMEstimatorǁfit__mutmut_81(
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
            init_probs = None
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

    def xǁEMEstimatorǁfit__mutmut_82(
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
            init_probs = smoothed[1].copy()
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

    def xǁEMEstimatorǁfit__mutmut_83(
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
            assert init_probs is None
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

    def xǁEMEstimatorǁfit__mutmut_84(
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
            init_sum = None
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

    def xǁEMEstimatorǁfit__mutmut_85(
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
            init_sum = float(None)
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

    def xǁEMEstimatorǁfit__mutmut_86(
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
            if init_sum >= 0.0:
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

    def xǁEMEstimatorǁfit__mutmut_87(
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
            if init_sum > 1.0:
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

    def xǁEMEstimatorǁfit__mutmut_88(
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
                init_probs = init_sum
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

    def xǁEMEstimatorǁfit__mutmut_89(
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
                init_probs *= init_sum
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

    def xǁEMEstimatorǁfit__mutmut_90(
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
                init_probs = None
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

    def xǁEMEstimatorǁfit__mutmut_91(
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
                init_probs = np.ones(k) * k
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

    def xǁEMEstimatorǁfit__mutmut_92(
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
                init_probs = np.ones(None) / k
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

    def xǁEMEstimatorǁfit__mutmut_93(
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
            init_probs = None
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

    def xǁEMEstimatorǁfit__mutmut_94(
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
            init_probs = np.maximum(None, 1e-12)
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

    def xǁEMEstimatorǁfit__mutmut_95(
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
            init_probs = np.maximum(init_probs, None)
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

    def xǁEMEstimatorǁfit__mutmut_96(
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
            init_probs = np.maximum(1e-12)
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

    def xǁEMEstimatorǁfit__mutmut_97(
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
            init_probs = np.maximum(
                init_probs,
            )
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

    def xǁEMEstimatorǁfit__mutmut_98(
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
            init_probs = np.maximum(init_probs, 1.000000000001)
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

    def xǁEMEstimatorǁfit__mutmut_99(
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
            init_probs = float(init_probs.sum())  # type: ignore[union-attr]

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

    def xǁEMEstimatorǁfit__mutmut_100(
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
            init_probs *= float(init_probs.sum())  # type: ignore[union-attr]

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

    def xǁEMEstimatorǁfit__mutmut_101(
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
            init_probs /= float(None)  # type: ignore[union-attr]

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

    def xǁEMEstimatorǁfit__mutmut_102(
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
            params = None

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

    def xǁEMEstimatorǁfit__mutmut_103(
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
            params = self._m_step(None, params, smoothed, joint_smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_104(
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
            params = self._m_step(model, None, smoothed, joint_smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_105(
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
            params = self._m_step(model, params, None, joint_smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_106(
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
            params = self._m_step(model, params, smoothed, None)

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

    def xǁEMEstimatorǁfit__mutmut_107(
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
            params = self._m_step(params, smoothed, joint_smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_108(
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
            params = self._m_step(model, smoothed, joint_smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_109(
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
            params = self._m_step(model, params, joint_smoothed)

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

    def xǁEMEstimatorǁfit__mutmut_110(
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
            params = self._m_step(
                model,
                params,
                smoothed,
            )

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

    def xǁEMEstimatorǁfit__mutmut_111(
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
        t_obs = None
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

    def xǁEMEstimatorǁfit__mutmut_112(
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
        regime_loglikes = None
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

    def xǁEMEstimatorǁfit__mutmut_113(
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
        regime_loglikes = np.zeros(None)
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

    def xǁEMEstimatorǁfit__mutmut_114(
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
        for s in range(None):
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

    def xǁEMEstimatorǁfit__mutmut_115(
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
            regime_loglikes[:, s] = None

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

    def xǁEMEstimatorǁfit__mutmut_116(
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
            regime_loglikes[:, s] = model._regime_loglike(None, s)

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

    def xǁEMEstimatorǁfit__mutmut_117(
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
            regime_loglikes[:, s] = model._regime_loglike(params, None)

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

    def xǁEMEstimatorǁfit__mutmut_118(
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
            regime_loglikes[:, s] = model._regime_loglike(s)

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

    def xǁEMEstimatorǁfit__mutmut_119(
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
            regime_loglikes[:, s] = model._regime_loglike(
                params,
            )

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

    def xǁEMEstimatorǁfit__mutmut_120(
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

        filtered, predicted, loglike, _ = None
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

    def xǁEMEstimatorǁfit__mutmut_121(
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
            None, transition_matrix
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

    def xǁEMEstimatorǁfit__mutmut_122(
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
            regime_loglikes, None
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

    def xǁEMEstimatorǁfit__mutmut_123(
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

        filtered, predicted, loglike, _ = self.hamilton_filter.filter_vectorized(transition_matrix)
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

    def xǁEMEstimatorǁfit__mutmut_124(
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
            regime_loglikes,
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

    def xǁEMEstimatorǁfit__mutmut_125(
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
        smoothed = None

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

    def xǁEMEstimatorǁfit__mutmut_126(
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
        smoothed = self.kim_smoother.smooth_vectorized(None, predicted, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_127(
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
        smoothed = self.kim_smoother.smooth_vectorized(filtered, None, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_128(
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
        smoothed = self.kim_smoother.smooth_vectorized(filtered, predicted, None)

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

    def xǁEMEstimatorǁfit__mutmut_129(
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
        smoothed = self.kim_smoother.smooth_vectorized(predicted, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_130(
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
        smoothed = self.kim_smoother.smooth_vectorized(filtered, transition_matrix)

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

    def xǁEMEstimatorǁfit__mutmut_131(
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
        smoothed = self.kim_smoother.smooth_vectorized(
            filtered,
            predicted,
        )

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

    def xǁEMEstimatorǁfit__mutmut_132(
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
        regime_params = None

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

    def xǁEMEstimatorǁfit__mutmut_133(
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
        regime_params = self._extract_regime_params(None, params)

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

    def xǁEMEstimatorǁfit__mutmut_134(
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
        regime_params = self._extract_regime_params(model, None)

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

    def xǁEMEstimatorǁfit__mutmut_135(
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
        regime_params = self._extract_regime_params(params)

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

    def xǁEMEstimatorǁfit__mutmut_136(
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
        regime_params = self._extract_regime_params(
            model,
        )

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

    def xǁEMEstimatorǁfit__mutmut_137(
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
        model._transition_matrix = None

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

    def xǁEMEstimatorǁfit__mutmut_138(
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
            params=None,
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

    def xǁEMEstimatorǁfit__mutmut_139(
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
            regime_params=None,
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

    def xǁEMEstimatorǁfit__mutmut_140(
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
            transition_matrix=None,
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

    def xǁEMEstimatorǁfit__mutmut_141(
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
            filtered_probs=None,
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

    def xǁEMEstimatorǁfit__mutmut_142(
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
            smoothed_probs=None,
            predicted_probs=predicted,
            loglike=loglike,
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_143(
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
            predicted_probs=None,
            loglike=loglike,
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_144(
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
            loglike=None,
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_145(
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
            nobs=None,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_146(
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
            k_regimes=None,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_147(
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
            model_name=None,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_148(
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
            param_names=None,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_149(
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
            converged=None,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_150(
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
            n_iter=None,
        )

    def xǁEMEstimatorǁfit__mutmut_151(
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

    def xǁEMEstimatorǁfit__mutmut_152(
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

    def xǁEMEstimatorǁfit__mutmut_153(
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

    def xǁEMEstimatorǁfit__mutmut_154(
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

    def xǁEMEstimatorǁfit__mutmut_155(
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
            predicted_probs=predicted,
            loglike=loglike,
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_156(
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
            loglike=loglike,
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_157(
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
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_158(
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
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_159(
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
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_160(
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
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_161(
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
            converged=converged,
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_162(
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
            n_iter=iteration + 1,
        )

    def xǁEMEstimatorǁfit__mutmut_163(
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
        )

    def xǁEMEstimatorǁfit__mutmut_164(
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
            n_iter=iteration - 1,
        )

    def xǁEMEstimatorǁfit__mutmut_165(
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
            n_iter=iteration + 2,
        )

    xǁEMEstimatorǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEMEstimatorǁfit__mutmut_1": xǁEMEstimatorǁfit__mutmut_1,
        "xǁEMEstimatorǁfit__mutmut_2": xǁEMEstimatorǁfit__mutmut_2,
        "xǁEMEstimatorǁfit__mutmut_3": xǁEMEstimatorǁfit__mutmut_3,
        "xǁEMEstimatorǁfit__mutmut_4": xǁEMEstimatorǁfit__mutmut_4,
        "xǁEMEstimatorǁfit__mutmut_5": xǁEMEstimatorǁfit__mutmut_5,
        "xǁEMEstimatorǁfit__mutmut_6": xǁEMEstimatorǁfit__mutmut_6,
        "xǁEMEstimatorǁfit__mutmut_7": xǁEMEstimatorǁfit__mutmut_7,
        "xǁEMEstimatorǁfit__mutmut_8": xǁEMEstimatorǁfit__mutmut_8,
        "xǁEMEstimatorǁfit__mutmut_9": xǁEMEstimatorǁfit__mutmut_9,
        "xǁEMEstimatorǁfit__mutmut_10": xǁEMEstimatorǁfit__mutmut_10,
        "xǁEMEstimatorǁfit__mutmut_11": xǁEMEstimatorǁfit__mutmut_11,
        "xǁEMEstimatorǁfit__mutmut_12": xǁEMEstimatorǁfit__mutmut_12,
        "xǁEMEstimatorǁfit__mutmut_13": xǁEMEstimatorǁfit__mutmut_13,
        "xǁEMEstimatorǁfit__mutmut_14": xǁEMEstimatorǁfit__mutmut_14,
        "xǁEMEstimatorǁfit__mutmut_15": xǁEMEstimatorǁfit__mutmut_15,
        "xǁEMEstimatorǁfit__mutmut_16": xǁEMEstimatorǁfit__mutmut_16,
        "xǁEMEstimatorǁfit__mutmut_17": xǁEMEstimatorǁfit__mutmut_17,
        "xǁEMEstimatorǁfit__mutmut_18": xǁEMEstimatorǁfit__mutmut_18,
        "xǁEMEstimatorǁfit__mutmut_19": xǁEMEstimatorǁfit__mutmut_19,
        "xǁEMEstimatorǁfit__mutmut_20": xǁEMEstimatorǁfit__mutmut_20,
        "xǁEMEstimatorǁfit__mutmut_21": xǁEMEstimatorǁfit__mutmut_21,
        "xǁEMEstimatorǁfit__mutmut_22": xǁEMEstimatorǁfit__mutmut_22,
        "xǁEMEstimatorǁfit__mutmut_23": xǁEMEstimatorǁfit__mutmut_23,
        "xǁEMEstimatorǁfit__mutmut_24": xǁEMEstimatorǁfit__mutmut_24,
        "xǁEMEstimatorǁfit__mutmut_25": xǁEMEstimatorǁfit__mutmut_25,
        "xǁEMEstimatorǁfit__mutmut_26": xǁEMEstimatorǁfit__mutmut_26,
        "xǁEMEstimatorǁfit__mutmut_27": xǁEMEstimatorǁfit__mutmut_27,
        "xǁEMEstimatorǁfit__mutmut_28": xǁEMEstimatorǁfit__mutmut_28,
        "xǁEMEstimatorǁfit__mutmut_29": xǁEMEstimatorǁfit__mutmut_29,
        "xǁEMEstimatorǁfit__mutmut_30": xǁEMEstimatorǁfit__mutmut_30,
        "xǁEMEstimatorǁfit__mutmut_31": xǁEMEstimatorǁfit__mutmut_31,
        "xǁEMEstimatorǁfit__mutmut_32": xǁEMEstimatorǁfit__mutmut_32,
        "xǁEMEstimatorǁfit__mutmut_33": xǁEMEstimatorǁfit__mutmut_33,
        "xǁEMEstimatorǁfit__mutmut_34": xǁEMEstimatorǁfit__mutmut_34,
        "xǁEMEstimatorǁfit__mutmut_35": xǁEMEstimatorǁfit__mutmut_35,
        "xǁEMEstimatorǁfit__mutmut_36": xǁEMEstimatorǁfit__mutmut_36,
        "xǁEMEstimatorǁfit__mutmut_37": xǁEMEstimatorǁfit__mutmut_37,
        "xǁEMEstimatorǁfit__mutmut_38": xǁEMEstimatorǁfit__mutmut_38,
        "xǁEMEstimatorǁfit__mutmut_39": xǁEMEstimatorǁfit__mutmut_39,
        "xǁEMEstimatorǁfit__mutmut_40": xǁEMEstimatorǁfit__mutmut_40,
        "xǁEMEstimatorǁfit__mutmut_41": xǁEMEstimatorǁfit__mutmut_41,
        "xǁEMEstimatorǁfit__mutmut_42": xǁEMEstimatorǁfit__mutmut_42,
        "xǁEMEstimatorǁfit__mutmut_43": xǁEMEstimatorǁfit__mutmut_43,
        "xǁEMEstimatorǁfit__mutmut_44": xǁEMEstimatorǁfit__mutmut_44,
        "xǁEMEstimatorǁfit__mutmut_45": xǁEMEstimatorǁfit__mutmut_45,
        "xǁEMEstimatorǁfit__mutmut_46": xǁEMEstimatorǁfit__mutmut_46,
        "xǁEMEstimatorǁfit__mutmut_47": xǁEMEstimatorǁfit__mutmut_47,
        "xǁEMEstimatorǁfit__mutmut_48": xǁEMEstimatorǁfit__mutmut_48,
        "xǁEMEstimatorǁfit__mutmut_49": xǁEMEstimatorǁfit__mutmut_49,
        "xǁEMEstimatorǁfit__mutmut_50": xǁEMEstimatorǁfit__mutmut_50,
        "xǁEMEstimatorǁfit__mutmut_51": xǁEMEstimatorǁfit__mutmut_51,
        "xǁEMEstimatorǁfit__mutmut_52": xǁEMEstimatorǁfit__mutmut_52,
        "xǁEMEstimatorǁfit__mutmut_53": xǁEMEstimatorǁfit__mutmut_53,
        "xǁEMEstimatorǁfit__mutmut_54": xǁEMEstimatorǁfit__mutmut_54,
        "xǁEMEstimatorǁfit__mutmut_55": xǁEMEstimatorǁfit__mutmut_55,
        "xǁEMEstimatorǁfit__mutmut_56": xǁEMEstimatorǁfit__mutmut_56,
        "xǁEMEstimatorǁfit__mutmut_57": xǁEMEstimatorǁfit__mutmut_57,
        "xǁEMEstimatorǁfit__mutmut_58": xǁEMEstimatorǁfit__mutmut_58,
        "xǁEMEstimatorǁfit__mutmut_59": xǁEMEstimatorǁfit__mutmut_59,
        "xǁEMEstimatorǁfit__mutmut_60": xǁEMEstimatorǁfit__mutmut_60,
        "xǁEMEstimatorǁfit__mutmut_61": xǁEMEstimatorǁfit__mutmut_61,
        "xǁEMEstimatorǁfit__mutmut_62": xǁEMEstimatorǁfit__mutmut_62,
        "xǁEMEstimatorǁfit__mutmut_63": xǁEMEstimatorǁfit__mutmut_63,
        "xǁEMEstimatorǁfit__mutmut_64": xǁEMEstimatorǁfit__mutmut_64,
        "xǁEMEstimatorǁfit__mutmut_65": xǁEMEstimatorǁfit__mutmut_65,
        "xǁEMEstimatorǁfit__mutmut_66": xǁEMEstimatorǁfit__mutmut_66,
        "xǁEMEstimatorǁfit__mutmut_67": xǁEMEstimatorǁfit__mutmut_67,
        "xǁEMEstimatorǁfit__mutmut_68": xǁEMEstimatorǁfit__mutmut_68,
        "xǁEMEstimatorǁfit__mutmut_69": xǁEMEstimatorǁfit__mutmut_69,
        "xǁEMEstimatorǁfit__mutmut_70": xǁEMEstimatorǁfit__mutmut_70,
        "xǁEMEstimatorǁfit__mutmut_71": xǁEMEstimatorǁfit__mutmut_71,
        "xǁEMEstimatorǁfit__mutmut_72": xǁEMEstimatorǁfit__mutmut_72,
        "xǁEMEstimatorǁfit__mutmut_73": xǁEMEstimatorǁfit__mutmut_73,
        "xǁEMEstimatorǁfit__mutmut_74": xǁEMEstimatorǁfit__mutmut_74,
        "xǁEMEstimatorǁfit__mutmut_75": xǁEMEstimatorǁfit__mutmut_75,
        "xǁEMEstimatorǁfit__mutmut_76": xǁEMEstimatorǁfit__mutmut_76,
        "xǁEMEstimatorǁfit__mutmut_77": xǁEMEstimatorǁfit__mutmut_77,
        "xǁEMEstimatorǁfit__mutmut_78": xǁEMEstimatorǁfit__mutmut_78,
        "xǁEMEstimatorǁfit__mutmut_79": xǁEMEstimatorǁfit__mutmut_79,
        "xǁEMEstimatorǁfit__mutmut_80": xǁEMEstimatorǁfit__mutmut_80,
        "xǁEMEstimatorǁfit__mutmut_81": xǁEMEstimatorǁfit__mutmut_81,
        "xǁEMEstimatorǁfit__mutmut_82": xǁEMEstimatorǁfit__mutmut_82,
        "xǁEMEstimatorǁfit__mutmut_83": xǁEMEstimatorǁfit__mutmut_83,
        "xǁEMEstimatorǁfit__mutmut_84": xǁEMEstimatorǁfit__mutmut_84,
        "xǁEMEstimatorǁfit__mutmut_85": xǁEMEstimatorǁfit__mutmut_85,
        "xǁEMEstimatorǁfit__mutmut_86": xǁEMEstimatorǁfit__mutmut_86,
        "xǁEMEstimatorǁfit__mutmut_87": xǁEMEstimatorǁfit__mutmut_87,
        "xǁEMEstimatorǁfit__mutmut_88": xǁEMEstimatorǁfit__mutmut_88,
        "xǁEMEstimatorǁfit__mutmut_89": xǁEMEstimatorǁfit__mutmut_89,
        "xǁEMEstimatorǁfit__mutmut_90": xǁEMEstimatorǁfit__mutmut_90,
        "xǁEMEstimatorǁfit__mutmut_91": xǁEMEstimatorǁfit__mutmut_91,
        "xǁEMEstimatorǁfit__mutmut_92": xǁEMEstimatorǁfit__mutmut_92,
        "xǁEMEstimatorǁfit__mutmut_93": xǁEMEstimatorǁfit__mutmut_93,
        "xǁEMEstimatorǁfit__mutmut_94": xǁEMEstimatorǁfit__mutmut_94,
        "xǁEMEstimatorǁfit__mutmut_95": xǁEMEstimatorǁfit__mutmut_95,
        "xǁEMEstimatorǁfit__mutmut_96": xǁEMEstimatorǁfit__mutmut_96,
        "xǁEMEstimatorǁfit__mutmut_97": xǁEMEstimatorǁfit__mutmut_97,
        "xǁEMEstimatorǁfit__mutmut_98": xǁEMEstimatorǁfit__mutmut_98,
        "xǁEMEstimatorǁfit__mutmut_99": xǁEMEstimatorǁfit__mutmut_99,
        "xǁEMEstimatorǁfit__mutmut_100": xǁEMEstimatorǁfit__mutmut_100,
        "xǁEMEstimatorǁfit__mutmut_101": xǁEMEstimatorǁfit__mutmut_101,
        "xǁEMEstimatorǁfit__mutmut_102": xǁEMEstimatorǁfit__mutmut_102,
        "xǁEMEstimatorǁfit__mutmut_103": xǁEMEstimatorǁfit__mutmut_103,
        "xǁEMEstimatorǁfit__mutmut_104": xǁEMEstimatorǁfit__mutmut_104,
        "xǁEMEstimatorǁfit__mutmut_105": xǁEMEstimatorǁfit__mutmut_105,
        "xǁEMEstimatorǁfit__mutmut_106": xǁEMEstimatorǁfit__mutmut_106,
        "xǁEMEstimatorǁfit__mutmut_107": xǁEMEstimatorǁfit__mutmut_107,
        "xǁEMEstimatorǁfit__mutmut_108": xǁEMEstimatorǁfit__mutmut_108,
        "xǁEMEstimatorǁfit__mutmut_109": xǁEMEstimatorǁfit__mutmut_109,
        "xǁEMEstimatorǁfit__mutmut_110": xǁEMEstimatorǁfit__mutmut_110,
        "xǁEMEstimatorǁfit__mutmut_111": xǁEMEstimatorǁfit__mutmut_111,
        "xǁEMEstimatorǁfit__mutmut_112": xǁEMEstimatorǁfit__mutmut_112,
        "xǁEMEstimatorǁfit__mutmut_113": xǁEMEstimatorǁfit__mutmut_113,
        "xǁEMEstimatorǁfit__mutmut_114": xǁEMEstimatorǁfit__mutmut_114,
        "xǁEMEstimatorǁfit__mutmut_115": xǁEMEstimatorǁfit__mutmut_115,
        "xǁEMEstimatorǁfit__mutmut_116": xǁEMEstimatorǁfit__mutmut_116,
        "xǁEMEstimatorǁfit__mutmut_117": xǁEMEstimatorǁfit__mutmut_117,
        "xǁEMEstimatorǁfit__mutmut_118": xǁEMEstimatorǁfit__mutmut_118,
        "xǁEMEstimatorǁfit__mutmut_119": xǁEMEstimatorǁfit__mutmut_119,
        "xǁEMEstimatorǁfit__mutmut_120": xǁEMEstimatorǁfit__mutmut_120,
        "xǁEMEstimatorǁfit__mutmut_121": xǁEMEstimatorǁfit__mutmut_121,
        "xǁEMEstimatorǁfit__mutmut_122": xǁEMEstimatorǁfit__mutmut_122,
        "xǁEMEstimatorǁfit__mutmut_123": xǁEMEstimatorǁfit__mutmut_123,
        "xǁEMEstimatorǁfit__mutmut_124": xǁEMEstimatorǁfit__mutmut_124,
        "xǁEMEstimatorǁfit__mutmut_125": xǁEMEstimatorǁfit__mutmut_125,
        "xǁEMEstimatorǁfit__mutmut_126": xǁEMEstimatorǁfit__mutmut_126,
        "xǁEMEstimatorǁfit__mutmut_127": xǁEMEstimatorǁfit__mutmut_127,
        "xǁEMEstimatorǁfit__mutmut_128": xǁEMEstimatorǁfit__mutmut_128,
        "xǁEMEstimatorǁfit__mutmut_129": xǁEMEstimatorǁfit__mutmut_129,
        "xǁEMEstimatorǁfit__mutmut_130": xǁEMEstimatorǁfit__mutmut_130,
        "xǁEMEstimatorǁfit__mutmut_131": xǁEMEstimatorǁfit__mutmut_131,
        "xǁEMEstimatorǁfit__mutmut_132": xǁEMEstimatorǁfit__mutmut_132,
        "xǁEMEstimatorǁfit__mutmut_133": xǁEMEstimatorǁfit__mutmut_133,
        "xǁEMEstimatorǁfit__mutmut_134": xǁEMEstimatorǁfit__mutmut_134,
        "xǁEMEstimatorǁfit__mutmut_135": xǁEMEstimatorǁfit__mutmut_135,
        "xǁEMEstimatorǁfit__mutmut_136": xǁEMEstimatorǁfit__mutmut_136,
        "xǁEMEstimatorǁfit__mutmut_137": xǁEMEstimatorǁfit__mutmut_137,
        "xǁEMEstimatorǁfit__mutmut_138": xǁEMEstimatorǁfit__mutmut_138,
        "xǁEMEstimatorǁfit__mutmut_139": xǁEMEstimatorǁfit__mutmut_139,
        "xǁEMEstimatorǁfit__mutmut_140": xǁEMEstimatorǁfit__mutmut_140,
        "xǁEMEstimatorǁfit__mutmut_141": xǁEMEstimatorǁfit__mutmut_141,
        "xǁEMEstimatorǁfit__mutmut_142": xǁEMEstimatorǁfit__mutmut_142,
        "xǁEMEstimatorǁfit__mutmut_143": xǁEMEstimatorǁfit__mutmut_143,
        "xǁEMEstimatorǁfit__mutmut_144": xǁEMEstimatorǁfit__mutmut_144,
        "xǁEMEstimatorǁfit__mutmut_145": xǁEMEstimatorǁfit__mutmut_145,
        "xǁEMEstimatorǁfit__mutmut_146": xǁEMEstimatorǁfit__mutmut_146,
        "xǁEMEstimatorǁfit__mutmut_147": xǁEMEstimatorǁfit__mutmut_147,
        "xǁEMEstimatorǁfit__mutmut_148": xǁEMEstimatorǁfit__mutmut_148,
        "xǁEMEstimatorǁfit__mutmut_149": xǁEMEstimatorǁfit__mutmut_149,
        "xǁEMEstimatorǁfit__mutmut_150": xǁEMEstimatorǁfit__mutmut_150,
        "xǁEMEstimatorǁfit__mutmut_151": xǁEMEstimatorǁfit__mutmut_151,
        "xǁEMEstimatorǁfit__mutmut_152": xǁEMEstimatorǁfit__mutmut_152,
        "xǁEMEstimatorǁfit__mutmut_153": xǁEMEstimatorǁfit__mutmut_153,
        "xǁEMEstimatorǁfit__mutmut_154": xǁEMEstimatorǁfit__mutmut_154,
        "xǁEMEstimatorǁfit__mutmut_155": xǁEMEstimatorǁfit__mutmut_155,
        "xǁEMEstimatorǁfit__mutmut_156": xǁEMEstimatorǁfit__mutmut_156,
        "xǁEMEstimatorǁfit__mutmut_157": xǁEMEstimatorǁfit__mutmut_157,
        "xǁEMEstimatorǁfit__mutmut_158": xǁEMEstimatorǁfit__mutmut_158,
        "xǁEMEstimatorǁfit__mutmut_159": xǁEMEstimatorǁfit__mutmut_159,
        "xǁEMEstimatorǁfit__mutmut_160": xǁEMEstimatorǁfit__mutmut_160,
        "xǁEMEstimatorǁfit__mutmut_161": xǁEMEstimatorǁfit__mutmut_161,
        "xǁEMEstimatorǁfit__mutmut_162": xǁEMEstimatorǁfit__mutmut_162,
        "xǁEMEstimatorǁfit__mutmut_163": xǁEMEstimatorǁfit__mutmut_163,
        "xǁEMEstimatorǁfit__mutmut_164": xǁEMEstimatorǁfit__mutmut_164,
        "xǁEMEstimatorǁfit__mutmut_165": xǁEMEstimatorǁfit__mutmut_165,
    }
    xǁEMEstimatorǁfit__mutmut_orig.__name__ = "xǁEMEstimatorǁfit"

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
        args = [joint_smoothed, smoothed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEMEstimatorǁ_update_transition_matrix__mutmut_orig"),
            object.__getattribute__(
                self, "xǁEMEstimatorǁ_update_transition_matrix__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_orig(
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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_1(
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
        k = None
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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_2(
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
        k = smoothed.shape[2]
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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_3(
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
        p_new = None

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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_4(
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
        p_new = np.zeros(None)

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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_5(
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

        for i in range(None):
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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_6(
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
            denom = None
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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_7(
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
            denom = smoothed[:+1, i].sum()
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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_8(
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
            denom = smoothed[:-2, i].sum()
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

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_9(
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
            if denom >= 1e-12:
                for j in range(k):
                    p_new[i, j] = joint_smoothed[:, i, j].sum() / denom
            else:
                p_new[i] = 1.0 / k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_10(
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
            if denom > 1.000000000001:
                for j in range(k):
                    p_new[i, j] = joint_smoothed[:, i, j].sum() / denom
            else:
                p_new[i] = 1.0 / k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_11(
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
                for j in range(None):
                    p_new[i, j] = joint_smoothed[:, i, j].sum() / denom
            else:
                p_new[i] = 1.0 / k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_12(
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
                    p_new[i, j] = None
            else:
                p_new[i] = 1.0 / k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_13(
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
                    p_new[i, j] = joint_smoothed[:, i, j].sum() * denom
            else:
                p_new[i] = 1.0 / k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_14(
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
                p_new[i] = None

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_15(
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
                p_new[i] = 1.0 * k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_16(
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
                p_new[i] = 2.0 / k

        # Ensure valid transition matrix
        for i in range(k):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_17(
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
        for i in range(None):
            p_new[i] = np.maximum(p_new[i], 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_18(
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
            p_new[i] = None
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_19(
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
            p_new[i] = np.maximum(None, 1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_20(
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
            p_new[i] = np.maximum(p_new[i], None)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_21(
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
            p_new[i] = np.maximum(1e-6)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_22(
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
            p_new[i] = np.maximum(
                p_new[i],
            )
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_23(
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
            p_new[i] = np.maximum(p_new[i], 1.000001)
            p_new[i] /= p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_24(
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
            p_new[i] = p_new[i].sum()

        return p_new

    def xǁEMEstimatorǁ_update_transition_matrix__mutmut_25(
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
            p_new[i] *= p_new[i].sum()

        return p_new

    xǁEMEstimatorǁ_update_transition_matrix__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_1": xǁEMEstimatorǁ_update_transition_matrix__mutmut_1,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_2": xǁEMEstimatorǁ_update_transition_matrix__mutmut_2,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_3": xǁEMEstimatorǁ_update_transition_matrix__mutmut_3,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_4": xǁEMEstimatorǁ_update_transition_matrix__mutmut_4,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_5": xǁEMEstimatorǁ_update_transition_matrix__mutmut_5,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_6": xǁEMEstimatorǁ_update_transition_matrix__mutmut_6,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_7": xǁEMEstimatorǁ_update_transition_matrix__mutmut_7,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_8": xǁEMEstimatorǁ_update_transition_matrix__mutmut_8,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_9": xǁEMEstimatorǁ_update_transition_matrix__mutmut_9,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_10": xǁEMEstimatorǁ_update_transition_matrix__mutmut_10,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_11": xǁEMEstimatorǁ_update_transition_matrix__mutmut_11,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_12": xǁEMEstimatorǁ_update_transition_matrix__mutmut_12,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_13": xǁEMEstimatorǁ_update_transition_matrix__mutmut_13,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_14": xǁEMEstimatorǁ_update_transition_matrix__mutmut_14,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_15": xǁEMEstimatorǁ_update_transition_matrix__mutmut_15,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_16": xǁEMEstimatorǁ_update_transition_matrix__mutmut_16,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_17": xǁEMEstimatorǁ_update_transition_matrix__mutmut_17,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_18": xǁEMEstimatorǁ_update_transition_matrix__mutmut_18,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_19": xǁEMEstimatorǁ_update_transition_matrix__mutmut_19,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_20": xǁEMEstimatorǁ_update_transition_matrix__mutmut_20,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_21": xǁEMEstimatorǁ_update_transition_matrix__mutmut_21,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_22": xǁEMEstimatorǁ_update_transition_matrix__mutmut_22,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_23": xǁEMEstimatorǁ_update_transition_matrix__mutmut_23,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_24": xǁEMEstimatorǁ_update_transition_matrix__mutmut_24,
        "xǁEMEstimatorǁ_update_transition_matrix__mutmut_25": xǁEMEstimatorǁ_update_transition_matrix__mutmut_25,
    }
    xǁEMEstimatorǁ_update_transition_matrix__mutmut_orig.__name__ = (
        "xǁEMEstimatorǁ_update_transition_matrix"
    )

    def _m_step(
        self,
        model: MarkovSwitchingModel,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [model, params, smoothed, joint_smoothed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEMEstimatorǁ_m_step__mutmut_orig"),
            object.__getattribute__(self, "xǁEMEstimatorǁ_m_step__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEMEstimatorǁ_m_step__mutmut_orig(
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

    def xǁEMEstimatorǁ_m_step__mutmut_1(
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
        if hasattr(None, "_m_step_update"):
            return model._m_step_update(params, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_2(
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
        if hasattr(model, None):
            return model._m_step_update(params, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_3(
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
        if hasattr("_m_step_update"):
            return model._m_step_update(params, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_4(
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
        if hasattr(
            model,
        ):
            return model._m_step_update(params, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_5(
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
        if hasattr(model, "XX_m_step_updateXX"):
            return model._m_step_update(params, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_6(
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
        if hasattr(model, "_M_STEP_UPDATE"):
            return model._m_step_update(params, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_7(
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
            return model._m_step_update(None, smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_8(
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
            return model._m_step_update(params, None, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_9(
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
            return model._m_step_update(params, smoothed, None)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_10(
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
            return model._m_step_update(smoothed, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_11(
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
            return model._m_step_update(params, joint_smoothed)  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_12(
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
            return model._m_step_update(
                params,
                smoothed,
            )  # type: ignore[attr-defined]

        return self._generic_m_step(model, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_13(
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

        return self._generic_m_step(None, params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_14(
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

        return self._generic_m_step(model, None, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_15(
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

        return self._generic_m_step(model, params, None)

    def xǁEMEstimatorǁ_m_step__mutmut_16(
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

        return self._generic_m_step(params, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_17(
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

        return self._generic_m_step(model, smoothed)

    def xǁEMEstimatorǁ_m_step__mutmut_18(
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

        return self._generic_m_step(
            model,
            params,
        )

    xǁEMEstimatorǁ_m_step__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEMEstimatorǁ_m_step__mutmut_1": xǁEMEstimatorǁ_m_step__mutmut_1,
        "xǁEMEstimatorǁ_m_step__mutmut_2": xǁEMEstimatorǁ_m_step__mutmut_2,
        "xǁEMEstimatorǁ_m_step__mutmut_3": xǁEMEstimatorǁ_m_step__mutmut_3,
        "xǁEMEstimatorǁ_m_step__mutmut_4": xǁEMEstimatorǁ_m_step__mutmut_4,
        "xǁEMEstimatorǁ_m_step__mutmut_5": xǁEMEstimatorǁ_m_step__mutmut_5,
        "xǁEMEstimatorǁ_m_step__mutmut_6": xǁEMEstimatorǁ_m_step__mutmut_6,
        "xǁEMEstimatorǁ_m_step__mutmut_7": xǁEMEstimatorǁ_m_step__mutmut_7,
        "xǁEMEstimatorǁ_m_step__mutmut_8": xǁEMEstimatorǁ_m_step__mutmut_8,
        "xǁEMEstimatorǁ_m_step__mutmut_9": xǁEMEstimatorǁ_m_step__mutmut_9,
        "xǁEMEstimatorǁ_m_step__mutmut_10": xǁEMEstimatorǁ_m_step__mutmut_10,
        "xǁEMEstimatorǁ_m_step__mutmut_11": xǁEMEstimatorǁ_m_step__mutmut_11,
        "xǁEMEstimatorǁ_m_step__mutmut_12": xǁEMEstimatorǁ_m_step__mutmut_12,
        "xǁEMEstimatorǁ_m_step__mutmut_13": xǁEMEstimatorǁ_m_step__mutmut_13,
        "xǁEMEstimatorǁ_m_step__mutmut_14": xǁEMEstimatorǁ_m_step__mutmut_14,
        "xǁEMEstimatorǁ_m_step__mutmut_15": xǁEMEstimatorǁ_m_step__mutmut_15,
        "xǁEMEstimatorǁ_m_step__mutmut_16": xǁEMEstimatorǁ_m_step__mutmut_16,
        "xǁEMEstimatorǁ_m_step__mutmut_17": xǁEMEstimatorǁ_m_step__mutmut_17,
        "xǁEMEstimatorǁ_m_step__mutmut_18": xǁEMEstimatorǁ_m_step__mutmut_18,
    }
    xǁEMEstimatorǁ_m_step__mutmut_orig.__name__ = "xǁEMEstimatorǁ_m_step"

    def _generic_m_step(
        self,
        model: MarkovSwitchingModel,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [model, params, smoothed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEMEstimatorǁ_generic_m_step__mutmut_orig"),
            object.__getattribute__(self, "xǁEMEstimatorǁ_generic_m_step__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEMEstimatorǁ_generic_m_step__mutmut_orig(
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_1(
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
        k = None
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_2(
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
        y = None
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_3(
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
        new_params = None

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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_4(
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
            for s in range(None):
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_5(
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
                weights = None
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_6(
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
                w_sum = None
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_7(
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
                if w_sum >= 1e-12:
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_8(
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
                if w_sum > 1.000000000001:
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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_9(
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
                    new_params[s] = None

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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_10(
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
                    new_params[s] = np.sum(weights * y) * w_sum

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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_11(
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
                    new_params[s] = np.sum(None) / w_sum

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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_12(
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
                    new_params[s] = np.sum(weights / y) / w_sum

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

    def xǁEMEstimatorǁ_generic_m_step__mutmut_13(
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
            for s in range(None):
                weights = smoothed[:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    mu_s = new_params[s]
                    resid2 = (y - mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_14(
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
                weights = None
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    mu_s = new_params[s]
                    resid2 = (y - mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_15(
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
                w_sum = None
                if w_sum > 1e-12:
                    mu_s = new_params[s]
                    resid2 = (y - mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_16(
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
                if w_sum >= 1e-12:
                    mu_s = new_params[s]
                    resid2 = (y - mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_17(
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
                if w_sum > 1.000000000001:
                    mu_s = new_params[s]
                    resid2 = (y - mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_18(
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
                    mu_s = None
                    resid2 = (y - mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_19(
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
                    resid2 = None
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_20(
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
                    resid2 = (y - mu_s) * 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_21(
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
                    resid2 = (y + mu_s) ** 2
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_22(
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
                    resid2 = (y - mu_s) ** 3
                    var_s = np.sum(weights * resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_23(
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
                    var_s = None
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_24(
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
                    var_s = np.sum(weights * resid2) * w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_25(
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
                    var_s = np.sum(None) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_26(
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
                    var_s = np.sum(weights / resid2) / w_sum
                    new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_27(
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
                    new_params[k + s] = None

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_28(
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
                    new_params[k - s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_29(
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
                    new_params[k + s] = max(None, 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_30(
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
                    new_params[k + s] = max(np.sqrt(var_s), None)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_31(
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
                    new_params[k + s] = max(1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_32(
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
                    new_params[k + s] = max(
                        np.sqrt(var_s),
                    )

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_33(
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
                    new_params[k + s] = max(np.sqrt(None), 1e-6)

        return new_params

    def xǁEMEstimatorǁ_generic_m_step__mutmut_34(
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
                    new_params[k + s] = max(np.sqrt(var_s), 1.000001)

        return new_params

    xǁEMEstimatorǁ_generic_m_step__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEMEstimatorǁ_generic_m_step__mutmut_1": xǁEMEstimatorǁ_generic_m_step__mutmut_1,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_2": xǁEMEstimatorǁ_generic_m_step__mutmut_2,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_3": xǁEMEstimatorǁ_generic_m_step__mutmut_3,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_4": xǁEMEstimatorǁ_generic_m_step__mutmut_4,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_5": xǁEMEstimatorǁ_generic_m_step__mutmut_5,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_6": xǁEMEstimatorǁ_generic_m_step__mutmut_6,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_7": xǁEMEstimatorǁ_generic_m_step__mutmut_7,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_8": xǁEMEstimatorǁ_generic_m_step__mutmut_8,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_9": xǁEMEstimatorǁ_generic_m_step__mutmut_9,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_10": xǁEMEstimatorǁ_generic_m_step__mutmut_10,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_11": xǁEMEstimatorǁ_generic_m_step__mutmut_11,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_12": xǁEMEstimatorǁ_generic_m_step__mutmut_12,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_13": xǁEMEstimatorǁ_generic_m_step__mutmut_13,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_14": xǁEMEstimatorǁ_generic_m_step__mutmut_14,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_15": xǁEMEstimatorǁ_generic_m_step__mutmut_15,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_16": xǁEMEstimatorǁ_generic_m_step__mutmut_16,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_17": xǁEMEstimatorǁ_generic_m_step__mutmut_17,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_18": xǁEMEstimatorǁ_generic_m_step__mutmut_18,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_19": xǁEMEstimatorǁ_generic_m_step__mutmut_19,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_20": xǁEMEstimatorǁ_generic_m_step__mutmut_20,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_21": xǁEMEstimatorǁ_generic_m_step__mutmut_21,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_22": xǁEMEstimatorǁ_generic_m_step__mutmut_22,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_23": xǁEMEstimatorǁ_generic_m_step__mutmut_23,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_24": xǁEMEstimatorǁ_generic_m_step__mutmut_24,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_25": xǁEMEstimatorǁ_generic_m_step__mutmut_25,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_26": xǁEMEstimatorǁ_generic_m_step__mutmut_26,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_27": xǁEMEstimatorǁ_generic_m_step__mutmut_27,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_28": xǁEMEstimatorǁ_generic_m_step__mutmut_28,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_29": xǁEMEstimatorǁ_generic_m_step__mutmut_29,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_30": xǁEMEstimatorǁ_generic_m_step__mutmut_30,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_31": xǁEMEstimatorǁ_generic_m_step__mutmut_31,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_32": xǁEMEstimatorǁ_generic_m_step__mutmut_32,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_33": xǁEMEstimatorǁ_generic_m_step__mutmut_33,
        "xǁEMEstimatorǁ_generic_m_step__mutmut_34": xǁEMEstimatorǁ_generic_m_step__mutmut_34,
    }
    xǁEMEstimatorǁ_generic_m_step__mutmut_orig.__name__ = "xǁEMEstimatorǁ_generic_m_step"

    def _extract_regime_params(
        self,
        model: MarkovSwitchingModel,
        params: NDArray[np.float64],
    ) -> dict[int, dict[str, float]]:
        args = [model, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEMEstimatorǁ_extract_regime_params__mutmut_orig"),
            object.__getattribute__(self, "xǁEMEstimatorǁ_extract_regime_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_orig(
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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_1(
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
        k = None

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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_2(
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

        if hasattr(None, "_extract_regime_params"):
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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_3(
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

        if hasattr(model, None):
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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_4(
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

        if hasattr("_extract_regime_params"):
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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_5(
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

        if hasattr(
            model,
        ):
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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_6(
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

        if hasattr(model, "XX_extract_regime_paramsXX"):
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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_7(
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

        if hasattr(model, "_EXTRACT_REGIME_PARAMS"):
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

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_8(
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
            return model._extract_regime_params(None)  # type: ignore[attr-defined]

        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            rp: dict[str, float] = {}
            if model.switching_mean:
                rp["mu"] = float(params[s])
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_9(
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

        regime_params: dict[int, dict[str, float]] = None
        for s in range(k):
            rp: dict[str, float] = {}
            if model.switching_mean:
                rp["mu"] = float(params[s])
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_10(
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
        for s in range(None):
            rp: dict[str, float] = {}
            if model.switching_mean:
                rp["mu"] = float(params[s])
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_11(
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
            rp: dict[str, float] = None
            if model.switching_mean:
                rp["mu"] = float(params[s])
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_12(
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
                rp["mu"] = None
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_13(
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
                rp["XXmuXX"] = float(params[s])
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_14(
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
                rp["MU"] = float(params[s])
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_15(
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
                rp["mu"] = float(None)
            if model.switching_variance:
                rp["sigma"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_16(
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
                rp["sigma"] = None
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_17(
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
                rp["XXsigmaXX"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_18(
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
                rp["SIGMA"] = float(params[k + s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_19(
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
                rp["sigma"] = float(None)
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_20(
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
                rp["sigma"] = float(params[k - s])
            regime_params[s] = rp

        return regime_params

    def xǁEMEstimatorǁ_extract_regime_params__mutmut_21(
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
            regime_params[s] = None

        return regime_params

    xǁEMEstimatorǁ_extract_regime_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_1": xǁEMEstimatorǁ_extract_regime_params__mutmut_1,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_2": xǁEMEstimatorǁ_extract_regime_params__mutmut_2,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_3": xǁEMEstimatorǁ_extract_regime_params__mutmut_3,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_4": xǁEMEstimatorǁ_extract_regime_params__mutmut_4,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_5": xǁEMEstimatorǁ_extract_regime_params__mutmut_5,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_6": xǁEMEstimatorǁ_extract_regime_params__mutmut_6,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_7": xǁEMEstimatorǁ_extract_regime_params__mutmut_7,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_8": xǁEMEstimatorǁ_extract_regime_params__mutmut_8,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_9": xǁEMEstimatorǁ_extract_regime_params__mutmut_9,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_10": xǁEMEstimatorǁ_extract_regime_params__mutmut_10,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_11": xǁEMEstimatorǁ_extract_regime_params__mutmut_11,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_12": xǁEMEstimatorǁ_extract_regime_params__mutmut_12,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_13": xǁEMEstimatorǁ_extract_regime_params__mutmut_13,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_14": xǁEMEstimatorǁ_extract_regime_params__mutmut_14,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_15": xǁEMEstimatorǁ_extract_regime_params__mutmut_15,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_16": xǁEMEstimatorǁ_extract_regime_params__mutmut_16,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_17": xǁEMEstimatorǁ_extract_regime_params__mutmut_17,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_18": xǁEMEstimatorǁ_extract_regime_params__mutmut_18,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_19": xǁEMEstimatorǁ_extract_regime_params__mutmut_19,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_20": xǁEMEstimatorǁ_extract_regime_params__mutmut_20,
        "xǁEMEstimatorǁ_extract_regime_params__mutmut_21": xǁEMEstimatorǁ_extract_regime_params__mutmut_21,
    }
    xǁEMEstimatorǁ_extract_regime_params__mutmut_orig.__name__ = (
        "xǁEMEstimatorǁ_extract_regime_params"
    )
