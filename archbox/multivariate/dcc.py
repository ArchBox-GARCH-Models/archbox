"""DCC-GARCH: Dynamic Conditional Correlation model (Engle, 2002).

H_t = D_t * R_t * D_t

Where R_t evolves dynamically:
    Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
    R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults


class DCC(MultivariateVolatilityModel):
    """Dynamic Conditional Correlation GARCH model.

    The DCC model extends CCC by allowing the conditional correlation matrix
    to vary over time, governed by two parameters (a, b).

    Parameters
    ----------
    endog : ndarray
        Array of shape (T, k) with k return series.
    univariate_model : str
        Univariate GARCH variant. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for univariate GARCH. Default (1, 1).

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
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

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
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

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

    def _estimate_correlation(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}
