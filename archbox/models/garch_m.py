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
        self.p = p
        self.q = q
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
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

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
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

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

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
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

        return self.dist.loglikelihood(adj_resids, sigma2)

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
        return np.concatenate([[omega], alphas, betas, lam])

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
