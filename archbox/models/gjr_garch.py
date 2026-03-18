"""GJR-GARCH model (Glosten, Jagannathan & Runkle, 1993).

sigma^2_t = omega + (alpha + gamma * I_{t-1}) * eps^2_{t-1} + beta * sigma^2_{t-1}

I_{t-1} = 1 se eps_{t-1} < 0, 0 caso contrario.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel


class GJRGARCH(VolatilityModel):
    """GJR-GARCH (Threshold GARCH) model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of GARCH lags (beta). Default 1.
    q : int
        Number of ARCH lags (alpha, gamma). Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "GJR-GARCH"

    def __init__(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        var = np.var(self.endog)
        omega = var * 0.01
        alphas = np.full(self.q, 0.05)
        gammas = np.full(self.q, 0.04)
        betas = np.full(self.p, 0.90)
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

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    @property
    def num_params(self) -> int:
        """Number of model parameters."""
        return 1 + 2 * self.q + self.p
