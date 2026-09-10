"""FIGARCH - Fractionally Integrated GARCH (Baillie, Bollerslev & Mikkelsen, 1996).

(1 - beta(L)) * sigma^2_t = omega + [1 - beta(L) - phi(L)(1-L)^d] * eps^2_t

Long memory in variance with fractional differencing parameter d.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel
from archbox.utils.validation import validate_positive_integer


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
        self.truncation_lag = validate_positive_integer(truncation_lag, "truncation_lag")
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

    # --- Simulation ---

    def _simulate_state(
        self,
        var_params: NDArray[np.float64],
        backcast: float,
    ) -> dict[str, Any]:
        """Cache the truncated ARCH(infinity) weights used by every step."""
        del backcast
        params = np.asarray(var_params, dtype=np.float64)
        phi = float(params[1])
        d = float(params[2])
        beta = float(params[3])
        omega = float(params[0])
        n_lags = max(int(self.truncation_lag), 1)
        return {
            "lam": self._compute_lambda_coefficients(phi, d, beta, n_lags),
            "omega_star": omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega,
            "n_lags": n_lags,
        }

    def _simulate_next_variance(
        self,
        var_params: NDArray[np.float64],
        eps: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        t: int,
        backcast: float,
        state: dict[str, Any],
    ) -> float:
        """One FIGARCH simulation step via the truncated lambda weights."""
        del var_params, sigma2, backcast
        lam: NDArray[np.float64] = state["lam"]
        n_lags = int(state["n_lags"])
        n_used = min(t, n_lags)
        if n_used == 0:
            return max(float(state["omega_star"]), 1e-12)
        past = eps[t - n_used : t][::-1] ** 2
        value = float(state["omega_star"]) + float(np.dot(lam[:n_used], past))
        return max(value, 1e-12)

    # --- Model-level moments and forecasts ---

    def persistence(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """FIGARCH persistence is 1: the ARCH(inf) weights sum to one.

        For ``0 < d < 1`` the lambda weights of the ARCH(infinity)
        representation sum to exactly one, so shocks to the variance decay
        hyperbolically but never die out. The speed of that hyperbolic decay is
        governed by ``d``, not by a geometric persistence coefficient.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, phi, d, beta]`` (unused).
        dist_params : ndarray, optional
            Unused.

        Returns
        -------
        float
            Always ``1.0``.
        """
        del var_params, dist_params
        return 1.0

    def unconditional_variance(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """FIGARCH is not covariance stationary, so the long-run variance is infinite.

        Parameters
        ----------
        var_params : ndarray
            Variance block (unused).
        dist_params : ndarray, optional
            Unused.

        Returns
        -------
        float
            Always ``inf``.
        """
        del var_params, dist_params
        return float("inf")

    def forecast_variance(
        self,
        var_params: NDArray[np.float64],
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        horizon: int = 1,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Analytic FIGARCH forecast via the truncated ARCH(infinity) weights.

        ``sigma^2_{T+h} = omega/(1-beta) + sum_{k=1}^{K} lambda_k E[eps^2_{T+h-k}]``
        with ``E[eps^2_s] = eps^2_s`` for observed dates and
        ``E[eps^2_s] = sigma^2_s`` for forecast dates.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, phi, d, beta]``.
        resids : ndarray
            In-sample residuals.
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
        del dist_params
        h_max = validate_positive_integer(horizon, "horizon")
        params = np.asarray(var_params, dtype=np.float64)
        omega = float(params[0])
        phi = float(params[1])
        d = float(params[2])
        beta = float(params[3])

        resid_arr = np.asarray(resids, dtype=np.float64).ravel()
        sigma2_arr = np.maximum(np.asarray(sigma2, dtype=np.float64).ravel(), 1e-12)
        n_lags = max(min(self.truncation_lag, len(resid_arr)), 1)
        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        fill = float(sigma2_arr[-1]) if sigma2_arr.size else self._backcast(self.endog)

        # History of E[eps^2], oldest first; forecasts are appended as they are made.
        eps2_hist = list(self._tail(resid_arr**2, n_lags, fill))

        out = np.empty(h_max, dtype=np.float64)
        for h in range(h_max):
            recent = np.asarray(eps2_hist[-n_lags:], dtype=np.float64)[::-1]
            value = omega_star + float(np.dot(lam, recent))
            value = max(value, 1e-12)
            out[h] = value
            eps2_hist.append(value)
        return out
