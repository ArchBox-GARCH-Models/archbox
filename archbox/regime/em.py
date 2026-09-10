"""EM Algorithm for Markov-Switching models.

Implements the Expectation-Maximization algorithm for parameter estimation
in Markov-Switching models. The E-step uses the Hamilton filter and Kim
smoother; the M-step updates the transition matrix and regime parameters.

All quantities estimated by EM (regime parameters *and* the transition
matrix) are written back into a single parameter vector whose entries
match ``model.param_names``, so that ``model.loglike(results.params)``
reproduces ``results.loglike``.  The initial state distribution is also
estimated (it is not part of ``params``); it is stored on the model and
on the results as ``init_probs`` and is used by ``model.loglike`` by
default once the model has been fitted.

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

from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from archbox.regime.hamilton_filter import HamiltonFilter
from archbox.regime.kim_smoother import KimSmoother
from archbox.regime.results import RegimeResults

if TYPE_CHECKING:
    from archbox.regime.base import MarkovSwitchingModel


def numerical_hessian(
    fn: Callable[[NDArray[np.float64]], float],
    params: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Central-difference numerical Hessian of a scalar function.

    Parameters
    ----------
    fn : callable
        Function of the parameter vector.
    params : ndarray
        Point at which the Hessian is evaluated, shape (n,).

    Returns
    -------
    ndarray
        Symmetric Hessian matrix, shape (n, n). Entries are NaN if any
        function evaluation fails or is not finite.
    """
    x = np.asarray(params, dtype=np.float64)
    n = x.size
    step = 6.06e-6 * np.maximum(np.abs(x), 1e-2)
    hess = np.zeros((n, n))

    def safe(point: NDArray[np.float64]) -> float:
        try:
            val = float(fn(point))
        except (ValueError, np.linalg.LinAlgError, ZeroDivisionError):
            return float("nan")
        return val if np.isfinite(val) else float("nan")

    for i in range(n):
        for j in range(i, n):
            ei = np.zeros(n)
            ej = np.zeros(n)
            ei[i] = step[i]
            ej[j] = step[j]
            f_pp = safe(x + ei + ej)
            f_pm = safe(x + ei - ej)
            f_mp = safe(x - ei + ej)
            f_mm = safe(x - ei - ej)
            value = (f_pp - f_pm - f_mp + f_mm) / (4.0 * step[i] * step[j])
            hess[i, j] = value
            hess[j, i] = value

    return hess


def standard_errors(
    fn: Callable[[NDArray[np.float64]], float],
    params: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Hessian-based standard errors of a log-likelihood at ``params``.

    Parameters
    ----------
    fn : callable
        Log-likelihood as a function of the parameter vector.
    params : ndarray
        Estimated parameters.

    Returns
    -------
    ndarray
        Standard errors, shape (n,). NaN where the observed information
        matrix is not positive definite.
    """
    n = np.asarray(params).size
    nan_out = np.full(n, np.nan)

    hess = numerical_hessian(fn, params)
    if not np.all(np.isfinite(hess)):
        return nan_out

    info = -0.5 * (hess + hess.T)
    try:
        eigvals = np.linalg.eigvalsh(info)
    except np.linalg.LinAlgError:
        return nan_out
    if np.min(eigvals) <= 0.0:
        return nan_out

    try:
        cov = np.linalg.inv(info)
    except np.linalg.LinAlgError:
        return nan_out

    diag = np.diag(cov)
    out = np.full(n, np.nan)
    positive = diag > 0.0
    out[positive] = np.sqrt(diag[positive])
    return out


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
        compute_se: bool = True,
    ) -> RegimeResults:
        """Fit a Markov-Switching model using the EM algorithm.

        Parameters
        ----------
        model : MarkovSwitchingModel
            The model to fit.
        maxiter : int
            Maximum number of EM iterations.
        tol : float
            Convergence tolerance. The criterion is absolute-or-relative:
            convergence is declared when the change in log-likelihood is
            below ``tol`` in absolute terms or below
            ``tol * max(1, |loglike|)``.
        verbose : bool
            Print progress information.
        compute_se : bool
            Compute numerical-Hessian standard errors at the final params.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        params = np.asarray(model.start_params, dtype=np.float64).copy()
        k = model.k_regimes
        t_start = model._t_start

        transition_matrix = model._extract_transition_matrix(params)
        init_probs = HamiltonFilter.ergodic_probabilities(transition_matrix)

        loglike_old = -np.inf
        converged = False
        self.loglike_history = []
        iteration = 0

        for iteration in range(maxiter):
            # === E-step (conditioning on the first t_start observations) ===
            regime_loglikes = model._regime_loglikes(params)[t_start:]

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

            # === Check convergence (absolute or relative, sane scale) ===
            delta = abs(loglike - loglike_old)
            rel_change = delta / max(1.0, abs(loglike))

            if verbose and iteration % 10 == 0:
                print(
                    f"  EM iter {iteration:4d}: "
                    f"loglike = {loglike:12.4f}, "
                    f"rel_change = {rel_change:.2e}"
                )

            if iteration > 0 and (delta < tol or rel_change < tol):
                converged = True
                if verbose:
                    print(
                        f"  EM converged at iteration {iteration} (rel_change = {rel_change:.2e})"
                    )
                break

            loglike_old = loglike

            # === M-step ===
            transition_matrix = self._update_transition_matrix(joint_smoothed, smoothed)

            init_probs = self._normalize_probs(smoothed[0], k)

            params = self._m_step(model, params, smoothed, joint_smoothed)
            # Keep the parameter vector in sync with the EM estimates
            params = model._set_transition_params(params, transition_matrix)

        # === Final E-step with the converged parameters ===
        regime_loglikes = model._regime_loglikes(params)[t_start:]
        filtered, predicted, loglike, _ = self.hamilton_filter.filter_vectorized(
            regime_loglikes, transition_matrix, init_probs
        )
        smoothed = self.kim_smoother.smooth_vectorized(filtered, predicted, transition_matrix)

        # Persist the fitted state on the model
        model._transition_matrix = transition_matrix
        model._init_probs = init_probs
        model._params = params
        model._last_filtered_probs = filtered[-1].copy()
        model._is_fitted = True

        std_errs: NDArray[np.float64] | None = None
        if compute_se:
            std_errs = standard_errors(lambda p: model.loglike(p, init_probs=init_probs), params)

        regime_params = self._extract_regime_params(model, params)
        coefficients: list[NDArray[np.float64]] | None = None
        intercepts: list[NDArray[np.float64]] | None = None
        coefs = model._regime_coefficients(params)
        if coefs is not None:
            coefficients, intercepts = coefs

        return RegimeResults(
            params=params,
            regime_params=regime_params,
            transition_matrix=transition_matrix,
            filtered_probs=self._pad(filtered, t_start),
            smoothed_probs=self._pad(smoothed, t_start),
            predicted_probs=self._pad(predicted, t_start),
            loglike=loglike,
            nobs=model.nobs,
            k_regimes=k,
            model_name=model.model_name,
            param_names=model.param_names,
            converged=converged,
            n_iter=iteration + 1,
            nobs_effective=model.nobs_effective,
            init_probs=init_probs,
            std_errors=std_errs,
            coefficients=coefficients,
            intercepts=intercepts,
        )

    @staticmethod
    def _normalize_probs(row: NDArray[np.float64], k: int) -> NDArray[np.float64]:
        """Normalize a (possibly unnormalized) probability vector."""
        probs = np.maximum(np.asarray(row, dtype=np.float64).copy(), 0.0)
        total = float(probs.sum())
        if total <= 0.0:
            return np.ones(k) / k
        probs /= total
        probs = np.maximum(probs, 1e-12)
        probs /= float(probs.sum())
        return probs

    @staticmethod
    def _pad(probs: NDArray[np.float64], t_start: int) -> NDArray[np.float64]:
        """Pad probability paths back to the full sample length.

        The first ``t_start`` observations are conditioned on and carry
        no filtered/smoothed information; they are filled with the first
        available row so that all arrays have shape (T, k) and every row
        still sums to one.

        Parameters
        ----------
        probs : ndarray
            Probabilities over the effective sample, shape (T-t_start, k).
        t_start : int
            Number of conditioned-on observations.

        Returns
        -------
        ndarray
            Shape (T, k).
        """
        if t_start <= 0:
            return probs
        pad = np.repeat(probs[:1], t_start, axis=0)
        return np.vstack([pad, probs])

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
        n_obs = filtered_probs.shape[0]
        trans = transition_matrix
        smoothed = np.zeros_like(filtered_probs)
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
        trans = transition_matrix
        pred_safe = np.maximum(predicted_probs[1:], 1e-300)
        ratio = smoothed_probs[1:] / pred_safe  # (T-1, k)
        # joint[t, i, j] = filtered[t, i] * P[i, j] * ratio[t+1, j]
        return filtered_probs[:-1, :, None] * trans[None, :, :] * ratio[:, None, :]

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
                p_new[i] = joint_smoothed[:, i, :].sum(axis=0) / denom
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

        If the model has a custom ``_m_step_update`` method, use it.
        Otherwise, use a generic M-step for mean/variance models.

        Parameters
        ----------
        model : MarkovSwitchingModel
            The model being estimated.
        params : ndarray
            Current parameter vector.
        smoothed : ndarray
            Smoothed probabilities over the effective sample,
            shape (T - t_start, k); row 0 corresponds to observation
            ``t = model._t_start``.
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T - t_start - 1, k, k).

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
            Smoothed probabilities, shape (T - t_start, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = model.k_regimes
        y = model.endog[model._t_start :]
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
