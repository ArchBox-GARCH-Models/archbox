"""TAR - Threshold Autoregressive Model (Tong, 1978).

The TAR model uses an abrupt (indicator) transition function based on
a threshold variable s_t:

    y_t = phi^{(1)}'x_t * I(s_t <= c) + phi^{(2)}'x_t * I(s_t > c) + eps_t

where x_t = [1, y_{t-1}, ..., y_{t-p}]'.

References
----------
- Tong, H. (1978). On a Threshold Model. In *Pattern Recognition and
  Signal Processing*, Sijthoff & Noordhoff.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.threshold.base import ThresholdModel
from archbox.threshold.results import ThresholdResults


class TAR(ThresholdModel):
    """Threshold Autoregressive model (Tong, 1978).

    Parameters
    ----------
    endog : array-like
        Endogenous time series.
    order : int
        AR order p (default 1).
    delay : int
        Delay parameter d (default 1). s_t = y_{t-d} unless threshold_var given.
    n_regimes : int
        Number of regimes (default 2).
    threshold_var : array-like, optional
        External threshold variable. If None, uses y_{t-d}.
    grid_points : int
        Number of grid points for threshold search (default 300).

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.threshold.tar import TAR
    >>> rng = np.random.default_rng(42)
    >>> n = 500
    >>> y = np.zeros(n)
    >>> for t in range(1, n):
    ...     if y[t-1] <= 0:
    ...         y[t] = 0.5 + 0.3 * y[t-1] + rng.standard_normal() * 0.5
    ...     else:
    ...         y[t] = -0.2 + 0.8 * y[t-1] + rng.standard_normal() * 0.5
    >>> model = TAR(y, order=1, delay=1)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "TAR"

    def __init__(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=n_regimes)
        self.grid_points = grid_points

        if threshold_var is not None:
            threshold_var = np.asarray(threshold_var, dtype=np.float64).ravel()
            # Align threshold variable with effective sample
            start = max(self.order, self.delay)
            if len(threshold_var) == self.nobs:
                self._s = threshold_var[start:]
            elif len(threshold_var) == len(self._s):
                self._s = threshold_var
            else:
                msg = (
                    f"threshold_var length ({len(threshold_var)}) must match "
                    f"endog ({self.nobs}) or effective sample ({len(self._s)})"
                )
                raise ValueError(msg)

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Indicator transition: G(s) = I(s > c).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [c] (threshold value).

        Returns
        -------
        ndarray
            Binary array: 0 if s <= c, 1 if s > c.
        """
        c = params[0]
        return (s > c).astype(np.float64)

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameters: median of transition variable."""
        return np.array([np.median(self._s)])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["c"]
        for regime in range(1, self.n_regimes + 1):
            names.append(f"phi_0_regime{regime}")
            for lag in range(1, self.order + 1):
                names.append(f"phi_{lag}_regime{regime}")
        return names

    def _estimate_threshold(
        self,
        s: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        grid_points: int = 300,
    ) -> tuple[float, float]:
        """Grid search for optimal threshold c.

        Parameters
        ----------
        s : ndarray
            Transition variable.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        grid_points : int
            Number of grid points.

        Returns
        -------
        best_c : float
            Optimal threshold.
        best_rss : float
            Minimal RSS at optimal threshold.
        """
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        candidates = np.linspace(s_sorted[lo], s_sorted[hi], grid_points)

        min_obs = self.order + 2  # minimum observations per regime

        best_rss = np.inf
        best_c = float(np.median(s))

        for c_val in candidates:
            mask1 = s <= c_val
            mask2 = s > c_val
            n1 = mask1.sum()
            n2 = mask2.sum()
            if n1 < min_obs or n2 < min_obs:
                continue
            rss1 = self._ols_rss(y[mask1], x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def _fit_cls(self) -> ThresholdResults:
        """Fit TAR model via Conditional Least Squares.

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for threshold
        best_c, _ = self._estimate_threshold(s, y, x_mat, self.grid_points)

        # Assign regimes
        mask1 = s <= best_c
        mask2 = s > best_c

        # OLS per regime
        beta1, resid1, rss1 = self._ols_fit(y[mask1], x_mat[mask1])
        beta2, resid2, rss2 = self._ols_fit(y[mask2], x_mat[mask2])

        n1 = mask1.sum()
        n2 = mask2.sum()
        sigma2_1 = rss1 / n1 if n1 > 0 else 0.0
        sigma2_2 = rss2 / n2 if n2 > 0 else 0.0

        # Full residuals
        resid = np.empty(len(y))
        resid[mask1] = resid1
        resid[mask2] = resid2

        # Transition values (binary)
        g_values = mask2.astype(np.float64)

        # Log-likelihood
        t_eff = len(y)
        ll = 0.0
        if n1 > 0 and sigma2_1 > 0:
            ll += -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
        if n2 > 0 and sigma2_2 > 0:
            ll += -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

        # Number of parameters: (p+1)*2 regimes + 1 threshold + 2 variances
        n_params = (self.order + 1) * 2 + 1
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"c": best_c},
            transition_params_array=np.array([best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g_values,
            transition_values=g_values,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )
