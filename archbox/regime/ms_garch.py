"""Markov-Switching GARCH model (Gray, 1996).

Implements GARCH with regime-switching parameters using the Gray (1996)
collapsing approach to handle path-dependence::

    sigma^2_t(s) = omega_s + alpha_s * eps^2_{t-1} + beta_s * h_{t-1}
    h_{t-1}      = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

The collapsing uses the *filtered* probabilities produced by the same
forward pass, so the recursion, the Hamilton filter and the likelihood
are computed in a single consistent sweep and no state is mutated as a
side effect of evaluating a regime density.  Parameters are estimated by
direct numerical maximisation of the Hamilton-filter likelihood (the
Gray recursion makes an exact EM M-step unavailable because the
conditional variances depend on the whole parameter vector through the
filtered probabilities).

References
----------
Gray, S.F. (1996). Modeling the Conditional Distribution of Interest Rates
as a Regime-Switching Process. Journal of Financial Economics, 42(1), 27-62.

Haas, M., Mittnik, S. & Paolella, M.S. (2004). A New Approach to
Markov-Switching GARCH Models. Journal of Financial Econometrics, 2(4), 493-530.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from archbox.regime.base import MarkovSwitchingModel
from archbox.regime.hamilton_filter import HamiltonFilter
from archbox.regime.kim_smoother import KimSmoother

if TYPE_CHECKING:
    from archbox.regime.results import RegimeResults

_MAX_PERSISTENCE = 0.9995


class MarkovSwitchingGARCH(MarkovSwitchingModel):
    """Markov-Switching GARCH model (Gray, 1996).

    sigma^2_t(s) = omega_s + alpha_s * eps^2_{t-1} + beta_s * h_{t-1}
    h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

    Parameters
    ----------
    endog : array-like
        Time series of returns, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.
    p : int
        GARCH order (number of lagged variances). Default is 1.
    q : int
        ARCH order (number of lagged squared residuals). Default is 1.
    method : str
        Collapsing method: 'gray' (default).

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_garch import MarkovSwitchingGARCH
    >>> returns = np.random.default_rng(0).standard_normal(500) * 0.01
    >>> model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
    >>> results = model.fit(verbose=False)
    >>> print(results.summary())
    """

    model_name: str = "MS-GARCH"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        if self.endog.ndim != 1:
            msg = "MarkovSwitchingGARCH requires a univariate series"
            raise ValueError(msg)
        self.p_garch = p
        self.q_arch = q
        self.method = method
        self._t_start = 0

    # --- Gray recursion ---

    def _garch_arrays(
        self,
        params: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Return (omega, alpha, beta) arrays over regimes."""
        k = self.k_regimes
        omega = np.empty(k)
        alpha = np.empty(k)
        beta = np.empty(k)
        for s in range(k):
            omega[s], alpha[s], beta[s] = self._unpack_garch_params(params, s)
        return omega, alpha, beta

    def _gray_recursion(
        self,
        params: NDArray[np.float64],
        init_probs: NDArray[np.float64] | None = None,
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
    ]:
        """Run the Gray (1996) filter.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        init_probs : ndarray, optional
            Initial state distribution. Defaults to the ergodic
            distribution implied by ``params``.

        Returns
        -------
        tuple
            (sigma2, h_collapsed, filtered_probs, regime_loglikes) with
            shapes (T, k), (T,), (T, k) and (T, k).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog
        omega, alpha, beta = self._garch_arrays(params)
        trans = self._extract_transition_matrix(params)

        if init_probs is None:
            init_probs = HamiltonFilter.ergodic_probabilities(trans)

        var_y = max(float(np.var(y)), 1e-12)

        sigma2 = np.zeros((n_obs, k))
        h_collapsed = np.zeros(n_obs)
        filtered = np.zeros((n_obs, k))
        log_eta = np.zeros((n_obs, k))

        xi = np.asarray(init_probs, dtype=np.float64).copy()

        for t in range(n_obs):
            if t == 0:
                sigma2[0] = var_y
            else:
                sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            np.maximum(sigma2[t], 1e-14, out=sigma2[t])

            log_eta[t] = (
                -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2[t]) - 0.5 * y[t] ** 2 / sigma2[t]
            )

            xi_pred = trans.T @ xi
            xi_pred = np.maximum(xi_pred, 1e-300)
            xi_pred /= xi_pred.sum()

            max_log = float(np.max(log_eta[t]))
            num = xi_pred * np.exp(log_eta[t] - max_log)
            f_t = float(num.sum())
            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            h_collapsed[t] = max(float(np.sum(xi * sigma2[t])), 1e-14)

        return sigma2, h_collapsed, filtered, log_eta

    def conditional_variances(
        self,
        params: NDArray[np.float64] | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Regime conditional variances and the Gray-collapsed variance.

        Parameters
        ----------
        params : ndarray, optional
            Parameter vector. Uses the fitted parameters if None.

        Returns
        -------
        tuple
            (sigma2, h_collapsed) with shapes (T, k) and (T,).
        """
        if params is None:
            params = self._params
        if params is None:
            msg = "No parameters available. Fit the model first or pass params."
            raise RuntimeError(msg)
        sigma2, h_collapsed, _, _ = self._gray_recursion(np.asarray(params, dtype=np.float64))
        return sigma2, h_collapsed

    def _regime_loglikes(self, params: NDArray[np.float64]) -> NDArray[np.float64]:
        """Regime conditional log densities, shape (T, k)."""
        _, _, _, log_eta = self._gray_recursion(params)
        return log_eta

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach. This method has no side
        effects: nothing is cached on the model.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return self._regime_loglikes(params)[:, regime]

    def _unpack_garch_params(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-12)
        alpha = max(abs(float(params[base + 1])), 0.0)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            [omega_0, alpha_0, beta_0, ..., omega_{k-1}, alpha_{k-1}, beta_{k-1}, trans_params].
        """
        k = self.k_regimes
        y = self.endog
        var_y = max(float(np.var(y)), 1e-12)
        params_list: list[float] = []

        for s in range(k):
            # Different initial GARCH params per regime
            scale = 0.5 + s * 1.0  # regime 0: low vol, regime 1: high vol
            alpha = 0.05 + s * 0.05
            beta = 0.85 - s * 0.10
            omega = var_y * scale * (1.0 - alpha - beta)
            params_list.extend([omega, alpha, beta])

        # Transition params: persistent regimes (p_ii ~ 0.95)
        stay = np.log(0.05 / 0.95)
        params_list.extend([stay] * (k * (k - 1)))

        return np.array(params_list)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        names: list[str] = []
        for s in range(k):
            names.extend([f"omega_{s}", f"alpha_{s}", f"beta_{s}"])
        names.extend([f"p_{i}{j}" for i in range(k) for j in range(k) if i != j])
        return names

    # --- Unconstrained reparametrisation for the optimiser ---

    def _to_unconstrained(self, params: NDArray[np.float64]) -> NDArray[np.float64]:
        """Map natural parameters to the unconstrained optimiser space."""
        k = self.k_regimes
        out: list[float] = []
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            persistence = min(max(alpha + beta, 1e-6), _MAX_PERSISTENCE - 1e-6)
            frac = min(max(alpha / persistence, 1e-6), 1.0 - 1e-6)
            out.append(float(np.log(max(omega, 1e-12))))
            ratio = persistence / _MAX_PERSISTENCE
            out.append(float(np.log(ratio / (1.0 - ratio))))
            out.append(float(np.log(frac / (1.0 - frac))))
        out.extend(np.asarray(params[-k * (k - 1) :], dtype=np.float64).tolist())
        return np.array(out, dtype=np.float64)

    def _from_unconstrained(self, z: NDArray[np.float64]) -> NDArray[np.float64]:
        """Map optimiser parameters back to the natural parametrisation."""
        k = self.k_regimes
        out = np.zeros(3 * k + k * (k - 1))
        for s in range(k):
            z_omega = float(np.clip(z[3 * s], -60.0, 20.0))
            persistence = _MAX_PERSISTENCE / (1.0 + np.exp(-float(np.clip(z[3 * s + 1], -30, 30))))
            frac = 1.0 / (1.0 + np.exp(-float(np.clip(z[3 * s + 2], -30, 30))))
            out[3 * s] = np.exp(z_omega)
            out[3 * s + 1] = persistence * frac
            out[3 * s + 2] = persistence * (1.0 - frac)
        out[3 * k :] = z[3 * k :]
        return out

    # --- Estimation ---

    def fit(
        self,
        method: str = "mle",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
        compute_se: bool = True,
        disp: bool | None = None,
    ) -> RegimeResults:
        """Fit the MS-GARCH model by direct numerical maximisation.

        Parameters
        ----------
        method : str
            Kept for API compatibility ('mle').
        maxiter : int
            Maximum number of optimiser iterations.
        em_iter : int
            Unused (kept for API compatibility).
        tol : float
            Optimiser tolerance.
        verbose : bool
            Print progress information.
        compute_se : bool
            Compute numerical-Hessian standard errors.
        disp : bool, optional
            Alias for ``verbose``.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import standard_errors
        from archbox.regime.results import RegimeResults

        if disp is not None:
            verbose = bool(disp)

        k = self.k_regimes
        start = np.asarray(self.start_params, dtype=np.float64)
        z0 = self._to_unconstrained(start)
        scale = float(max(self.nobs, 1))

        def negloglike(z: NDArray[np.float64]) -> float:
            params = self._from_unconstrained(np.asarray(z, dtype=np.float64))
            ergodic = HamiltonFilter.ergodic_probabilities(self._extract_transition_matrix(params))
            try:
                value = self.loglike(params, init_probs=ergodic)
            except (ValueError, np.linalg.LinAlgError):
                return 1e10
            if not np.isfinite(value):
                return 1e10
            return -value / scale

        n_z = z0.size
        res = minimize(
            negloglike,
            z0,
            method="L-BFGS-B",
            options={"maxiter": maxiter, "maxfun": 200 * n_z, "ftol": tol, "gtol": 1e-8},
        )
        best_z = np.asarray(res.x, dtype=np.float64)
        best_val = float(res.fun)
        converged = bool(res.success)

        if not converged:
            # Bounded derivative-free polish (the numerical gradient can stall
            # in the flat directions of the persistence reparametrisation).
            res2 = minimize(
                negloglike,
                best_z,
                method="Nelder-Mead",
                options={
                    "maxiter": 200 * n_z,
                    "maxfev": 400 * n_z,
                    "xatol": 1e-8,
                    "fatol": 1e-10,
                },
            )
            if float(res2.fun) <= best_val:
                improvement = best_val - float(res2.fun)
                best_z = np.asarray(res2.x, dtype=np.float64)
                best_val = float(res2.fun)
                converged = bool(res2.success) or improvement < 1e-8

        params = self._from_unconstrained(best_z)
        transition_matrix = self._extract_transition_matrix(params)
        init_probs = HamiltonFilter.ergodic_probabilities(transition_matrix)

        sigma2, _h, _filtered_gray, log_eta = self._gray_recursion(params, init_probs)
        hfilter = HamiltonFilter()
        filtered, predicted, loglike, _ = hfilter.filter_vectorized(
            log_eta, transition_matrix, init_probs
        )
        smoothed = KimSmoother().smooth_vectorized(filtered, predicted, transition_matrix)

        if verbose:
            print(f"  MS-GARCH MLE: loglike = {loglike:.4f}, converged = {converged}")

        self._transition_matrix = transition_matrix
        self._init_probs = init_probs
        self._params = params
        self._last_filtered_probs = filtered[-1].copy()
        self._is_fitted = True

        std_errs: NDArray[np.float64] | None = None
        if compute_se:
            std_errs = standard_errors(lambda p: self.loglike(p, init_probs=init_probs), params)

        return RegimeResults(
            params=params,
            regime_params=self._extract_regime_params(params),
            transition_matrix=transition_matrix,
            filtered_probs=filtered,
            smoothed_probs=smoothed,
            predicted_probs=predicted,
            loglike=loglike,
            nobs=self.nobs,
            k_regimes=k,
            model_name=self.model_name,
            param_names=self.param_names,
            converged=converged,
            n_iter=int(getattr(res, "nit", 0)),
            nobs_effective=self.nobs_effective,
            init_probs=init_probs,
            std_errors=std_errs,
            conditional_variances=sigma2,
        )

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    # --- Forecasting and simulation ---

    def _regime_forecast_moments(
        self,
        params: NDArray[np.float64],
        horizon: int,
        regime_probs: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Regime-conditional variance forecasts (the mean is zero).

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        horizon : int
            Forecast horizon.
        regime_probs : ndarray
            Predicted regime probabilities, shape (horizon, k).

        Returns
        -------
        tuple
            (means, variances), both shape (horizon, k).
        """
        k = self.k_regimes
        omega, alpha, beta = self._garch_arrays(params)
        _, h_collapsed, _, _ = self._gray_recursion(params)

        means = np.zeros((horizon, k))
        variances = np.zeros((horizon, k))

        eps2_last = float(self.endog[-1] ** 2)
        h_last = float(h_collapsed[-1])

        for h in range(horizon):
            if h == 0:
                variances[0] = omega + alpha * eps2_last + beta * h_last
            else:
                prev = float(np.sum(regime_probs[h - 1] * variances[h - 1]))
                variances[h] = omega + (alpha + beta) * prev
            np.maximum(variances[h], 1e-14, out=variances[h])

        return means, variances

    def _simulate_observations(
        self,
        params: NDArray[np.float64],
        regimes: NDArray[np.int64],
        rng: np.random.Generator,
    ) -> NDArray[np.float64]:
        """Simulate a Gray MS-GARCH path given a regime sequence."""
        n_obs = regimes.size
        omega, alpha, beta = self._garch_arrays(params)
        persistence = np.maximum(alpha + beta, 0.0)
        uncond = omega / np.maximum(1.0 - persistence, 1e-6)

        y = np.zeros(n_obs)
        h_prev = float(np.mean(uncond))
        eps2_prev = h_prev
        for t in range(n_obs):
            s = int(regimes[t])
            sigma2_t = max(omega[s] + alpha[s] * eps2_prev + beta[s] * h_prev, 1e-14)
            y[t] = np.sqrt(sigma2_t) * rng.standard_normal()
            eps2_prev = y[t] ** 2
            h_prev = sigma2_t
        return y
