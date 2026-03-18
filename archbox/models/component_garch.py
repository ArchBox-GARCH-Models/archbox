"""Component GARCH model (Engle & Lee, 1999).

sigma^2_t = q_t + h_t

q_t = omega + beta_p * (q_{t-1} - omega) + alpha_p * (eps^2_{t-1} - sigma^2_{t-1})
h_t = alpha * (eps^2_{t-1} - q_{t-1}) + beta * h_{t-1}

Decomposes variance into permanent (q_t) and transitory (h_t) components.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel


class ComponentGARCH(VolatilityModel):
    """Component GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "Component GARCH"

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=mean, dist=dist)

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def variance_decomposition(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: [omega, alpha, beta, alpha_p, beta_p]."""
        var = np.var(self.endog)
        return np.array([var, 0.05, 0.10, 0.04, 0.98])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        return ["omega", "alpha", "beta", "alpha_p", "beta_p"]

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.0, np.inf),  # alpha >= 0
            (0.0, np.inf),  # beta >= 0
            (0.0, np.inf),  # alpha_p >= 0
            (0.001, 0.999),  # 0 < beta_p < 1
        ]

    @property
    def num_params(self) -> int:
        """Number of parameters: omega, alpha, beta, alpha_p, beta_p."""
        return 5
