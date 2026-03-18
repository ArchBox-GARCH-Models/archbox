"""APARCH - Asymmetric Power ARCH model (Ding, Granger & Engle, 1993).

sigma^delta_t = omega + alpha * (|eps_{t-1}| - gamma * eps_{t-1})^delta + beta * sigma^delta_{t-1}
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel


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
        self.p = p
        self.q = q
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
        return np.concatenate([[omega], alphas, gammas, betas, delta])

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
