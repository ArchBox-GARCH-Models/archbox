"""APARCH - Asymmetric Power ARCH model (Ding, Granger & Engle, 1993).

sigma^delta_t = omega + alpha * (|eps_{t-1}| - gamma * eps_{t-1})^delta + beta * sigma^delta_{t-1}
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel
from archbox.utils.validation import validate_positive_integer


class APARCH(VolatilityModel):
    """Asymmetric Power ARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of lagged sigma^delta terms (beta). Default 1.
    q : int
        Number of lagged shock terms (alpha, gamma). Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "APARCH"

    def __init__(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        self._innovation_cache: dict[tuple[float, ...], NDArray[np.float64]] = {}
        super().__init__(endog, mean=mean, dist=dist)

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
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
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        var = np.var(self.endog)
        omega = var * 0.01
        alphas = np.full(self.q, 0.05)
        gammas = np.full(self.q, 0.0)
        betas = np.full(self.p, 0.90)
        delta = np.array([2.0])
        return np.concatenate([[omega], alphas, gammas, betas, delta], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["omega"]
        names += [f"alpha[{i + 1}]" for i in range(self.q)]
        names += [f"gamma[{i + 1}]" for i in range(self.q)]
        names += [f"beta[{i + 1}]" for i in range(self.p)]
        names += ["delta"]
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    @property
    def num_params(self) -> int:
        """Number of model parameters: omega + q alphas + q gammas + p betas + delta."""
        return 1 + 2 * self.q + self.p + 1

    # --- Model-level moments and forecasts ---

    #: Monte-Carlo settings (fixed for reproducibility).
    FORECAST_PATHS: int = 10_000
    FORECAST_SEED: int = 20240101
    KAPPA_DRAWS: int = 200_000
    KAPPA_SEED: int = 20240102

    def _aparch_blocks(
        self, var_params: NDArray[np.float64]
    ) -> tuple[float, NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], float]:
        """Split the parameter vector into (omega, alphas, gammas, betas, delta)."""
        params = np.asarray(var_params, dtype=np.float64)
        omega = float(params[0])
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = float(params[1 + 2 * self.q + self.p])
        return omega, alphas, gammas, betas, max(delta, 1e-6)

    def _innovation_sample(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> NDArray[np.float64]:
        """Fixed-seed sample of standardized innovations, cached per shape vector.

        Parameters
        ----------
        dist_params : ndarray, optional
            Fitted distribution shape parameters.

        Returns
        -------
        ndarray
            ``KAPPA_DRAWS`` deterministic draws z_t ~ D(0, 1).
        """
        key: tuple[float, ...] = ()
        if dist_params is not None:
            key = tuple(float(v) for v in np.asarray(dist_params, dtype=np.float64).ravel())
        cached = self._innovation_cache.get(key)
        if cached is None:
            rng = np.random.default_rng(self.KAPPA_SEED)
            cached = self._simulate_innovations(self.KAPPA_DRAWS, rng, dist_params)
            self._innovation_cache[key] = cached
        return cached

    def _kappa(
        self,
        gamma: float,
        delta: float,
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """Compute ``E[(|z| - gamma z)^delta]`` for the fitted innovation law.

        Evaluated by fixed-seed Monte-Carlo over ``KAPPA_DRAWS`` draws, so the
        value is deterministic for a given (gamma, delta, distribution).

        Parameters
        ----------
        gamma : float
            Leverage coefficient, |gamma| < 1.
        delta : float
            Power parameter.
        dist_params : ndarray, optional
            Fitted distribution shape parameters.

        Returns
        -------
        float
            The expectation, a strictly positive finite number.
        """
        z = self._innovation_sample(dist_params)
        base = np.maximum(np.abs(z) - gamma * z, 0.0)
        value = float(np.mean(base**delta))
        return value if np.isfinite(value) else 0.0

    def persistence(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """APARCH persistence ``sum_i alpha_i E[(|z|-gamma_i z)^delta] + sum(beta)``.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha.., gamma.., beta.., delta]``.
        dist_params : ndarray, optional
            Fitted distribution shape parameters used for the expectation.

        Returns
        -------
        float
            Persistence of the sigma^delta recursion.
        """
        _, alphas, gammas, betas, delta = self._aparch_blocks(var_params)
        arch = 0.0
        for i in range(self.q):
            arch += float(alphas[i]) * self._kappa(float(gammas[i]), delta, dist_params)
        return float(arch + np.sum(betas))

    def unconditional_variance(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """Long-run variance ``(omega / (1 - persistence))^(2/delta)``.

        Parameters
        ----------
        var_params : ndarray
            Variance block.
        dist_params : ndarray, optional
            Fitted distribution shape parameters.

        Returns
        -------
        float
            Long-run variance, or ``inf`` when persistence >= 1.
        """
        pers = self.persistence(var_params, dist_params)
        if not np.isfinite(pers) or pers >= 1.0:
            return float("inf")
        omega, _, _, _, delta = self._aparch_blocks(var_params)
        sigma_delta_inf = omega / (1.0 - pers)
        if sigma_delta_inf <= 0.0:
            return float("inf")
        return float(sigma_delta_inf ** (2.0 / delta))

    def forecast_variance(
        self,
        var_params: NDArray[np.float64],
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        horizon: int = 1,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Multi-step APARCH variance forecast by Monte-Carlo simulation.

        APARCH has no closed-form multi-step forecast because the power
        transform ``sigma^delta -> sigma^2`` is non-linear, so the forecast is
        obtained by **Monte-Carlo simulation with a fixed seed**
        (``FORECAST_PATHS`` paths, seed ``FORECAST_SEED``). The one-step value
        is exact: every input is observed, so all paths coincide at h = 1.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha.., gamma.., beta.., delta]``.
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
        omega, alphas, gammas, betas, delta = self._aparch_blocks(var_params)

        sigma2_arr = np.maximum(np.asarray(sigma2, dtype=np.float64).ravel(), 1e-12)
        resid_arr = np.asarray(resids, dtype=np.float64).ravel()
        fill = float(sigma2_arr[-1]) if sigma2_arr.size else self._backcast(self.endog)

        n_paths = int(self.FORECAST_PATHS)
        rng = np.random.default_rng(self.FORECAST_SEED)

        sd_tail = self._tail(sigma2_arr, self.p, fill) ** (delta / 2.0)
        e_tail = self._tail(resid_arr, self.q, 0.0)
        sd_hist = [np.full(n_paths, v, dtype=np.float64) for v in sd_tail]
        e_hist = [np.full(n_paths, v, dtype=np.float64) for v in e_tail]

        out = np.empty(h_max, dtype=np.float64)
        for h in range(h_max):
            sd_next = np.full(n_paths, omega, dtype=np.float64)
            for i in range(self.q):
                e_lag = e_hist[-1 - i]
                shock = np.maximum(np.abs(e_lag) - gammas[i] * e_lag, 0.0)
                sd_next += alphas[i] * shock**delta
            for j in range(self.p):
                sd_next += betas[j] * sd_hist[-1 - j]
            sd_next = np.maximum(sd_next, 1e-300)
            sigma2_next = sd_next ** (2.0 / delta)
            sigma2_next = np.where(np.isfinite(sigma2_next), sigma2_next, 1e-12)
            out[h] = max(float(np.mean(sigma2_next)), 1e-12)
            sd_hist.append(sd_next)
            z_new = self._simulate_innovations(n_paths, rng, dist_params)
            e_hist.append(z_new * np.sqrt(np.maximum(sigma2_next, 1e-12)))
        return out
