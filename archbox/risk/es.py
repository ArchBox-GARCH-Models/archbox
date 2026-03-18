"""Expected Shortfall (ES / CVaR) implementations.

The Expected Shortfall at level alpha is the expected loss given that
the loss exceeds the VaR at the same level.

Methods:
    - Parametric (Normal, Student-t)
    - Historical
    - Filtered Historical Simulation

References
----------
- Artzner, P., Delbaen, F., Eber, J.-M. & Heath, D. (1999).
  Coherent Measures of Risk. Mathematical Finance, 9(3), 203-228.
- McNeil, A.J., Frey, R. & Embrechts, P. (2015).
  Quantitative Risk Management. 2nd ed. Princeton University Press. Cap. 2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from scipy import stats

if TYPE_CHECKING:
    pass


class ExpectedShortfall:
    """Expected Shortfall (CVaR) calculator.

    Parameters
    ----------
    results : ArchResults
        Fitted model results from archbox.
    alpha : float
        Significance level (e.g., 0.05 for 5% ES). Default is 0.05.

    Attributes
    ----------
    results : ArchResults
        The fitted model results.
    alpha : float
        Significance level.
    returns : NDArray[np.float64]
        The return series.
    conditional_volatility : NDArray[np.float64]
        Conditional volatility series sigma_t.
    """

    def __init__(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

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
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def historical(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def filtered_historical(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series
