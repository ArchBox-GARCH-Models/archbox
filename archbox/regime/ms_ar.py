"""Markov-Switching Autoregressive model (Hamilton, 1989).

Implements the classic MS(k)-AR(p) model where the mean, variance,
and optionally AR coefficients switch between regimes.

References
----------
Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle.
Econometrica, 57(2), 357-384.

Hamilton, J.D. (1994). Time Series Analysis. Princeton University Press.
Chapter 22.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.regime.base import MarkovSwitchingModel


class MarkovSwitchingAR(MarkovSwitchingModel):
    """Markov-Switching AR(p) model (Hamilton, 1989).

    y_t - mu_{S_t} = phi_1 * (y_{t-1} - mu_{S_{t-1}}) + ... + eps_t
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
    >>> gdp = load_dataset('us_gdp_quarterly')
    >>> growth = gdp['growth'].to_numpy()
    >>> model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
    >>> results = model.fit()
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
        self._effective_nobs = self.nobs - self.order

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

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
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            Initial parameters.
        """
        k = self.k_regimes
        p = self.order
        y = self.endog
        params_list: list[float] = []

        # Means: spread across data range
        if self.switching_mean:
            quantiles = np.linspace(0.2, 0.8, k)
            mus = [float(np.quantile(y, q)) for q in quantiles]
            params_list.extend(mus)
        else:
            params_list.append(float(np.mean(y)))

        # AR coefficients: start near zero
        if self.switching_ar:
            for _s in range(k):
                ar_init = [0.1 / (lag + 1) for lag in range(p)]
                params_list.extend(ar_init)
        else:
            ar_init = [0.1 / (lag + 1) for lag in range(p)]
            params_list.extend(ar_init)

        # Sigmas
        std_y = float(np.std(y))
        if self.switching_variance:
            sigmas = [std_y * (0.5 + s * 0.5) for s in range(k)]
            params_list.extend(sigmas)
        else:
            params_list.append(std_y)

        # Transition params
        n_trans = k * (k - 1)
        params_list.extend([0.0] * n_trans)

        return np.array(params_list)

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

    def _update_means(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def _wls_ar_coeffs(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def _update_ar_coeffs(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def _compute_regime_residuals(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def _update_variances(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params
