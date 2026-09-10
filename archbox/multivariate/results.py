"""Results container for fitted multivariate volatility models.

``MultivarResults`` is the single home of the fitted output of every
multivariate model (CCC, DCC, DECO, BEKK, GO-GARCH). It is deliberately
self-contained: every quantity a caller may need is stored on the object, so
nothing has to be read back out of mutable model state after the fit.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from archbox.multivariate.portfolio import portfolio_variance as _portfolio_variance

if TYPE_CHECKING:
    from archbox.multivariate.base import MultivariateVolatilityModel


def _as_str_list(value: Any) -> list[str]:
    """Coerce an attribute to a list of strings, returning [] when not iterable."""
    if value is None or isinstance(value, str):
        return []
    try:
        return [str(v) for v in value]
    except TypeError:
        return []


class MultivarResults:
    """Container for multivariate GARCH results.

    Parameters
    ----------
    model : MultivariateVolatilityModel
        The fitted model.
    univariate_results : list
        List of ``ArchResults`` from each univariate (or factor) GARCH fit.
    params : ndarray
        Second-step (correlation / covariance) model parameters.
    dynamic_correlation : ndarray
        R_t for all t, shape (T, k, k).
    dynamic_covariance : ndarray
        H_t = D_t R_t D_t for all t, shape (T, k, k).
    conditional_volatility : ndarray
        sigma_{i,t} for each series, shape (T, k).
    std_resids : ndarray
        Standardized residuals z_t = eps_t / sigma_t, shape (T, k).
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
    param_names : list of str, optional
        Names of ``params``. Defaults to the model's ``param_names``.
    std_errors : ndarray, optional
        Standard errors of ``params`` (``nan`` where unavailable).
    converged : bool
        Whether the second-step optimizer reported success.
    series_names : list of str, optional
        Column names of the input data when it was a pandas object.
    index : pandas.Index, optional
        Row index of the input data when it was a pandas object.
    extras : dict, optional
        Model-specific state needed for forecasting (e.g. the DCC ``Q`` path).
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
        param_names: list[str] | None = None,
        std_errors: NDArray[np.float64] | None = None,
        converged: bool = True,
        series_names: list[str] | None = None,
        index: pd.Index | None = None,
        extras: dict[str, Any] | None = None,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = np.asarray(params, dtype=np.float64)
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series
        self.converged = bool(converged)
        self.extras: dict[str, Any] = dict(extras or {})

        if param_names is None:
            param_names = _as_str_list(getattr(model, "param_names", None))
        self.param_names = list(param_names)

        if std_errors is None:
            std_errors = np.full(self.params.shape, np.nan)
        self.std_errors = np.asarray(std_errors, dtype=np.float64)

        if series_names is None:
            series_names = _as_str_list(getattr(model, "series_names", None))
        if not series_names:
            series_names = [f"series_{i}" for i in range(n_series)]
        self.series_names = list(series_names)
        self.index = index

    # --- Residual / state accessors ---

    @property
    def std_resid(self) -> NDArray[np.float64]:
        """Standardized residuals z_t (alias of ``std_resids``), shape (T, k)."""
        return self.std_resids

    @property
    def conditional_covariance(self) -> NDArray[np.float64]:
        """H_t for all t (alias of ``dynamic_covariance``), shape (T, k, k)."""
        return self.dynamic_covariance

    @property
    def conditional_correlation(self) -> NDArray[np.float64]:
        """R_t for all t (alias of ``dynamic_correlation``), shape (T, k, k)."""
        return self.dynamic_correlation

    # Compatibility aliases: ``archbox.visualization.correlation_plot`` and
    # ``archbox.report.transformers.multivariate`` read these plural / alternative
    # names off a fitted multivariate result.
    @property
    def dynamic_correlations(self) -> NDArray[np.float64]:
        """R_t for all t (plural alias used by the plotting/report helpers)."""
        return self.dynamic_correlation

    @property
    def dynamic_covariances(self) -> NDArray[np.float64]:
        """H_t for all t (plural alias used by the plotting/report helpers)."""
        return self.dynamic_covariance

    @property
    def model_name(self) -> str:
        """Name of the fitted model."""
        return str(self.model.model_name)

    @property
    def nobs(self) -> int:
        """Number of observations (alias of ``n_obs``)."""
        return self.n_obs

    @property
    def loglikelihood(self) -> float:
        """Total log-likelihood (alias of ``loglike``)."""
        return self.loglike

    @property
    def tvalues(self) -> NDArray[np.float64]:
        """t-statistics of the second-step parameters (``nan`` without SEs)."""
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.asarray(self.params / self.std_errors, dtype=np.float64)

    def covariance(self, t: int) -> NDArray[np.float64]:
        """Covariance matrix H_t at time ``t``.

        Read from the stored covariance path, not from mutable model state.

        Parameters
        ----------
        t : int
            Time index.

        Returns
        -------
        ndarray
            Covariance matrix (k, k).
        """
        return np.asarray(self.dynamic_covariance[t], dtype=np.float64)

    def correlation(self, t: int) -> NDArray[np.float64]:
        """Correlation matrix R_t at time ``t``.

        Parameters
        ----------
        t : int
            Time index.

        Returns
        -------
        ndarray
            Correlation matrix (k, k).
        """
        return np.asarray(self.dynamic_correlation[t], dtype=np.float64)

    # --- pandas-flavoured accessors (preserve input column names) ---

    def covariance_frame(self, t: int) -> pd.DataFrame:
        """H_t at time ``t`` as a DataFrame labelled with the series names."""
        return pd.DataFrame(self.covariance(t), index=self.series_names, columns=self.series_names)

    def correlation_frame(self, t: int) -> pd.DataFrame:
        """R_t at time ``t`` as a DataFrame labelled with the series names."""
        return pd.DataFrame(self.correlation(t), index=self.series_names, columns=self.series_names)

    def conditional_volatility_frame(self) -> pd.DataFrame:
        """Conditional volatilities (T, k) as a DataFrame.

        Columns carry the input column names and the row index the input index
        when the model was fitted on a pandas object.
        """
        return pd.DataFrame(
            np.asarray(self.conditional_volatility, dtype=np.float64),
            index=self.index,
            columns=self.series_names,
        )

    def std_resid_frame(self) -> pd.DataFrame:
        """Standardized residuals (T, k) as a DataFrame with named columns."""
        return pd.DataFrame(
            np.asarray(self.std_resids, dtype=np.float64),
            index=self.index,
            columns=self.series_names,
        )

    def params_frame(self) -> pd.DataFrame:
        """Second-step parameters, standard errors and t-statistics."""
        return pd.DataFrame(
            {
                "coef": self.params,
                "std_err": self.std_errors,
                "t": self.tvalues,
            },
            index=self.param_names if len(self.param_names) == len(self.params) else None,
        )

    # --- Reporting ---

    def summary(self) -> str:
        """Generate a summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append(f"  Converged:             {self.converged}")
        lines.append(f"  Series:                {', '.join(self.series_names)}")
        lines.append("")

        if self.univariate_results:
            lines.append("-" * 70)
            lines.append("Univariate GARCH Parameters")
            lines.append("-" * 70)
            for i, res in enumerate(self.univariate_results):
                name = self.series_names[i] if i < len(self.series_names) else f"Series {i}"
                names = _as_str_list(getattr(res, "param_names", None))
                values = np.asarray(getattr(res, "params", []), dtype=np.float64)
                if len(names) == len(values) and len(values) > 0:
                    body = "  ".join(f"{n}={v:.6f}" for n, v in zip(names, values, strict=True))
                else:
                    body = str(values)
                lines.append(f"  {name}: {body}")
            lines.append("")

        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            lines.append(f"  {'param':>14s} {'coef':>12s} {'std err':>12s} {'t':>10s}")
            names = self.param_names
            if len(names) != len(self.params):
                names = [f"param[{i}]" for i in range(len(self.params))]
            for name, val, se, tval in zip(
                names, self.params, self.std_errors, self.tvalues, strict=True
            ):
                se_txt = "nan" if not np.isfinite(se) else f"{se:.6f}"
                t_txt = "nan" if not np.isfinite(tval) else f"{tval:.4f}"
                lines.append(f"  {name:>14s} {val:12.6f} {se_txt:>12s} {t_txt:>10s}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def plot_correlation(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series ``i`` and ``j``.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        name_i = self.series_names[i] if i < len(self.series_names) else f"Series {i}"
        name_j = self.series_names[j] if j < len(self.series_names) else f"Series {j}"
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: {name_i} vs {name_j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def plot_covariance(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series ``i`` and ``j``.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        name_i = self.series_names[i] if i < len(self.series_names) else f"Series {i}"
        name_j = self.series_names[j] if j < len(self.series_names) else f"Series {j}"
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: {name_i} vs {name_j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def portfolio_volatility(self, weights: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute the portfolio volatility series from the stored H_t path.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = _portfolio_variance(weights, np.asarray(self.dynamic_covariance))
        return np.sqrt(np.maximum(port_var, 0.0))

    def forecast(self, horizon: int = 10) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} and R_{T+h} for h = 1, ..., ``horizon``.

        Delegates to the fitted model, passing this results object.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' and 'correlation', each (horizon, k, k).
        """
        return self.model.forecast(self, horizon=horizon)


__all__ = ["MultivarResults"]
