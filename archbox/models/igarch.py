"""IGARCH - Integrated GARCH model (Engle & Bollerslev, 1986).

sigma^2_t = omega + alpha * eps^2_{t-1} + (1 - alpha) * sigma^2_{t-1}

Persistencia = 1 (alpha + beta = 1, beta = 1 - alpha).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel


class IGARCH(VolatilityModel):
    """Integrated GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.

    Notes
    -----
    IGARCH(1,1) has persistence = 1 (alpha + beta = 1).
    beta = 1 - alpha is enforced internally.
    The unconditional variance does not exist (infinite),
    but forecasts are still finite.
    """

    volatility_process = "IGARCH"

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
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
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        var = np.var(self.endog)
        omega = var * 0.005
        alpha = 0.05
        return np.array([omega, alpha])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        return ["omega", "alpha"]

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.001, 0.999),  # 0 < alpha < 1
        ]

    @property
    def num_params(self) -> int:
        """Number of model parameters (omega, alpha). beta = 1-alpha is implicit."""
        return 2
