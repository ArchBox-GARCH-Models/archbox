"""HAR-RV - Heterogeneous Autoregressive Realized Volatility (Corsi, 2009).

RV_t = beta_0 + beta_d * RV_{t-1} + beta_w * RV_w_{t-1} + beta_m * RV_m_{t-1} + eps_t

where:
- RV^{(d)}: daily realized variance
- RV^{(w)} = (1/5) * sum_{i=0}^{4} RV_{t-i}^{(d)}: weekly average
- RV^{(m)} = (1/22) * sum_{i=0}^{21} RV_{t-i}^{(d)}: monthly average
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass
class HARRVResults:
    """Results container for HAR-RV model.

    Attributes
    ----------
    params : ndarray
        Estimated coefficients [beta_0, beta_d, beta_w, beta_m].
    param_names : list[str]
        Parameter names.
    std_errors : ndarray
        Standard errors of coefficients.
    t_values : ndarray
        t-statistics.
    r_squared : float
        R-squared of the regression.
    adj_r_squared : float
        Adjusted R-squared.
    residuals : ndarray
        OLS residuals.
    fitted_values : ndarray
        Fitted values.
    nobs : int
        Number of observations used in the regression.
    """

    params: NDArray[np.float64]
    param_names: list[str]
    std_errors: NDArray[np.float64]
    t_values: NDArray[np.float64]
    r_squared: float
    adj_r_squared: float
    residuals: NDArray[np.float64]
    fitted_values: NDArray[np.float64]
    nobs: int

    def summary(self) -> str:
        """Generate summary table."""
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("HAR-RV Regression Results")
        lines.append("=" * 60)
        lines.append(f"Observations: {self.nobs}")
        lines.append(f"R-squared: {self.r_squared:.6f}")
        lines.append(f"Adj. R-squared: {self.adj_r_squared:.6f}")
        lines.append("-" * 60)
        lines.append(f"{'Parameter':<15} {'Estimate':>12} {'Std.Err':>12} {'t-value':>12}")
        lines.append("-" * 60)
        for name, coef, se, t in zip(
            self.param_names,
            self.params,
            self.std_errors,
            self.t_values,
            strict=True,
        ):
            lines.append(f"{name:<15} {coef:>12.6f} {se:>12.6f} {t:>12.4f}")
        lines.append("=" * 60)
        return "\n".join(lines)

    def forecast(self, horizon: int = 1) -> NDArray[np.float64]:
        """Forecast realized variance.

        Simple iterative forecast using last available RV values.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.

        Returns
        -------
        ndarray
            Forecast values.
        """
        # Use last fitted value as base forecast
        forecasts = np.full(horizon, self.fitted_values[-1])
        return forecasts


class HARRV:
    """Heterogeneous Autoregressive Realized Volatility model.

    Parameters
    ----------
    realized_variance : array-like
        Time series of daily realized variance.
    components : list[str]
        HAR components. Default ['daily', 'weekly', 'monthly'].
    """

    def __init__(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def _build_regressors(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def fit(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )
