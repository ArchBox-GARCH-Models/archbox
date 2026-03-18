"""CCC-GARCH: Constant Conditional Correlation model (Bollerslev, 1990).

H_t = D_t * R * D_t

Where R is constant, estimated as sample correlation of standardized residuals.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults


class CCC(MultivariateVolatilityModel):
    """Constant Conditional Correlation GARCH model.

    The CCC model assumes that the conditional correlation matrix R is constant
    over time. It is estimated as the sample correlation of standardized residuals
    from univariate GARCH models.

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
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
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

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

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

    def fit(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

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

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}
