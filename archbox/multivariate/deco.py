"""DECO: Dynamic Equicorrelation model (Engle & Kelly, 2012).

R_t = (1 - rho_t) * I_k + rho_t * J_k

Where rho_t is the average off-diagonal element of the DCC-like Q_t.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel
from archbox.multivariate.dcc import normalize_q
from archbox.multivariate.results import MultivarResults
from archbox.multivariate.utils import corr_to_cov


def equicorrelation_matrices(
    rho_t: NDArray[np.float64],
    k: int,
) -> NDArray[np.float64]:
    """Build the stack of equicorrelation matrices R_t = (1-rho_t) I + rho_t J.

    Parameters
    ----------
    rho_t : ndarray
        Equicorrelation series (T,).
    k : int
        Number of series.

    Returns
    -------
    ndarray
        Equicorrelation matrices, shape (T, k, k).
    """
    rho = np.asarray(rho_t, dtype=np.float64)
    eye = np.eye(k)
    ones = np.ones((k, k))
    return (1.0 - rho)[:, None, None] * eye + rho[:, None, None] * ones


def equicorrelation_loglike(
    rho_t: NDArray[np.float64],
    std_resids: NDArray[np.float64],
) -> float:
    """Correlation log-likelihood for equicorrelated R_t, in closed form.

    For R = (1-rho) I + rho J,

        log|R| = (k-1) log(1-rho) + log(1 + (k-1) rho)
        z' R^{-1} z = [z'z - rho (1'z)^2 / (1 + (k-1) rho)] / (1 - rho)

    which avoids a (T, k, k) determinant/solve and lets DECO scale to large k.

    Parameters
    ----------
    rho_t : ndarray
        Equicorrelation series (T,).
    std_resids : ndarray
        Standardized residuals (T, k).

    Returns
    -------
    float
        ``-0.5 * sum_t [log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t]``, or ``-inf``
        if any rho_t leaves the valid interval (-1/(k-1), 1).
    """
    rho = np.asarray(rho_t, dtype=np.float64)
    k = std_resids.shape[1]
    denom = 1.0 + (k - 1) * rho
    if np.any(rho >= 1.0) or np.any(denom <= 0.0):
        return -np.inf

    logdet = (k - 1) * np.log1p(-rho) + np.log(denom)
    quad_i = np.einsum("tk,tk->t", std_resids, std_resids)
    row_sum = np.sum(std_resids, axis=1)
    quad_r = (quad_i - rho * row_sum**2 / denom) / (1.0 - rho)
    total = float(np.sum(logdet + quad_r - quad_i))
    if not np.isfinite(total):
        return -np.inf
    return -0.5 * total


class DECO(MultivariateVolatilityModel):
    """Dynamic Equicorrelation model.

    DECO simplifies DCC by assuming a single scalar equicorrelation rho_t
    for all pairs. This allows scaling to very large k (hundreds of assets).

    R_t = (1 - rho_t) * I_k + rho_t * J_k

    Where:
    - J_k = 1_k * 1_k' (matrix of ones)
    - rho_t = mean off-diagonal of the normalized Q_t from DCC dynamics

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
        univariate_model: str | type | Callable[..., Any] = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
        univariate_dist: str = "normal",
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, univariate_order, univariate_dist)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    # --- Recursion ---

    def _rho_bounds(self) -> tuple[float, float]:
        """Valid open interval for the equicorrelation given k."""
        return (-1.0 / (self.k - 1) + 1e-6, 1.0 - 1e-6)

    def rho_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Run the DCC-style Q recursion and reduce it to a scalar rho_t.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            ``(rho_t, q_path, q_bar)``.
        """
        a, b = float(params[0]), float(params[1])
        n_obs, k = std_resids.shape

        q_bar = std_resids.T @ std_resids / n_obs
        q_mat = np.empty((n_obs, k, k))
        q_mat[0] = q_bar

        outer = std_resids[:, :, None] * std_resids[:, None, :]
        const = (1.0 - a - b) * q_bar

        q_prev = q_mat[0]
        for t in range(1, n_obs):
            q_prev = const + a * outer[t - 1] + b * q_prev
            q_mat[t] = q_prev

        r_dcc = normalize_q(q_mat)
        rho_t = (np.sum(r_dcc, axis=(1, 2)) - k) / (k * (k - 1))
        low, high = self._rho_bounds()
        rho_t = np.clip(rho_t, low, high)

        return rho_t, q_mat, q_bar

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same role as the DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        rho_t, _q_path, q_bar = self.rho_recursion(params, std_resids)
        self._q_bar = q_bar
        self._rho_t = rho_t
        return equicorrelation_matrices(rho_t, std_resids.shape[1])

    def _results_extras(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> dict[str, Any]:
        """Store the rho path and Q state so forecasting is state-free."""
        rho_t, q_path, q_bar = self.rho_recursion(params, std_resids)
        return {
            "rho_t": rho_t,
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
        """DECO parameter names."""
        return ["a", "b"]

    def _param_bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1e-6, 0.9999)]

    def _constraints(self) -> list[dict[str, Any]]:
        """Stationarity constraint a + b < 1."""
        return [{"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]}]

    def _starting_points(self) -> list[NDArray[np.float64]]:
        """Multi-start grid, mirroring DCC.

        A single start at (0.05, 0.90) leaves the SLSQP run stuck against the
        a + b < 1 face on many samples; the extra starts recover the interior
        optimum (and confirm a corner solution when the data really has a
        constant correlation).
        """
        return [
            self.start_params,
            np.array([1e-6, 1e-6]),
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
        """Negative DECO log-likelihood using the closed-form equicorrelation."""
        a, b = float(params[0]), float(params[1])
        if a <= 0.0 or b <= 0.0 or a + b >= 0.9999:
            return float(np.inf)
        rho_t, _q_path, _q_bar = self.rho_recursion(params, std_resids)
        ll = equicorrelation_loglike(rho_t, std_resids)
        if not np.isfinite(ll):
            return float(np.inf)
        return -ll

    @property
    def equicorrelation(self) -> NDArray[np.float64] | None:
        """Return the time-varying equicorrelation rho_t."""
        return self._rho_t

    # --- Forecast ---

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

        The Q recursion is projected exactly as in DCC -- one true step ahead
        for h = 1 (using z_T z_T' and Q_T) and the mean-reverting approximation
        afterwards -- and each Q_{T+h} is reduced to a scalar rho_{T+h}.
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
        low, high = self._rho_bounds()

        rho_forecast = np.zeros(horizon)
        for h in range(horizon):
            if h == 0:
                q_prev = const + a * np.outer(z_last, z_last) + b * q_prev
            else:
                q_prev = const + (a + b) * q_prev
            r_dcc = normalize_q(q_prev)
            rho = (float(np.sum(r_dcc)) - k) / (k * (k - 1))
            rho_forecast[h] = np.clip(rho, low, high)

        r_forecast = equicorrelation_matrices(rho_forecast, k)
        vol = self._univariate_volatility_forecast(results, horizon)
        h_forecast = corr_to_cov(r_forecast, vol)

        return {"covariance": h_forecast, "correlation": r_forecast}
