"""Markov-Switching Autoregressive model (Hamilton, 1989).

Implements the MS(k)-AR(p) model where the mean, variance, and optionally
the AR coefficients switch between regimes.

Specification
-------------
This module implements the Kim-style approximation in which the state
enters only through the *current* regime, the lags being mean-adjusted
with the current regime mean::

    y_t = mu_{S_t} + sum_{l=1}^p phi_l(S_t) * (y_{t-l} - mu_{S_t}) + eps_t
    eps_t ~ N(0, sigma^2_{S_t})

which is algebraically identical to the intercept-switching form

    y_t = c_{S_t} + sum_l phi_l(S_t) y_{t-l} + eps_t,
    c_s = mu_s * (1 - sum_l phi_l(s))

used by, among others, the R package ``MSwM``.  The exact Hamilton (1989)
MS-AR (in which the lags are adjusted with the *lagged* regime means, so
that the effective state is (S_t, ..., S_{t-p})) is **not** used here: it
requires a k^{p+1}-state filter.  The first ``p`` observations are
conditioned on: they are not part of the likelihood and
``nobs_effective = nobs - p``.

References
----------
Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle.
Econometrica, 57(2), 357-384.

Hamilton, J.D. (1994). Time Series Analysis. Princeton University Press.
Chapter 22.

Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching.
Journal of Econometrics, 60(1-2), 1-22.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.regime.base import MarkovSwitchingModel


class MarkovSwitchingAR(MarkovSwitchingModel):
    """Markov-Switching AR(p) model (Hamilton, 1989).

    y_t - mu_{S_t} = phi_1 * (y_{t-1} - mu_{S_t}) + ... + eps_t
    eps_t ~ N(0, sigma^2_{S_t})

    Parameters
    ----------
    endog : array-like
        Time series of observations, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.
    order : int
        AR order (number of lags). Default is 4.
    switching_mean : bool
        If True, the mean switches between regimes. Default True.
    switching_variance : bool
        If True, the variance switches between regimes. Default True.
    switching_ar : bool
        If True, AR coefficients switch between regimes. Default False.

    Examples
    --------
    >>> from archbox.regime.ms_ar import MarkovSwitchingAR
    >>> from archbox.datasets import load_dataset
    >>> gdp = load_dataset('us_gdp')
    >>> growth = gdp['growth'].to_numpy()
    >>> model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
    >>> results = model.fit(verbose=False)
    >>> print(results.summary())
    """

    model_name: str = "MS-AR"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        if self.order < 0:
            msg = f"order must be >= 0, got {self.order}"
            raise ValueError(msg)
        if self.order >= self.nobs:
            msg = f"order ({self.order}) must be < nobs ({self.nobs})"
            raise ValueError(msg)

        self._t_start = self.order
        self._effective_nobs = self.nobs - self.order
        self._design_cache: tuple[NDArray[np.float64], NDArray[np.float64]] | None = None

    # --- Parameter layout helpers ---

    def _block_offsets(self) -> tuple[int, int, int, int, int]:
        """Return (mu_off, n_mu, ar_off, n_ar, sigma_off) parameter offsets."""
        k = self.k_regimes
        p = self.order
        n_mu = k if self.switching_mean else 1
        n_ar = k * p if self.switching_ar else p
        return 0, n_mu, n_mu, n_ar, n_mu + n_ar

    def _set_mu(self, params: NDArray[np.float64], regime: int, value: float) -> None:
        """Write the mean of a regime into the parameter vector."""
        mu_off, _, _, _, _ = self._block_offsets()
        params[mu_off + (regime if self.switching_mean else 0)] = value

    def _set_phi(self, params: NDArray[np.float64], regime: int, phi: NDArray[np.float64]) -> None:
        """Write the AR coefficients of a regime into the parameter vector."""
        p = self.order
        if p == 0:
            return
        _, _, ar_off, _, _ = self._block_offsets()
        start = ar_off + (regime * p if self.switching_ar else 0)
        params[start : start + p] = phi

    def _set_sigma(self, params: NDArray[np.float64], regime: int, value: float) -> None:
        """Write the standard deviation of a regime into the parameter vector."""
        _, _, _, _, sigma_off = self._block_offsets()
        params[sigma_off + (regime if self.switching_variance else 0)] = value

    def _design_matrices(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Lagged design matrix and dependent variable over the effective sample.

        Returns
        -------
        tuple
            (X, y_dep) with X of shape (T-p, p) (column l holds y_{t-l-1})
            and y_dep of shape (T-p,).
        """
        if self._design_cache is None:
            p = self.order
            n = self.nobs
            y = self.endog
            x_mat = np.zeros((n - p, p))
            for lag in range(p):
                x_mat[:, lag] = y[p - lag - 1 : n - lag - 1]
            self._design_cache = (x_mat, y[p:].copy())
        return self._design_cache

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        The first ``order`` entries are conditioned on and returned as
        zeros (they are excluded from the likelihood).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.zeros(n)

        if p == 0:
            resid = y - mu
        else:
            x_mat, y_dep = self._design_matrices()
            resid = y_dep - mu - (x_mat - mu) @ phi

        ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
        return ll

    def _unpack_params(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        p = self.order
        mu_off, _, ar_off, _, sigma_off = self._block_offsets()

        mu = float(params[mu_off + (regime if self.switching_mean else 0)])

        ar_start = ar_off + (regime * p if self.switching_ar else 0)
        phi = np.asarray(params[ar_start : ar_start + p], dtype=np.float64).copy()

        sigma = max(
            abs(float(params[sigma_off + (regime if self.switching_variance else 0)])), 1e-6
        )

        return mu, phi, sigma

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        The pooled AR(p) is estimated by OLS and its residuals are split
        into ``k`` quantile groups; each regime starts from the pooled AR
        coefficients, with its group's mean residual added to the
        intercept and its group's residual standard deviation.  The chain
        starts persistent (p_ii = 0.9).  Separating the regimes in the
        mean from the first E-step keeps EM away from the flat local
        optimum that uninformative starting values fall into.

        Returns
        -------
        ndarray
            Initial parameters.
        """
        k = self.k_regimes
        params_list: list[float] = []

        x_mat, y_dep = self._design_matrices()
        n_eff = y_dep.size
        design = np.column_stack([np.ones(n_eff), x_mat])
        beta = np.asarray(np.linalg.lstsq(design, y_dep, rcond=None)[0], dtype=np.float64)
        resid = y_dep - design @ beta
        intercept = float(beta[0])
        phi = beta[1:]

        groups = np.array_split(np.argsort(resid), k)
        shifts: list[float] = []
        sigmas: list[float] = []
        pooled_sigma = max(float(np.std(resid)), 1e-6)
        for idx in groups:
            if idx.size >= 2:
                block = resid[idx]
                shifts.append(float(np.mean(block)))
                sigmas.append(max(float(np.std(block - np.mean(block))), 1e-6))
            else:
                shifts.append(0.0)
                sigmas.append(pooled_sigma)

        # Means (via the implied intercepts)
        if self.switching_mean:
            params_list.extend(self._mu_from_intercept(intercept + shift, phi) for shift in shifts)
        else:
            params_list.append(self._mu_from_intercept(intercept, phi))

        # AR coefficients: pooled OLS estimates
        if self.switching_ar:
            for _s in range(k):
                params_list.extend(phi.tolist())
        else:
            params_list.extend(phi.tolist())

        # Sigmas
        if self.switching_variance:
            params_list.extend(sigmas)
        else:
            params_list.append(pooled_sigma)

        # Transition params: persistent regimes (p_ii = 0.9)
        off = 0.1 / max(k - 1, 1)
        params_list.extend([float(np.log(off / 0.9))] * (k * (k - 1)))

        return np.array(params_list, dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        p = self.order
        names: list[str] = []

        # Means
        if self.switching_mean:
            names.extend([f"mu_{s}" for s in range(k)])
        else:
            names.append("mu")

        # AR coefficients
        if self.switching_ar:
            for s in range(k):
                names.extend([f"phi_{lag + 1}(S={s})" for lag in range(p)])
        else:
            names.extend([f"phi_{lag + 1}" for lag in range(p)])

        # Sigmas
        if self.switching_variance:
            names.extend([f"sigma_{s}" for s in range(k)])
        else:
            names.append("sigma")

        # Transition
        names.extend([f"p_{i}{j}" for i in range(k) for j in range(k) if i != j])

        return names

    # --- M-step ---

    @staticmethod
    def _mu_from_intercept(intercept: float, phi: NDArray[np.float64]) -> float:
        """Convert an intercept to the implied regime mean."""
        denom = 1.0 - float(np.sum(phi))
        if abs(denom) < 1e-3:
            denom = 1e-3 if denom >= 0.0 else -1e-3
        return intercept / denom

    def _update_mean_ar(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
    ) -> None:
        """Weighted-least-squares update of means and AR coefficients.

        Maximises the expected complete-data log-likelihood in the
        intercept parametrisation ``y_t = c_s + sum_l phi_l y_{t-l}``,
        which is linear in (c, phi); the regime means follow from
        ``mu_s = c_s / (1 - sum_l phi_l(s))``.

        Parameters
        ----------
        new_params : ndarray
            Parameter vector, modified in place.
        smoothed : ndarray
            Smoothed probabilities over the effective sample, shape (T-p, k).
        """
        k = self.k_regimes
        p = self.order
        x_mat, y_dep = self._design_matrices()
        n_eff = y_dep.size

        if self.switching_ar:
            for s in range(k):
                w = np.maximum(smoothed[:, s], 0.0)
                if w.sum() <= 1e-12:
                    continue
                z_mat = np.column_stack([np.ones(n_eff), x_mat])
                sw = np.sqrt(w)
                beta = np.asarray(
                    np.linalg.lstsq(z_mat * sw[:, None], y_dep * sw, rcond=None)[0],
                    dtype=np.float64,
                )
                phi_s = beta[1:]
                self._set_phi(new_params, s, phi_s)
                self._set_mu(new_params, s, self._mu_from_intercept(float(beta[0]), phi_s))
            return

        # Shared AR coefficients: one stacked weighted regression over all
        # regimes with weights P(S_t=s | Y_T) / sigma_s^2.
        n_c = k if self.switching_mean else 1
        sigmas = np.array([self._unpack_params(new_params, s)[2] for s in range(k)])

        z_mat = np.zeros((k * n_eff, n_c + p))
        weights = np.zeros(k * n_eff)
        target = np.tile(y_dep, k)
        for s in range(k):
            sl = slice(s * n_eff, (s + 1) * n_eff)
            z_mat[sl, s if self.switching_mean else 0] = 1.0
            if p > 0:
                z_mat[sl, n_c:] = x_mat
            weights[sl] = np.maximum(smoothed[:, s], 0.0) / sigmas[s] ** 2

        if weights.sum() <= 1e-12:
            return

        sw = np.sqrt(weights)
        beta = np.asarray(
            np.linalg.lstsq(z_mat * sw[:, None], target * sw, rcond=None)[0], dtype=np.float64
        )
        phi = beta[n_c:]
        for s in range(k):
            self._set_phi(new_params, s, phi)
            c_s = float(beta[s if self.switching_mean else 0])
            self._set_mu(new_params, s, self._mu_from_intercept(c_s, phi))

    def _regime_residuals(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Residuals of a regime over the effective sample."""
        p = self.order
        mu_s, phi_s, _ = self._unpack_params(params, regime)
        if p == 0:
            return self.endog - mu_s
        x_mat, y_dep = self._design_matrices()
        return y_dep - mu_s - (x_mat - mu_s) @ phi_s

    def _update_variances(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
    ) -> None:
        """Weighted update of the regime variances."""
        k = self.k_regimes

        if self.switching_variance:
            for s in range(k):
                resid = self._regime_residuals(new_params, s)
                weights = np.maximum(smoothed[:, s], 0.0)
                w_sum = float(weights.sum())
                if w_sum > 1e-12:
                    var_s = float(np.sum(weights * resid**2)) / w_sum
                    self._set_sigma(new_params, s, max(np.sqrt(var_s), 1e-6))
            return

        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            resid = self._regime_residuals(new_params, s)
            weights = np.maximum(smoothed[:, s], 0.0)
            total_var += float(np.sum(weights * resid**2))
            total_weight += float(weights.sum())
        if total_weight > 1e-12:
            self._set_sigma(new_params, 0, max(np.sqrt(total_var / total_weight), 1e-6))

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Applies the exact conditional maximisers of the expected
        complete-data log-likelihood: a stacked weighted least squares
        for (intercepts, AR coefficients) given the variances, then the
        weighted residual variances.  The two blocks are cycled twice.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities over the effective sample, shape (T-p, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-p-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        new_params = np.asarray(params, dtype=np.float64).copy()
        for _ in range(2):
            self._update_mean_ar(new_params, smoothed)
            self._update_variances(new_params, smoothed)
        return new_params

    # --- Results helpers ---

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            rp["intercept"] = mu * (1.0 - float(np.sum(phi)))
            regime_params[s] = rp
        return regime_params

    def _regime_coefficients(
        self,
        params: NDArray[np.float64],
    ) -> tuple[list[NDArray[np.float64]], list[NDArray[np.float64]]] | None:
        """AR coefficients and intercepts per regime."""
        coefs: list[NDArray[np.float64]] = []
        intercepts: list[NDArray[np.float64]] = []
        for s in range(self.k_regimes):
            mu, phi, _ = self._unpack_params(params, s)
            coefs.append(phi.reshape(1, -1))
            intercepts.append(np.array([mu * (1.0 - float(np.sum(phi)))]))
        return coefs, intercepts

    # --- Forecasting and simulation ---

    def _regime_forecast_moments(
        self,
        params: NDArray[np.float64],
        horizon: int,
        regime_probs: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Iterated regime-conditional forecast moments.

        Future lags are replaced by the mixture forecasts of the previous
        horizons (an iterated, regime-probability-weighted forecast).

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
        p = self.order
        mus = np.array([self._unpack_params(params, s)[0] for s in range(k)])
        phis = np.array([self._unpack_params(params, s)[1] for s in range(k)]).reshape(k, p)
        sigmas = np.array([self._unpack_params(params, s)[2] for s in range(k)])

        hist = list(self.endog[self.nobs - p :]) if p > 0 else []
        hist_var = [0.0] * p

        means = np.zeros((horizon, k))
        variances = np.zeros((horizon, k))

        for h in range(horizon):
            for s in range(k):
                mean_hs = mus[s]
                var_hs = sigmas[s] ** 2
                for lag in range(p):
                    mean_hs += phis[s, lag] * (hist[-1 - lag] - mus[s])
                    var_hs += phis[s, lag] ** 2 * hist_var[-1 - lag]
                means[h, s] = mean_hs
                variances[h, s] = var_hs
            mix_mean = float(np.sum(regime_probs[h] * means[h]))
            mix_var = float(np.sum(regime_probs[h] * (variances[h] + means[h] ** 2)) - mix_mean**2)
            if p > 0:
                hist.append(mix_mean)
                hist_var.append(max(mix_var, 0.0))

        return means, variances

    def _simulate_observations(
        self,
        params: NDArray[np.float64],
        regimes: NDArray[np.int64],
        rng: np.random.Generator,
    ) -> NDArray[np.float64]:
        """Simulate an MS-AR path given a regime sequence."""
        k = self.k_regimes
        p = self.order
        n = regimes.size
        mus = np.array([self._unpack_params(params, s)[0] for s in range(k)])
        phis = np.array([self._unpack_params(params, s)[1] for s in range(k)]).reshape(k, p)
        sigmas = np.array([self._unpack_params(params, s)[2] for s in range(k)])

        y = np.zeros(n)
        for t in range(n):
            s = int(regimes[t])
            value = mus[s] + sigmas[s] * rng.standard_normal()
            for lag in range(p):
                if t - lag - 1 >= 0:
                    value += phis[s, lag] * (y[t - lag - 1] - mus[s])
            y[t] = value
        return y
