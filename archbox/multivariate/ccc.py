"""CCC-GARCH: Constant Conditional Correlation model (Bollerslev, 1990).

H_t = D_t * R * D_t

Where R is constant, estimated as sample correlation of standardized residuals.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel
from archbox.multivariate.results import MultivarResults
from archbox.multivariate.utils import (
    corr_to_cov,
    cov_to_corr,
    ensure_positive_definite,
)


class CCC(MultivariateVolatilityModel):
    """Constant Conditional Correlation GARCH model.

    The CCC model assumes that the conditional correlation matrix R is constant
    over time. It is estimated as the sample correlation of standardized residuals
    from univariate GARCH models.

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
    >>> from archbox.multivariate.ccc import CCC
    >>> returns = np.random.randn(500, 3) * 0.01
    >>> model = CCC(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    Bollerslev, T. (1990). Modelling the Coherence in Short-Run Nominal Exchange Rates:
    A Multivariate Generalized ARCH Model. Review of Economics and Statistics, 72(3), 498-505.
    """

    model_name: str = "CCC-GARCH"

    def __init__(
        self,
        endog: Any,
        univariate_model: str | type | Callable[..., Any] = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
        univariate_dist: str = "normal",
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order, univariate_dist)
        self._R: NDArray[np.float64] | None = None

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        corr = np.asarray(np.corrcoef(std_resids.T), dtype=np.float64)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            corr = cov_to_corr(ensure_positive_definite(corr))

        self._R = corr

        return np.broadcast_to(corr, (n_obs, k, k)).copy()

    @property
    def start_params(self) -> NDArray[np.float64]:
        """No parameters to estimate for CCC."""
        return np.array([], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """No parameter names for CCC."""
        return []

    def _param_bounds(self) -> list[tuple[float, float]]:
        """No bounds for CCC (no parameters)."""
        return []

    def _results_extras(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> dict[str, Any]:
        """Store the estimated constant correlation on the results object."""
        return {"constant_correlation": self._correlation_recursion(params, std_resids)[0]}

    @property
    def constant_correlation(self) -> NDArray[np.float64] | None:
        """Return the estimated constant correlation matrix R."""
        return self._R

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        The correlation forecast is the constant R; the variance forecasts come
        from each univariate ``ArchResults.forecast(horizon)``.

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

        corr = np.asarray(
            results.extras.get("constant_correlation", results.dynamic_correlation[-1]),
            dtype=np.float64,
        )
        corr_forecast = np.tile(corr, (horizon, 1, 1))
        vol = self._univariate_volatility_forecast(results, horizon)
        cov_forecast = corr_to_cov(corr_forecast, vol)

        return {"covariance": cov_forecast, "correlation": corr_forecast}
