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
from archbox.utils.validation import validate_positive_integer


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

    # --- Simulation ---

    def _simulate_state(
        self,
        var_params: NDArray[np.float64],
        backcast: float,
    ) -> dict[str, Any]:
        """Carry the permanent/transitory split across simulation steps."""
        del var_params
        return {"q": float(backcast), "h": 0.0}

    def _simulate_next_variance(
        self,
        var_params: NDArray[np.float64],
        eps: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        t: int,
        backcast: float,
        state: dict[str, Any],
    ) -> float:
        """One Component-GARCH simulation step (same recursion as the filter)."""
        del backcast
        params = np.asarray(var_params, dtype=np.float64)
        omega = float(params[0])
        alpha = float(params[1])
        beta = float(params[2])
        alpha_p = float(params[3])
        beta_p = float(params[4])

        eps2 = float(eps[t - 1]) ** 2
        q_prev = float(state["q"])
        h_prev = float(state["h"])
        sigma2_prev = float(sigma2[t - 1])

        q_next = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        q_next = max(q_next, 1e-12)
        h_next = alpha * (eps2 - q_prev) + beta * h_prev
        state["q"] = q_next
        state["h"] = h_next
        return max(q_next + h_next, 1e-12)

    # --- Model-level moments and forecasts ---

    def persistence(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """Dominant persistence of the two-component variance process.

        The permanent component decays at rate ``beta_p`` and the transitory
        component at rate ``alpha + beta``; the slowest of the two governs how
        long a shock is felt, so it is the one reported (and the one that drives
        the half-life).

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha, beta, alpha_p, beta_p]``.
        dist_params : ndarray, optional
            Unused.

        Returns
        -------
        float
            ``max(beta_p, alpha + beta)``.
        """
        del dist_params
        params = np.asarray(var_params, dtype=np.float64)
        transitory = float(params[1]) + float(params[2])
        permanent = float(params[4])
        return float(max(permanent, transitory))

    def unconditional_variance(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """Long-run variance of the Component GARCH model.

        The transitory component has zero mean and the permanent component
        mean-reverts to ``omega``, so ``E[sigma^2_t] = omega``.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha, beta, alpha_p, beta_p]``.
        dist_params : ndarray, optional
            Unused.

        Returns
        -------
        float
            ``omega``, or ``inf`` when either component is non-stationary.
        """
        pers = self.persistence(var_params, dist_params)
        if not np.isfinite(pers) or pers >= 1.0:
            return float("inf")
        omega = float(np.asarray(var_params, dtype=np.float64)[0])
        return float(max(omega, 1e-12))

    def forecast_variance(
        self,
        var_params: NDArray[np.float64],
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        horizon: int = 1,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Analytic Component GARCH forecast on the permanent/transitory split.

        The first step uses the observed shock. For ``h > 1`` the substitution
        ``E[eps^2_{T+k}] = sigma^2_{T+k}`` makes the two components decouple:
        ``q_{T+h} = omega + beta_p (q_{T+h-1} - omega)`` and
        ``h_{T+h} = (alpha + beta) h_{T+h-1}``.

        Parameters
        ----------
        var_params : ndarray
            Variance block ``[omega, alpha, beta, alpha_p, beta_p]``.
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
        alpha = float(params[1])
        beta = float(params[2])
        alpha_p = float(params[3])
        beta_p = float(params[4])

        resid_arr = np.asarray(resids, dtype=np.float64).ravel()
        backcast = self._backcast(resid_arr) if resid_arr.size else self._backcast(self.endog)
        path_sigma2, path_q, path_h = self.variance_decomposition(params, resid_arr, backcast)

        sigma2_arr = np.asarray(sigma2, dtype=np.float64).ravel()
        last_sigma2 = float(sigma2_arr[-1]) if sigma2_arr.size else float(path_sigma2[-1])
        q_prev = float(path_q[-1])
        h_prev = float(path_h[-1])
        eps2 = float(resid_arr[-1] ** 2) if resid_arr.size else last_sigma2

        out = np.empty(h_max, dtype=np.float64)
        for step in range(h_max):
            if step == 0:
                q_next = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - last_sigma2)
                h_next = alpha * (eps2 - q_prev) + beta * h_prev
            else:
                q_next = omega + beta_p * (q_prev - omega)
                h_next = (alpha + beta) * h_prev
            q_next = max(q_next, 1e-12)
            value = max(q_next + h_next, 1e-12)
            out[step] = value
            q_prev, h_prev = q_next, h_next
        return out
