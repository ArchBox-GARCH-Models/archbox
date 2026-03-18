"""Value at Risk (VaR) implementations.

Methods:
    - Parametric (Normal, Student-t)
    - Historical Simulation
    - Filtered Historical Simulation (Barone-Adesi et al., 1999)
    - Monte Carlo

References
----------
- Barone-Adesi, G., Giannopoulos, K. & Vosper, L. (1999).
  VaR Without Correlations for Portfolios of Derivative Securities.
  Journal of Futures Markets, 19(5), 583-602.
- McNeil, A.J., Frey, R. & Embrechts, P. (2015).
  Quantitative Risk Management. 2nd ed. Princeton University Press.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from scipy import stats

if TYPE_CHECKING:
    pass


class ValueAtRisk:
    """Value at Risk calculator.

    Parameters
    ----------
    results : ArchResults
        Fitted model results from archbox.
    alpha : float
        Significance level (e.g., 0.05 for 5% VaR). Default is 0.05.

    Attributes
    ----------
    results : ArchResults
        The fitted model results.
    alpha : float
        Significance level.
    returns : NDArray[np.float64]
        The return series from the fitted model.
    conditional_volatility : NDArray[np.float64]
        Conditional volatility series sigma_t.
    """

    def __init__(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def parametric(self, dist: str = "normal", nu: float = 8.0) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def historical(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def filtered_historical(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def monte_carlo(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series
