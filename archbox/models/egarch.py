"""EGARCH - Exponential GARCH model (Nelson, 1991).

log(sigma^2_t) = omega + alpha * |z_{t-1}| + gamma * z_{t-1} + beta * log(sigma^2_{t-1})

onde z_t = eps_t / sigma_t (residuo padronizado).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel


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
        self.p = p
        self.q = q
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
