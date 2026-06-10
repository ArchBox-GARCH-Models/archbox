"""Results container for fitted volatility models."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import stats

if TYPE_CHECKING:
    from archbox.core.volatility_model import VolatilityModel


class ArchResults:
    """Container for fitted ARCH/GARCH model results.

    Parameters
    ----------
    model : VolatilityModel
        The fitted model instance.
    params : ndarray
        Estimated parameters.
    loglike : float
        Log-likelihood at optimum.
    sigma2 : ndarray
        Conditional variance series sigma^2_t.
    se_robust : ndarray
        Robust (Bollerslev-Wooldridge) standard errors.
    se_nonrobust : ndarray
        Non-robust (inverse Hessian) standard errors.
    convergence : bool
        Whether optimization converged.
    """

    def __init__(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        # Number of variance parameters (leading block of `params`).
        self._n_var = getattr(model, "num_params", len(params))
        if hasattr(model, "full_param_names"):
            self.param_names = model.full_param_names()
        else:
            self.param_names = model.param_names
        # Fitted distribution shape parameters (trailing block of `params`).
        self._dist_params = np.asarray(params[self._n_var :], dtype=np.float64)
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def persistence(self) -> float:
        """Compute persistence: sum(alpha_i) + sum(beta_j).

        Returns
        -------
        float
            Persistence value. Must be < 1 for stationarity.
        """
        # params = [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, dist...]
        return float(np.sum(self.params[1 : self._n_var]))

    def half_life(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def unconditional_variance(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("inf")
        return float(self.params[0] / (1.0 - p))

    def forecast(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        q = getattr(self._model, "q", 1)
        alphas = self.params[1 : 1 + q]
        betas = self.params[1 + q : self._n_var]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def _fitted_dist(self) -> Any:
        """Return a distribution instance reflecting the fitted shape params.

        The distribution objects expose ``ppf``/``cdf`` that read shape params
        from internal fixed values (set at construction). Since the fitted
        instance on the model holds no fitted shape value, we rebuild a fresh
        instance with the estimated parameters bound as constructor kwargs.

        If the estimated shape params cannot be mapped onto the constructor
        (unknown distribution), we fall back to the model's distribution
        instance and its default shape parameters.
        """
        dist = self._model.dist
        names = list(getattr(dist, "param_names", []))
        if len(self._dist_params) == 0 or len(names) != len(self._dist_params):
            return dist

        # Map fitted param names to known constructor kwargs.
        kwarg_map = {"nu": "nu", "lambda": "lam", "lam": "lam", "p": "p", "sigma1": "sigma1"}
        kwargs: dict[str, float] = {}
        for name, value in zip(names, self._dist_params, strict=True):
            key = kwarg_map.get(name)
            if key is None:
                # Unknown shape param: fall back to model's dist (default shape).
                return dist
            kwargs[key] = float(value)
        try:
            return type(dist)(**kwargs)
        except TypeError:
            # Constructor signature mismatch: fall back to model's dist.
            return dist

    def _sigma_next(self) -> float:
        """Conditional std for the next step (one-step-ahead forecast)."""
        try:
            fc = self.forecast(horizon=1)
            return float(np.sqrt(fc["variance"][0]))
        except Exception:  # noqa: BLE001 - robust fallback to last fitted sigma
            return float(np.sqrt(self._sigma2[-1]))

    def var(self, alpha: float = 0.05, horizon: int = 1) -> float:
        """One-step parametric Value-at-Risk as a positive loss number.

        Parameters
        ----------
        alpha : float
            Tail probability (e.g. 0.01 for 99% VaR).
        horizon : int
            Forecast horizon (one-step variance is used for the std).

        Returns
        -------
        float
            VaR as a positive loss magnitude.
        """
        sigma_next = self._sigma_next()
        dist = self._fitted_dist()
        quantile = float(dist.ppf(alpha))
        return float(-(self._model.mu + sigma_next * quantile))

    def es(self, alpha: float = 0.05) -> float:
        """Parametric Expected Shortfall (positive loss).

        Parameters
        ----------
        alpha : float
            Tail probability (e.g. 0.01 for 99% ES).

        Returns
        -------
        float
            Expected Shortfall as a positive loss magnitude.
        """
        sigma_next = self._sigma_next()
        dist = self._fitted_dist()

        # Closed form for Normal; numeric integration of the inverse CDF
        # (tail mean of the quantile function) for general distributions.
        if dist.name == "Normal":
            q = float(stats.norm.ppf(alpha))
            tail_mean_z = -float(stats.norm.pdf(q)) / alpha
        else:
            us = np.linspace(1e-4, alpha, 200)
            tail_mean_z = float(np.mean([dist.ppf(float(u)) for u in us]))

        return float(-(self._model.mu + sigma_next * tail_mean_z))

    def summary(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def plot(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def to_dataframe(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def save(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str | Path) -> ArchResults:
        """Load results from pickle file.

        Parameters
        ----------
        path : str or Path
            Input file path.

        Returns
        -------
        ArchResults
            Loaded results.
        """
        with open(path, "rb") as f:
            return pickle.load(f)  # noqa: S301  # nosec B301

    def __repr__(self) -> str:
        """Return string representation of ArchResults."""
        return (
            f"ArchResults(model={self._model.volatility_process}, "
            f"nobs={self.nobs}, loglike={self.loglike:.4f})"
        )
