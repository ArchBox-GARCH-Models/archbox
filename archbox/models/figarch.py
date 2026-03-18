"""FIGARCH - Fractionally Integrated GARCH (Baillie, Bollerslev & Mikkelsen, 1996).

(1 - beta(L)) * sigma^2_t = omega + [1 - beta(L) - phi(L)(1-L)^d] * eps^2_t

Long memory in variance with fractional differencing parameter d.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel


def _fractional_coefficients(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


class FIGARCH(VolatilityModel):
    """Fractionally Integrated GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    truncation_lag : int
        Number of lags for the truncated fractional expansion. Default 1000.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "FIGARCH"

    def __init__(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=dist)

    def _compute_lambda_coefficients(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: [omega, phi, d, beta]."""
        var = np.var(self.endog)
        omega = var * 0.01
        phi = 0.2
        d = 0.4
        beta = 0.3
        return np.array([omega, phi, d, beta])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        return ["omega", "phi", "d", "beta"]

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    @property
    def num_params(self) -> int:
        """Number of parameters: omega, phi, d, beta."""
        return 4
