"""GARCH-M - GARCH in Mean model (Engle, Lilien & Robins, 1987).

r_t = mu + lambda * f(sigma^2_t) + eps_t
sigma^2_t = omega + alpha * eps^2_{t-1} + beta * sigma^2_{t-1}

The volatility (or variance) enters the mean equation as a risk premium.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel
from archbox.utils.validation import validate_positive_integer


class GARCHM(VolatilityModel):
    """GARCH-in-Mean model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of GARCH lags (beta). Default 1.
    q : int
        Number of ARCH lags (alpha). Default 1.
    risk_premium : str
        Form of the risk premium in the mean equation.
        'variance' (default): f(sigma^2) = sigma^2
        'volatility': f(sigma^2) = sigma
        'log_variance': f(sigma^2) = log(sigma^2)
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "GARCH-M"

    def __init__(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def _risk_premium_function(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "volatility":
            return float(np.sqrt(max(sigma2, 1e-12)))
        if self.risk_premium == "log_variance":
            return float(np.log(max(sigma2, 1e-12)))
        return float(sigma2)

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def _garchm_blocks(
        self, params: NDArray[np.float64]
    ) -> tuple[float, NDArray[np.float64], NDArray[np.float64], float]:
        """Split the variance block into ``(omega, alphas, betas, lambda)``.

        Only the leading ``num_params`` entries are read, so the full
        ``[variance block, distribution block]`` vector may be passed: the
        in-mean coefficient is ``params[num_params - 1]``, never ``params[-1]``
        (which is a distribution shape parameter when ``dist != 'normal'``).

        Parameters
        ----------
        params : ndarray
            Full or variance-only parameter vector.

        Returns
        -------
        tuple
            ``(omega, alphas, betas, lambda)``.
        """
        block = np.asarray(params, dtype=np.float64)[: self.num_params]
        omega = float(block[0])
        alphas = block[1 : 1 + self.q]
        betas = block[1 + self.q : 1 + self.q + self.p]
        lam = float(block[1 + self.q + self.p])
        return omega, alphas, betas, lam

    def _garchm_joint_recursion(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega, alphas, betas, lam = self._garchm_blocks(params)

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def loglike(self, params: NDArray[np.float64], backcast: float | None = None) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses the joint forward pass where ``eps_t = r_t - lambda f(sigma2_t)``.
        ``params`` is the combined vector ``[omega, alpha.., beta.., lambda]``
        followed by the distribution shape parameters, which are forwarded to
        the conditional distribution.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        dist_params = np.asarray(params, dtype=np.float64)[self.num_params :]
        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2, dist_params)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def loglike_per_obs(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        dist_params = np.asarray(params, dtype=np.float64)[self.num_params :]
        return self.dist.loglikelihood(adj_resids, sigma2, dist_params)

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: [omega, alpha_1..q, beta_1..p, lambda]."""
        var = np.var(self.endog)
        omega = var * 0.01
        alphas = np.full(self.q, 0.05)
        betas = np.full(self.p, 0.90)
        lam = np.array([0.01])
        return np.concatenate([[omega], alphas, betas, lam], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["omega"]
        names += [f"alpha[{i + 1}]" for i in range(self.q)]
        names += [f"beta[{i + 1}]" for i in range(self.p)]
        names += ["lambda"]
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    @property
    def num_params(self) -> int:
        """Number of parameters: omega + q alphas + p betas + lambda."""
        return 1 + self.q + self.p + 1

    # --- Simulation ---

    def _simulate_mean_offset(
        self,
        var_params: NDArray[np.float64],
        sigma2_t: float,
    ) -> float:
        """Risk premium ``lambda f(sigma^2_t)`` added to the simulated return.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha.., beta.., lambda]``.
        sigma2_t : float
            Conditional variance at date ``t``.

        Returns
        -------
        float
            The in-mean contribution to r_t.
        """
        _, _, _, lam = self._garchm_blocks(var_params)
        return lam * self._risk_premium_function(sigma2_t)

    # --- Model-level moments and forecasts ---

    def _arch_garch_blocks(
        self, var_params: NDArray[np.float64]
    ) -> tuple[float, NDArray[np.float64], NDArray[np.float64]]:
        """Split ``[omega, alpha.., beta.., lambda]`` into (omega, alphas, betas).

        The in-mean coefficient ``lambda`` belongs to the mean equation, not to
        the variance dynamics, so it is excluded here. As a consequence the
        inherited ``persistence`` and ``unconditional_variance`` are the plain
        GARCH ones.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha.., beta.., lambda]``.

        Returns
        -------
        tuple
            ``(omega, alphas, betas)``.
        """
        params = np.asarray(var_params, dtype=np.float64)
        omega = float(params[0])
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        return omega, alphas, betas

    def conditional_variance(
        self,
        params: NDArray[np.float64],
        backcast: float | None = None,
    ) -> NDArray[np.float64]:
        """Conditional variance path from the GARCH-M joint forward pass.

        In GARCH-M ``eps_t = r_t - lambda f(sigma^2_t)`` while ``sigma^2_t``
        depends on ``eps_{t-1}``, so the variance path used by the likelihood
        comes from the joint recursion, not from ``_variance_recursion`` on the
        raw returns.

        Parameters
        ----------
        params : ndarray
            Full or variance-only parameter vector.
        backcast : float, optional
            Initial variance. Computed from the data when omitted.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        var_params = np.asarray(params, dtype=np.float64)[: self.num_params]
        sigma2, _ = self._garchm_joint_recursion(var_params, float(backcast))
        return np.maximum(sigma2, 1e-12)

    def forecast_variance(
        self,
        var_params: NDArray[np.float64],
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        horizon: int = 1,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Analytic GARCH-M variance forecast.

        The variance dynamics are plain GARCH(p, q); the only difference is
        that the shocks feeding the recursion are the *adjusted* residuals
        ``eps_t = r_t - lambda f(sigma^2_t)`` rather than the raw returns.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha.., beta.., lambda]``.
        resids : ndarray
            In-sample residuals (raw returns); replaced internally by the
            adjusted GARCH-M residuals.
        sigma2 : ndarray
            In-sample conditional variance path.
        horizon : int
            Number of steps ahead (>= 1).
        dist_params : ndarray, optional
            Unused.

        Returns
        -------
        ndarray
            Forecast variances, shape ``(horizon,)``.
        """
        del resids
        params = np.asarray(var_params, dtype=np.float64)
        backcast = self._backcast(self.endog)
        joint_sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2_arr = np.asarray(sigma2, dtype=np.float64).ravel()
        if sigma2_arr.size != joint_sigma2.size:
            sigma2_arr = joint_sigma2
        return super().forecast_variance(params, adj_resids, sigma2_arr, horizon, dist_params)
