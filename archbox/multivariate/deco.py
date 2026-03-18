"""DECO: Dynamic Equicorrelation model (Engle & Kelly, 2012).

R_t = (1 - rho_t) * I_k + rho_t * J_k

Where rho_t is the average off-diagonal element of the DCC-like Q_t.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults


class DECO(MultivariateVolatilityModel):
    """Dynamic Equicorrelation model.

    DECO simplifies DCC by assuming a single scalar equicorrelation rho_t
    for all pairs. This allows scaling to very large k (hundreds of assets).

    R_t = (1 - rho_t) * I_k + rho_t * J_k

    Where:
    - J_k = 1_k * 1_k' (matrix of ones)
    - rho_t = mean off-diagonal of normalized Q_t from DCC dynamics

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
    >>> from archbox.multivariate.deco import DECO
    >>> returns = np.random.randn(500, 10) * 0.01
    >>> model = DECO(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    Engle, R.F. & Kelly, B.T. (2012). Dynamic Equicorrelation.
    Journal of Business & Economic Statistics, 30(2), 212-228.
    """

    model_name: str = "DECO"

    def __init__(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: a=0.05, b=0.90."""
        return np.array([0.05, 0.90])

    @property
    def param_names(self) -> list[str]:
        """DECO parameter names."""
        return ["a", "b"]

    def _param_bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1e-6, 0.9999)]

    def _estimate_correlation(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

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

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

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

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    @property
    def equicorrelation(self) -> NDArray[np.float64] | None:
        """Return the time-varying equicorrelation rho_t."""
        return self._rho_t

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}
