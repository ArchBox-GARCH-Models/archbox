"""Value at Risk (VaR) implementations.

Every method returns VaR on the scale of the returns, as a *signed* quantile:
a value of ``-0.02`` means "a 2% loss". The series are aligned with the return
series of the fitted model, so ``returns[t] < var[t]`` is a violation at date
``t``.

Methods:
    - Parametric (fitted conditional distribution, Normal, Student-t, ...)
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

import numpy as np
from numpy.typing import NDArray

from archbox.risk.base import RiskMeasure


class ValueAtRisk(RiskMeasure):
    """Value at Risk calculator.

    Parameters
    ----------
    results : ArchResults
        Fitted model results from archbox (``model.fit()``).
    alpha : float
        Tail probability (e.g. 0.05 for 95% VaR). Default is 0.05.

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

    Examples
    --------
    >>> from archbox import GARCH
    >>> from archbox.datasets import load_dataset
    >>> returns = load_dataset('sp500')['returns'].to_numpy()
    >>> res = GARCH(returns).fit(disp=False)
    >>> var = ValueAtRisk(res, alpha=0.05).parametric()
    """

    def parametric(
        self,
        dist: str | None = None,
        nu: float | None = None,
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str, optional
            Distribution used for the innovation quantile: ``'normal'``,
            ``'studentt'``, ``'ged'``, ``'skewed-t'``, ``'mixture-normal'``.
            The default (``None``) uses the distribution the model was fitted
            with, together with its *estimated* shape parameters.
        nu : float, optional
            Degrees of freedom for Student-t. The default (``None``) uses the
            fitted ``nu`` when the model carries one, and falls back to
            :data:`~archbox.risk.base.DEFAULT_NU` only when Student-t measures
            are requested on a model fitted without a ``nu``.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        ``VaR_alpha(t) = mu + sigma_t * F^{-1}_z(alpha)``

        where ``F_z`` is the standardized (zero mean, unit variance)
        conditional distribution of the innovations. For the Normal this is
        ``Phi^{-1}(alpha)``; for the Student-t
        ``t^{-1}_nu(alpha) * sqrt((nu-2)/nu)``.
        """
        quantile = self._standardized_quantile(dist, nu)
        return self.mu + self.conditional_volatility * quantile

    def historical(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). The first ``window`` values are NaN.

        Raises
        ------
        ValueError
            If ``window`` is not a positive integer.

        Notes
        -----
        ``VaR_alpha(t) = quantile(r_{t-W}, ..., r_{t-1}; alpha)``

        The quantile is taken over the *raw returns* (mean included), so the
        result is on the return scale, and only observations strictly before
        ``t`` enter the window (the forecast is out-of-sample at each date).
        """
        window = int(window)
        if window < 1:
            msg = f"window must be a positive integer, got {window}"
            raise ValueError(msg)

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            var_series[t] = np.quantile(self.returns[t - window : t], self.alpha)

        return var_series

    def filtered_historical(self, min_obs: int = 50) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Parameters
        ----------
        min_obs : int
            Minimum number of standardized residuals required before a
            quantile is reported. Default is 50.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). The first ``min_obs`` values are NaN.

        Notes
        -----
        Barone-Adesi et al. (1999):

        1. ``z_t = eps_t / sigma_t`` (standardized residuals of the fit)
        2. ``VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1}; alpha)``

        FHS combines the GARCH volatility dynamics (through ``sigma_t``, which
        is known at ``t-1``) with the empirical distribution of the
        standardized residuals, so the result is on the return scale.
        """
        min_obs = int(min_obs)
        if min_obs < 1:
            msg = f"min_obs must be a positive integer, got {min_obs}"
            raise ValueError(msg)

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)
        sigma = self.conditional_volatility

        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(self.std_resid[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def monte_carlo(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation of the fitted model.

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
            VaR of the return at each future date, shape ``(horizon,)``, on the
            return scale. ``result[h]`` is the VaR of ``r_{T+h+1}``.

        Raises
        ------
        TypeError
            If the results do not come from a fitted archbox volatility model.

        Notes
        -----
        The paths continue the estimation sample: the one-step conditional
        variance is the model's own forecast, the innovations are drawn from
        the *fitted* conditional distribution (Student-t, GED, skewed-t, ...),
        and multi-step paths iterate the model's own variance recursion, so
        the simulated variance is path dependent (not deterministic).
        """
        sims = self._simulate_future_returns(n_sims, horizon, seed)
        return np.quantile(sims, self.alpha, axis=0)
