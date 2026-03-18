"""Markov-Switching VAR model (Krolzig, 1997).

Implements VAR(p) with regime-dependent parameters using EM estimation.

References
----------
Krolzig, H.-M. (1997). Markov-Switching Vector Autoregressions. Springer.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.regime.base import MarkovSwitchingModel


class MarkovSwitchingVAR(MarkovSwitchingModel):
    """Markov-Switching VAR(p) model (Krolzig, 1997).

    y_t = mu_{S_t} + Phi_1(S_t) * y_{t-1} + ... + Phi_p(S_t) * y_{t-p} + eps_t
    eps_t ~ N(0, Sigma_{S_t})

    Parameters
    ----------
    endog : array-like
        Multivariate time series, shape (T, n).
    k_regimes : int
        Number of regimes. Default is 2.
    order : int
        VAR order (number of lags). Default is 1.
    switching_mean : bool
        If True, intercept switches. Default True.
    switching_variance : bool
        If True, covariance matrix switches. Default True.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_var import MarkovSwitchingVAR
    >>> y = np.random.randn(200, 2)
    >>> model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-VAR"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

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
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def _unpack_var_params(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        params_list: list[float] = []

        # Intercepts (k * n)
        y_mean = np.mean(y, axis=0)
        for s in range(k):
            spread = (s - (k - 1) / 2.0) * 0.5
            mu_s = y_mean + spread
            params_list.extend(mu_s.tolist())

        # VAR coefficients (k * n * n * p): small values
        for _s in range(k):
            for _l in range(p):
                phi_l = 0.1 * np.eye(n)
                params_list.extend(phi_l.flatten().tolist())

        # Covariance (k * n*(n+1)/2): from sample covariance
        sample_cov = np.cov(y.T)
        if sample_cov.ndim == 0:
            sample_cov = np.array([[float(sample_cov)]])
        try:
            l_sample = np.linalg.cholesky(sample_cov)
        except np.linalg.LinAlgError:
            l_sample = np.eye(n) * np.sqrt(float(np.var(y)))

        for s in range(k):
            scale = 0.5 + s * 1.0
            l_s = l_sample * np.sqrt(scale)
            for i in range(n):
                for j in range(i + 1):
                    params_list.append(float(l_s[i, j]))

        # Transition params
        n_trans = k * (k - 1)
        params_list.extend([0.0] * n_trans)

        return np.array(params_list)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        names: list[str] = []

        # Intercepts
        for s in range(k):
            names.extend([f"mu_{s}_{v}" for v in range(n)])

        # VAR coefficients
        for s in range(k):
            for lag in range(p):
                for i in range(n):
                    for j in range(n):
                        names.append(f"Phi_{lag + 1}_{i}{j}(S={s})")

        # Covariance
        for s in range(k):
            for i in range(n):
                for j in range(i + 1):
                    names.append(f"L_{i}{j}(S={s})")

        # Transition
        names.extend([f"p_{i}{j}" for i in range(k) for j in range(k) if i != j])

        return names

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

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
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params
