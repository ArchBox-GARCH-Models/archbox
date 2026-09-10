"""EGARCH - Exponential GARCH model (Nelson, 1991).

log(sigma^2_t) = omega + alpha * |z_{t-1}| + gamma * z_{t-1} + beta * log(sigma^2_{t-1})

onde z_t = eps_t / sigma_t (residuo padronizado).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel
from archbox.utils.validation import validate_positive_integer


class EGARCH(VolatilityModel):
    """Exponential GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of lagged log-variance terms (beta). Default 1.
    q : int
        Number of lagged shock terms (alpha, gamma). Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution: 'normal', 'studentt', etc.
    """

    volatility_process = "EGARCH"

    def __init__(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for optimization."""
        omega = np.log(np.var(self.endog)) * 0.05
        alphas = np.full(self.q, 0.1)
        gammas = np.full(self.q, -0.05)
        betas = np.full(self.p, 0.95)
        return np.concatenate([[omega], alphas, gammas, betas])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["omega"]
        names += [f"alpha[{i + 1}]" for i in range(self.q)]
        names += [f"gamma[{i + 1}]" for i in range(self.q)]
        names += [f"beta[{i + 1}]" for i in range(self.p)]
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    @property
    def num_params(self) -> int:
        """Number of model parameters."""
        return 1 + 2 * self.q + self.p

    # --- Model-level moments and forecasts ---

    #: Monte-Carlo settings for multi-step forecasts (fixed for reproducibility).
    FORECAST_PATHS: int = 10_000
    FORECAST_SEED: int = 20240101

    def _egarch_blocks(
        self, var_params: NDArray[np.float64]
    ) -> tuple[float, NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Split the parameter vector into (omega, alphas, gammas, betas)."""
        params = np.asarray(var_params, dtype=np.float64)
        omega = float(params[0])
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        return omega, alphas, gammas, betas

    def persistence(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """EGARCH persistence: ``sum(beta)`` on the log-variance.

        The ARCH block ``alpha_i(|z|-E|z|) + gamma_i z`` has zero mean, so the
        autoregressive decay of ``log sigma^2_t`` is governed by the betas alone.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha.., gamma.., beta..]``.
        dist_params : ndarray, optional
            Unused: the log-variance decay does not depend on the innovation law.

        Returns
        -------
        float
            Sum of the beta coefficients.
        """
        del dist_params
        _, _, _, betas = self._egarch_blocks(var_params)
        return float(np.sum(betas))

    def unconditional_variance(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """Long-run variance level ``exp(omega / (1 - sum(beta)))``.

        ``E[log sigma^2] = omega / (1 - sum(beta))`` because the innovation
        block is mean zero; exponentiating gives the long-run *median*
        variance level, which is the natural EGARCH analogue of
        ``omega / (1 - persistence)``.

        Parameters
        ----------
        var_params : ndarray
            Variance block.
        dist_params : ndarray, optional
            Unused.

        Returns
        -------
        float
            Long-run variance level, or ``inf`` when ``sum(beta) >= 1``.
        """
        pers = self.persistence(var_params, dist_params)
        if not np.isfinite(pers) or pers >= 1.0:
            return float("inf")
        omega, _, _, _ = self._egarch_blocks(var_params)
        return float(np.exp(omega / (1.0 - pers)))

    def forecast_variance(
        self,
        var_params: NDArray[np.float64],
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        horizon: int = 1,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Multi-step EGARCH variance forecast.

        The one-step forecast is the exact log-variance recursion (all inputs
        are observed). For ``h > 1`` the log-normal expectation
        ``E[sigma^2_{T+h}]`` has no simple closed form for general (p, q), so
        it is obtained by **Monte-Carlo simulation with a fixed seed**
        (``FORECAST_PATHS`` paths, seed ``FORECAST_SEED``): future innovations
        are drawn from the fitted conditional distribution and the log-variance
        recursion is iterated path by path. Results are therefore deterministic
        and always finite and strictly positive.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha.., gamma.., beta..]``.
        resids : ndarray
            In-sample residuals.
        sigma2 : ndarray
            In-sample conditional variance path.
        horizon : int
            Number of steps ahead (>= 1).
        dist_params : ndarray, optional
            Fitted distribution shape parameters used to draw innovations.

        Returns
        -------
        ndarray
            Forecast variances, shape ``(horizon,)``.
        """
        h_max = validate_positive_integer(horizon, "horizon")
        omega, alphas, gammas, betas = self._egarch_blocks(var_params)
        const = np.sqrt(2.0 / np.pi)  # E|z| used by the fitted recursion

        sigma2_arr = np.maximum(np.asarray(sigma2, dtype=np.float64).ravel(), 1e-12)
        resid_arr = np.asarray(resids, dtype=np.float64).ravel()
        fill = float(sigma2_arr[-1]) if sigma2_arr.size else self._backcast(self.endog)

        n_paths = int(self.FORECAST_PATHS)
        rng = np.random.default_rng(self.FORECAST_SEED)

        # History replicated across simulation paths (oldest entry first).
        log_s2_tail = np.log(self._tail(sigma2_arr, self.p, fill))
        n_z = max(self.q, 1)
        sigma_tail = np.sqrt(self._tail(sigma2_arr, n_z, fill))
        z_tail = self._tail(resid_arr, n_z, 0.0) / np.maximum(sigma_tail, 1e-12)

        log_s2_hist = [np.full(n_paths, v, dtype=np.float64) for v in log_s2_tail]
        z_hist = [np.full(n_paths, v, dtype=np.float64) for v in z_tail]

        out = np.empty(h_max, dtype=np.float64)
        for h in range(h_max):
            log_next = np.full(n_paths, omega, dtype=np.float64)
            for j in range(self.p):
                log_next += betas[j] * log_s2_hist[-1 - j]
            for i in range(self.q):
                z_lag = z_hist[-1 - i]
                log_next += alphas[i] * (np.abs(z_lag) - const) + gammas[i] * z_lag
            log_next = np.clip(log_next, -700.0, 700.0)
            sigma2_next = np.exp(log_next)
            out[h] = max(float(np.mean(sigma2_next)), 1e-12)
            log_s2_hist.append(log_next)
            z_hist.append(self._simulate_innovations(n_paths, rng, dist_params))
        return out
