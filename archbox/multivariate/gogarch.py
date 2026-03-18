"""GO-GARCH: Generalized Orthogonal GARCH (van der Weide, 2002).

eps_t = Z * f_t
f_{i,t} ~ GARCH(1,1) (independent factors)
H_t = Z * diag(h_{1,t}, ..., h_{k,t}) * Z'
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults


class GOGARCH(MultivariateVolatilityModel):
    """Generalized Orthogonal GARCH model.

    GO-GARCH uses ICA to find independent factors, then fits univariate
    GARCH on each factor. The covariance is reconstructed as:
        H_t = Z * diag(h_{1,t}, ..., h_{k,t}) * Z'

    Parameters
    ----------
    endog : ndarray
        Array of shape (T, k) with k return series.
    n_components : int or None
        Number of ICA components. Default None (= k).
    univariate_model : str
        Univariate GARCH variant for factors. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for univariate GARCH. Default (1, 1).

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.multivariate.gogarch import GOGARCH
    >>> returns = np.random.randn(500, 3) * 0.01
    >>> model = GOGARCH(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    van der Weide, R. (2002). GO-GARCH: A Multivariate Generalized Orthogonal
    GARCH Model. Journal of Applied Econometrics, 17(5), 549-564.
    """

    model_name: str = "GO-GARCH"

    def __init__(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

        Parameters
        ----------
        params : ndarray
            Empty (no correlation params for GO-GARCH).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Identity correlation matrices, shape (T, k, k).
        """
        n_obs, k = std_resids.shape
        r_mat = np.zeros((n_obs, k, k))
        for t in range(n_obs):
            r_mat[t] = np.eye(k)
        return r_mat

    @property
    def start_params(self) -> NDArray[np.float64]:
        """No separate correlation parameters for GO-GARCH."""
        return np.array([], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """No correlation parameter names."""
        return []

    def fit(self, method: str = "two_step", disp: bool = True) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    @property
    def mixing_matrix(self) -> NDArray[np.float64] | None:
        """Return the ICA mixing matrix Z."""
        return self._mixing_matrix

    @property
    def factors(self) -> NDArray[np.float64] | None:
        """Return the independent factors."""
        return self._factors

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}
