"""Expected Shortfall (ES / CVaR) implementations.

The Expected Shortfall at level alpha is the expected return given that the
return falls below the VaR at the same level. Like
:class:`~archbox.risk.var.ValueAtRisk`, every method returns a *signed* number
on the scale of the returns: ``-0.03`` means "an expected 3% loss in the tail".

Methods:
    - Parametric (fitted conditional distribution, Normal, Student-t, ...)
    - Historical
    - Filtered Historical Simulation
    - Monte Carlo

References
----------
- Artzner, P., Delbaen, F., Eber, J.-M. & Heath, D. (1999).
  Coherent Measures of Risk. Mathematical Finance, 9(3), 203-228.
- McNeil, A.J., Frey, R. & Embrechts, P. (2015).
  Quantitative Risk Management. 2nd ed. Princeton University Press. Cap. 2.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from archbox.risk.base import RiskMeasure


class ExpectedShortfall(RiskMeasure):
    """Expected Shortfall (CVaR) calculator.

    Parameters
    ----------
    results : ArchResults
        Fitted model results from archbox (``model.fit()``).
    alpha : float
        Tail probability (e.g. 0.05 for 95% ES). Default is 0.05.

    Attributes
    ----------
    results : ArchResults
        The fitted model results.
    alpha : float
        Tail probability.
    returns : NDArray[np.float64]
        Return series ``r_t = mu + eps_t`` (raw, on the return scale).
    resid : NDArray[np.float64]
        Raw residuals ``eps_t``.
    std_resid : NDArray[np.float64]
        Standardized residuals ``z_t = eps_t / sigma_t``.
    conditional_volatility : NDArray[np.float64]
        Conditional volatility series ``sigma_t``.
    mu : float
        Fitted mean of the return process.
    """

    def parametric(
        self,
        dist: str | None = None,
        nu: float | None = None,
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str, optional
            Distribution used for the innovation tail: ``'normal'``,
            ``'studentt'``, ``'ged'``, ``'skewed-t'``, ``'mixture-normal'``.
            The default (``None``) uses the distribution the model was fitted
            with, together with its *estimated* shape parameters.
        nu : float, optional
            Degrees of freedom for Student-t. The default (``None``) uses the
            fitted ``nu`` when the model carries one.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        ``ES_alpha(t) = mu + sigma_t * E[z | z <= F^{-1}_z(alpha)]``

        Normal:
            ``E[z | .] = -phi(z_alpha) / alpha``

        Student-t (standardized to unit variance):
            ``E[z | .] = -(f_nu(t_alpha) / alpha) * ((nu + t_alpha^2) / (nu-1))
            * sqrt((nu-2)/nu)``

        For any other fitted distribution the tail integral of the quantile
        function is evaluated numerically.
        """
        tail_mean = self._standardized_tail_mean(dist, nu)
        return self.mu + self.conditional_volatility * tail_mean

    def historical(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). The first ``window`` values are NaN.

        Raises
        ------
        ValueError
            If ``window`` is not a positive integer.

        Notes
        -----
        ``ES_alpha(t) = mean(r_s | r_s <= VaR_alpha(t))`` over the rolling
        window ``s in [t-W, t-1]`` of *raw returns*, so the result is on the
        return scale.
        """
        window = int(window)
        if window < 1:
            msg = f"window must be a positive integer, got {window}"
            raise ValueError(msg)

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def filtered_historical(self, min_obs: int = 50) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Parameters
        ----------
        min_obs : int
            Minimum number of standardized residuals required before a value
            is reported. Default is 50.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). The first ``min_obs`` values are NaN.

        Notes
        -----
        1. ``z_t = eps_t / sigma_t`` (standardized residuals of the fit)
        2. ``ES_t = mu + sigma_t * mean(z_s | z_s <= quantile(z; alpha))``
        """
        min_obs = int(min_obs)
        if min_obs < 1:
            msg = f"min_obs must be a positive integer, got {min_obs}"
            raise ValueError(msg)

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)
        sigma = self.conditional_volatility

        for t in range(min_obs, n_obs):
            z_window = self.std_resid[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def monte_carlo(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute ES by Monte Carlo simulation of the fitted model.

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
            ES of the return at each future date, shape ``(horizon,)``, on the
            return scale. ``result[h]`` is the ES of ``r_{T+h+1}``.

        Notes
        -----
        The paths are generated exactly as in
        :meth:`archbox.risk.var.ValueAtRisk.monte_carlo` (fitted innovation
        distribution, model-specific variance recursion); the ES is the mean of
        the simulated returns at or below their empirical alpha-quantile.
        """
        sims = self._simulate_future_returns(n_sims, horizon, seed)
        var_h = np.quantile(sims, self.alpha, axis=0)

        es = np.empty(sims.shape[1], dtype=np.float64)
        for h in range(sims.shape[1]):
            tail = sims[:, h][sims[:, h] <= var_h[h]]
            es[h] = float(np.mean(tail)) if tail.size else float(var_h[h])
        return es
