"""DCC-GARCH: Dynamic Conditional Correlation model (Engle, 2002).

H_t = D_t * R_t * D_t

Where R_t evolves dynamically:
    Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
    R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel
from archbox.multivariate.results import MultivarResults
from archbox.multivariate.utils import corr_to_cov, cov_to_corr


def normalize_q(q_mat: NDArray[np.float64]) -> NDArray[np.float64]:
    """Normalize a Q matrix (or a stack of them) to a correlation matrix.

    Parameters
    ----------
    q_mat : ndarray
        Q matrix (k, k) or a stack (T, k, k).

    Returns
    -------
    ndarray
        R = diag(Q)^{-1/2} Q diag(Q)^{-1/2}, same shape as ``q_mat``.
    """
    return cov_to_corr(q_mat)


class DCC(MultivariateVolatilityModel):
    """Dynamic Conditional Correlation GARCH model.

    The DCC model extends CCC by allowing the conditional correlation matrix
    to vary over time, governed by two parameters (a, b).

    Parameters
    ----------
    endog : array-like
        Array or DataFrame of shape (T, k) with k return series.
    univariate_model : str or type or callable
        Univariate volatility model for each series. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for the univariate model. Default (1, 1).
    univariate_dist : str
        Conditional distribution of the univariate models. Default 'normal'.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.multivariate.dcc import DCC
    >>> returns = np.random.randn(500, 3) * 0.01
    >>> model = DCC(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    Engle, R.F. (2002). Dynamic Conditional Correlation: A Simple Class of
    Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models.
    Journal of Business & Economic Statistics, 20(3), 339-350.
    """

    model_name: str = "DCC-GARCH"

    def __init__(
        self,
        endog: Any,
        univariate_model: str | type | Callable[..., Any] = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
        univariate_dist: str = "normal",
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order, univariate_dist)
        self._Q_bar: NDArray[np.float64] | None = None
        self._Q_path: NDArray[np.float64] | None = None

    # --- Recursion ---

    def q_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Run the DCC Q recursion and return the *full* Q path.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}, with Q_0 = Q_bar.

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        tuple[ndarray, ndarray]
            ``(q_path, q_bar)`` with ``q_path`` of shape (T, k, k).
        """
        a, b = float(params[0]), float(params[1])
        n_obs, k = std_resids.shape

        q_bar = std_resids.T @ std_resids / n_obs

        q_mat = np.empty((n_obs, k, k))
        q_mat[0] = q_bar

        # Outer products z_t z_t' for every t, computed once.
        outer = std_resids[:, :, None] * std_resids[:, None, :]
        const = (1.0 - a - b) * q_bar

        q_prev = q_mat[0]
        for t in range(1, n_obs):
            q_prev = const + a * outer[t - 1] + b * q_prev
            q_mat[t] = q_prev

        return q_mat, q_bar

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via the DCC recursion.

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        q_mat, q_bar = self.q_recursion(params, std_resids)
        self._Q_bar = q_bar
        self._Q_path = q_mat
        return normalize_q(q_mat)

    def _results_extras(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> dict[str, Any]:
        """Store the Q path so the forecast does not depend on model state."""
        q_path, q_bar = self.q_recursion(params, std_resids)
        return {
            "q_path": q_path,
            "q_bar": q_bar,
            "q_last": q_path[-1].copy(),
            "z_last": np.asarray(std_resids[-1], dtype=np.float64).copy(),
        }

    # --- Parameters ---

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: a=0.05, b=0.90."""
        return np.array([0.05, 0.90])

    @property
    def param_names(self) -> list[str]:
        """DCC parameter names."""
        return ["a", "b"]

    def _param_bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1e-6, 0.9999)]

    def _constraints(self) -> list[dict[str, Any]]:
        """Stationarity constraint a + b < 1."""
        return [{"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]}]

    def _starting_points(self) -> list[NDArray[np.float64]]:
        """Several starting points, so the optimizer does not stall in a corner."""
        return [
            self.start_params,
            np.array([1e-6, 1e-6]),  # near CCC (a ~ 0, b ~ 0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
            np.array([0.03, 0.60]),
        ]

    def _second_step_neg_loglike(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> float:
        """Negative DCC correlation log-likelihood (infeasible -> ``inf``)."""
        a, b = float(params[0]), float(params[1])
        if a <= 0.0 or b <= 0.0 or a + b >= 0.9999:
            return float(np.inf)
        return super()._second_step_neg_loglike(params, std_resids)

    # --- Forecast ---

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        The one-step forecast applies the in-sample recursion one step ahead,

            Q_{T+1} = (1 - a - b) Q_bar + a z_T z_T' + b Q_T,

        and for h > 1 uses the standard approximation

            Q_{T+h} = (1 - a - b) Q_bar + (a + b) Q_{T+h-1}.

        Variances come from each univariate ``ArchResults.forecast(horizon)``.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' and 'correlation' forecasts.
        """
        if horizon < 1:
            msg = f"horizon must be >= 1, got {horizon}"
            raise ValueError(msg)

        a, b = float(results.params[0]), float(results.params[1])
        extras = results.extras
        q_bar = np.asarray(extras["q_bar"], dtype=np.float64)
        q_prev = np.asarray(extras["q_last"], dtype=np.float64)
        z_last = np.asarray(extras["z_last"], dtype=np.float64)

        k = q_bar.shape[0]
        const = (1.0 - a - b) * q_bar
        r_forecast = np.zeros((horizon, k, k))

        for h in range(horizon):
            if h == 0:
                q_prev = const + a * np.outer(z_last, z_last) + b * q_prev
            else:
                q_prev = const + (a + b) * q_prev
            r_forecast[h] = normalize_q(q_prev)

        vol = self._univariate_volatility_forecast(results, horizon)
        h_forecast = corr_to_cov(r_forecast, vol)

        return {"covariance": h_forecast, "correlation": r_forecast}
