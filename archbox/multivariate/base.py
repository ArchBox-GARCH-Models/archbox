"""Base class for multivariate volatility models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

if TYPE_CHECKING:
    pass


class MultivariateVolatilityModel(ABC):
    """Abstract base class for multivariate GARCH models.

    All multivariate models (DCC, CCC, BEKK, GO-GARCH, DECO) inherit from this class.

    Parameters
    ----------
    endog : ndarray
        Array of shape (T, k) with k return series.
    univariate_model : str
        Univariate GARCH variant to use for each series. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for the univariate GARCH. Default (1, 1).

    Attributes
    ----------
    endog : NDArray[np.float64]
        Returns array (T, k).
    T : int
        Number of observations.
    k : int
        Number of series.
    """

    model_name: str = "Unknown"

    def __init__(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t.

        Parameters
        ----------
        params : ndarray
            Correlation model parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """

    @property
    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for correlation model optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names for the correlation model."""

    # --- Concrete methods ---

    def _fit_univariate(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    def fit(self, method: str = "two_step", disp: bool = True) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

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

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
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

    def _estimate_correlation(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def _param_bounds(self) -> list[tuple[float, float]]:
        """Default parameter bounds. Override in subclasses."""
        return [(1e-6, 0.999)] * len(self.start_params)

    def _compute_covariance(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = np.zeros((n_obs, n_k, n_k))
        for t in range(n_obs):
            d_mat = np.diag(cond_vol[t])
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def _loglikelihood(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def covariance(self, corr_t: NDArray[np.float64], t: int) -> NDArray[np.float64]:
        """Get covariance matrix H_t at time t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        t : int
            Time index.

        Returns
        -------
        ndarray
            Covariance matrix (k, k).
        """
        assert self._conditional_volatility is not None
        d_mat = np.diag(self._conditional_volatility[t])
        return d_mat @ corr_t[t] @ d_mat

    def correlation(self, corr_t: NDArray[np.float64], t: int) -> NDArray[np.float64]:
        """Get correlation matrix R_t at time t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        t : int
            Time index.

        Returns
        -------
        ndarray
            Correlation matrix (k, k).
        """
        return corr_t[t]

    def portfolio_variance(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}


class MultivarResults:
    """Container for multivariate GARCH results.

    Attributes
    ----------
    model : MultivariateVolatilityModel
        The fitted model.
    univariate_results : list
        List of ArchResults from each univariate GARCH.
    params : ndarray
        Correlation model parameters.
    dynamic_correlation : ndarray
        R_t for all t, shape (T, k, k).
    dynamic_covariance : ndarray
        H_t = D_t R_t D_t for all t, shape (T, k, k).
    conditional_volatility : ndarray
        sigma_{i,t} for each series, shape (T, k).
    std_resids : ndarray
        Standardized residuals z_t, shape (T, k).
    loglike : float
        Total log-likelihood.
    aic : float
        Akaike Information Criterion.
    bic : float
        Bayesian Information Criterion.
    n_obs : int
        Number of observations.
    n_series : int
        Number of series.
    """

    def __init__(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def summary(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def plot_correlation(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def plot_covariance(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def portfolio_volatility(self, weights: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(np.maximum(port_var, 0.0))
