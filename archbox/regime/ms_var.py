"""Markov-Switching VAR model (Krolzig, 1997).

Implements VAR(p) with regime-dependent parameters using EM estimation.
The first ``p`` observations are conditioned on (they are not part of the
likelihood), and the M-step is the exact weighted multivariate least
squares maximiser for the intercepts and the VAR coefficient matrices.

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
    >>> results = model.fit(verbose=False)
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

        if self.order < 1:
            msg = f"order must be >= 1, got {self.order}"
            raise ValueError(msg)
        if self.order >= self.nobs:
            msg = f"order ({self.order}) must be < nobs ({self.nobs})"
            raise ValueError(msg)

        self._t_start = self.order
        self._effective_nobs = self.nobs - self.order
        self._design_cache: tuple[NDArray[np.float64], NDArray[np.float64]] | None = None

    def _design_matrices(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Stacked lag matrix and dependent block over the effective sample.

        Returns
        -------
        tuple
            (Z, Y) with Z of shape (T-p, n*p) holding
            [y_{t-1}, ..., y_{t-p}] and Y of shape (T-p, n).
        """
        if self._design_cache is None:
            n = self.n_vars
            p = self.order
            n_obs = self.nobs
            y = self.endog
            z_mat = np.zeros((n_obs - p, n * p))
            for lag in range(p):
                z_mat[:, lag * n : (lag + 1) * n] = y[p - lag - 1 : n_obs - lag - 1, :]
            self._design_cache = (z_mat, y[p:, :].copy())
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
        n_obs = self.nobs
        n = self.n_vars
        p = self.order

        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.zeros(n_obs)

        sigma = sigma + 1e-8 * np.eye(n)
        try:
            chol = np.linalg.cholesky(sigma)
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            shift = max(-float(np.min(eigvals)) + 1e-6, 1e-6)
            sigma = sigma + shift * np.eye(n)
            chol = np.linalg.cholesky(sigma)

        log_det = 2.0 * float(np.sum(np.log(np.diag(chol))))
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        z_mat, y_dep = self._design_matrices()
        resid = y_dep - mu - z_mat @ phi.T  # (T-p, n)
        # solve_triangular-free Mahalanobis distance via the Cholesky factor
        sol = np.linalg.solve(chol, resid.T)  # (n, T-p)
        quad = np.sum(sol**2, axis=0)

        ll[p:] = const - 0.5 * quad
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
        mu = np.asarray(params[idx + mu_start : idx + mu_start + n], dtype=np.float64).copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = np.asarray(phi_flat, dtype=np.float64).reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        chol = np.zeros((n, n))
        rows, cols = np.tril_indices(n)
        chol[rows, cols] = l_flat
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def _cov_offset(self, regime: int) -> int:
        """Parameter offset of the Cholesky block of a regime."""
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        cov_size = n * (n + 1) // 2
        return k * n + k * n * n * p + regime * cov_size

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        The pooled VAR is estimated by OLS and the observations are split
        into ``k`` groups by the quantiles of the residual projection on
        the leading principal component.  Each regime starts from the
        pooled coefficients with its group's residual mean added to the
        intercept and its group's residual covariance; the chain starts
        persistent (p_ii = 0.9).  Separating the regimes in the mean from
        the very first E-step avoids the poor local optimum that flat
        starting values fall into.
        """
        k = self.k_regimes
        n = self.n_vars
        params_list: list[float] = []

        z_mat, y_dep = self._design_matrices()
        n_eff = y_dep.shape[0]
        x_mat = np.column_stack([np.ones(n_eff), z_mat])
        beta = np.asarray(np.linalg.lstsq(x_mat, y_dep, rcond=None)[0], dtype=np.float64)
        resid = y_dep - x_mat @ beta
        intercept = np.asarray(beta[0], dtype=np.float64)
        phi = np.asarray(beta[1:], dtype=np.float64).T  # (n, n*p)

        resid_cov = resid.T @ resid / max(n_eff, 1) + 1e-8 * np.eye(n)
        eigvecs = np.linalg.eigh(resid_cov)[1]
        score = resid @ eigvecs[:, -1]
        groups = np.array_split(np.argsort(score), k)

        shifts: list[NDArray[np.float64]] = []
        chols: list[NDArray[np.float64]] = []
        for idx in groups:
            if idx.size >= n + 2:
                block = resid[idx]
                shift = np.asarray(np.mean(block, axis=0), dtype=np.float64)
                centered = block - shift
                cov_s = centered.T @ centered / block.shape[0]
            else:
                shift = np.zeros(n)
                cov_s = resid_cov
            cov_s = cov_s + 1e-6 * np.trace(resid_cov) / n * np.eye(n)
            try:
                chol_s = np.linalg.cholesky(cov_s)
            except np.linalg.LinAlgError:
                chol_s = np.linalg.cholesky(resid_cov)
            shifts.append(shift)
            chols.append(chol_s)

        # Intercepts (k * n)
        for s in range(k):
            params_list.extend((intercept + shifts[s]).tolist())

        # VAR coefficients (k * n * n * p): pooled OLS estimates
        for _s in range(k):
            params_list.extend(phi.reshape(-1).tolist())

        # Covariance (k * n*(n+1)/2)
        rows, cols = np.tril_indices(n)
        for s in range(k):
            params_list.extend(chols[s][rows, cols].tolist())

        # Transition params: persistent regimes (p_ii = 0.9)
        off = 0.1 / max(k - 1, 1)
        params_list.extend([float(np.log(off / 0.9))] * (k * (k - 1)))

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

        Weighted multivariate least squares per regime for the intercept
        and the VAR coefficient matrices (weights = smoothed
        probabilities), followed by the weighted residual covariance.

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
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        new_params = np.asarray(params, dtype=np.float64).copy()

        z_mat, y_dep = self._design_matrices()
        n_eff = y_dep.shape[0]
        x_mat = np.column_stack([np.ones(n_eff), z_mat])  # (T-p, 1+n*p)
        rows, cols = np.tril_indices(n)

        for s in range(k):
            weights = np.maximum(smoothed[:, s], 0.0)
            w_sum = float(weights.sum())
            if w_sum < 1e-12:
                continue

            # --- Weighted LS for (intercept, Phi) ---
            xw = x_mat * weights[:, None]
            xwx = x_mat.T @ xw
            xwy = xw.T @ y_dep
            ridge = 1e-10 * np.trace(xwx) / max(xwx.shape[0], 1)
            try:
                beta = np.linalg.solve(xwx + max(ridge, 1e-12) * np.eye(xwx.shape[0]), xwy)
            except np.linalg.LinAlgError:
                beta = np.linalg.lstsq(xwx, xwy, rcond=None)[0]

            mu_s = np.asarray(beta[0], dtype=np.float64)
            phi_s = np.asarray(beta[1:], dtype=np.float64).T  # (n, n*p)

            if self.switching_mean:
                new_params[s * n : (s + 1) * n] = mu_s
            elif s == 0:
                for j in range(k):
                    new_params[j * n : (j + 1) * n] = mu_s

            phi_size = n * n * p
            phi_off = k * n + s * phi_size
            new_params[phi_off : phi_off + phi_size] = phi_s.reshape(-1)

            # --- Weighted residual covariance ---
            resid = y_dep - mu_s - z_mat @ phi_s.T
            sigma_s = (resid * weights[:, None]).T @ resid / w_sum
            sigma_s = 0.5 * (sigma_s + sigma_s.T) + 1e-8 * np.eye(n)
            try:
                l_s = np.linalg.cholesky(sigma_s)
            except np.linalg.LinAlgError:
                eigvals = np.linalg.eigvalsh(sigma_s)
                shift = max(-float(np.min(eigvals)) + 1e-6, 1e-6)
                l_s = np.linalg.cholesky(sigma_s + shift * np.eye(n))

            cov_off = self._cov_offset(s)
            new_params[cov_off : cov_off + rows.size] = l_s[rows, cols]

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

    def _regime_coefficients(
        self,
        params: NDArray[np.float64],
    ) -> tuple[list[NDArray[np.float64]], list[NDArray[np.float64]]] | None:
        """VAR coefficient matrices (n, n*p) and intercepts per regime."""
        coefs: list[NDArray[np.float64]] = []
        intercepts: list[NDArray[np.float64]] = []
        for s in range(self.k_regimes):
            mu, phi, _ = self._unpack_var_params(params, s)
            coefs.append(phi)
            intercepts.append(mu)
        return coefs, intercepts

    # --- Forecasting and simulation ---

    def _regime_forecast_moments(
        self,
        params: NDArray[np.float64],
        horizon: int,
        regime_probs: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Iterated regime-conditional forecast moments.

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
            (means, covariances) of shapes (horizon, k, n) and
            (horizon, k, n, n).
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        unpacked = [self._unpack_var_params(params, s) for s in range(k)]

        hist = [self.endog[self.nobs - 1 - lag].copy() for lag in range(p)]  # y_{T-1-lag}
        hist_cov = [np.zeros((n, n)) for _ in range(p)]

        means = np.zeros((horizon, k, n))
        covs = np.zeros((horizon, k, n, n))

        for h in range(horizon):
            for s in range(k):
                mu_s, phi_s, sigma_s = unpacked[s]
                mean_hs = mu_s.copy()
                cov_hs = sigma_s.copy()
                for lag in range(p):
                    phi_l = phi_s[:, lag * n : (lag + 1) * n]
                    mean_hs = mean_hs + phi_l @ hist[lag]
                    cov_hs = cov_hs + phi_l @ hist_cov[lag] @ phi_l.T
                means[h, s] = mean_hs
                covs[h, s] = cov_hs

            mix_mean = np.einsum("k,kn->n", regime_probs[h], means[h])
            outer = np.einsum("kn,km->knm", means[h], means[h])
            mix_cov = np.einsum("k,knm->nm", regime_probs[h], covs[h] + outer) - np.outer(
                mix_mean, mix_mean
            )
            hist.insert(0, mix_mean)
            hist_cov.insert(0, mix_cov)
            hist = hist[:p]
            hist_cov = hist_cov[:p]

        return means, covs

    def _simulate_observations(
        self,
        params: NDArray[np.float64],
        regimes: NDArray[np.int64],
        rng: np.random.Generator,
    ) -> NDArray[np.float64]:
        """Simulate an MS-VAR path given a regime sequence."""
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        n_obs = regimes.size
        unpacked = [self._unpack_var_params(params, s) for s in range(k)]
        chols = [np.linalg.cholesky(u[2] + 1e-10 * np.eye(n)) for u in unpacked]

        y = np.zeros((n_obs, n))
        for t in range(n_obs):
            s = int(regimes[t])
            mu_s, phi_s, _ = unpacked[s]
            value = mu_s + chols[s] @ rng.standard_normal(n)
            for lag in range(p):
                if t - lag - 1 >= 0:
                    phi_l = phi_s[:, lag * n : (lag + 1) * n]
                    value = value + phi_l @ y[t - lag - 1]
            y[t] = value
        return y
