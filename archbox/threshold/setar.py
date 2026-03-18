"""SETAR - Self-Exciting Threshold Autoregressive Model (Tong & Lim, 1980).

The SETAR model is a TAR where the threshold variable is the lagged
endogenous variable: s_t = y_{t-d}.

    y_t = phi^{(1)}'x_t * I(y_{t-d} <= c) + phi^{(2)}'x_t * I(y_{t-d} > c) + eps_t

Features:
- Automatic delay (d) selection via AIC/BIC
- Extension to 3 regimes with 2 thresholds

References
----------
- Tong, H. & Lim, K.S. (1980). Threshold Autoregression, Limit Cycles
  and Cyclical Data. JRSS-B, 42(3), 245-292.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.threshold.base import ThresholdModel
from archbox.threshold.results import ThresholdResults


class SETAR(ThresholdModel):
    """Self-Exciting Threshold Autoregressive model (Tong & Lim, 1980).

    Parameters
    ----------
    endog : array-like
        Endogenous time series.
    order : int
        AR order p (default 1).
    delay : int | None
        Delay parameter d (default None = auto-select from 1..d_max).
    n_regimes : int
        Number of regimes: 2 or 3 (default 2).
    d_max : int
        Maximum delay to search when delay=None (default 6).
    grid_points : int
        Number of grid points for threshold search (default 300).
    ic : str
        Information criterion for delay selection: 'aic' or 'bic' (default 'aic').

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.threshold.setar import SETAR
    >>> rng = np.random.default_rng(42)
    >>> n = 500
    >>> y = np.zeros(n)
    >>> for t in range(1, n):
    ...     if y[t-1] <= 0:
    ...         y[t] = 0.5 + 0.3 * y[t-1] + rng.standard_normal() * 0.5
    ...     else:
    ...         y[t] = -0.2 + 0.8 * y[t-1] + rng.standard_normal() * 0.5
    >>> model = SETAR(y, order=1, n_regimes=2)
    >>> results = model.fit()
    >>> print(f"Threshold: {results.threshold}")
    >>> print(f"Delay: {results.delay}")
    """

    model_name: str = "SETAR"

    def __init__(
        self,
        endog: Any,
        order: int = 1,
        delay: int | None = None,
        n_regimes: int = 2,
        d_max: int = 6,
        grid_points: int = 300,
        ic: str = "aic",
    ) -> None:
        """Initialize SETAR model with threshold search configuration."""
        self._auto_delay = delay is None
        self._d_max = d_max
        self._ic = ic.lower()
        if self._ic not in ("aic", "bic"):
            msg = f"ic must be 'aic' or 'bic', got '{ic}'"
            raise ValueError(msg)

        effective_delay = delay if delay is not None else 1
        super().__init__(endog, order=order, delay=effective_delay, n_regimes=n_regimes)
        self.grid_points = grid_points

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Indicator transition: G(s) = I(s > c).

        For 3 regimes, returns values in {0, 0.5, 1}:
        - 0: regime 1 (s <= c1)
        - 0.5: regime 2 (c1 < s <= c2)
        - 1: regime 3 (s > c2)

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            [c] for 2 regimes, [c1, c2] for 3 regimes.

        Returns
        -------
        ndarray
            Transition values.
        """
        if self.n_regimes == 2:
            c = params[0]
            return (s > c).astype(np.float64)
        else:
            c1, c2 = params[0], params[1]
            g = np.zeros_like(s)
            g[(s > c1) & (s <= c2)] = 0.5
            g[s > c2] = 1.0
            return g

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameters."""
        if self.n_regimes == 2:
            return np.array([np.median(self._s)])
        q1 = np.percentile(self._s, 33)
        q2 = np.percentile(self._s, 67)
        return np.array([q1, q2])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["delay"]
        if self.n_regimes == 2:
            names.append("c")
        else:
            names.extend(["c_1", "c_2"])
        for regime in range(1, self.n_regimes + 1):
            names.append(f"phi_0_regime{regime}")
            for lag in range(1, self.order + 1):
                names.append(f"phi_{lag}_regime{regime}")
        return names

    def _rebuild_for_delay(
        self, d: int
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Rebuild matrices for a specific delay d.

        Parameters
        ----------
        d : int
            Delay parameter.

        Returns
        -------
        y, X, s : tuple of ndarrays
        """
        p = self.order
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]
        return y, x_mat, s

    def _fit_two_regimes(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[
        float,
        float,
        NDArray[np.float64],
        NDArray[np.float64],
        float,
        float,
        float,
    ]:
        """Fit 2-regime SETAR for given y, X, s.

        Returns
        -------
        c, rss_total, beta1, beta2, sigma2_1, sigma2_2, loglike
        """
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        grid = np.linspace(s_sorted[lo], s_sorted[hi], self.grid_points)

        min_obs = self.order + 2
        best_rss = np.inf
        best_c = float(np.median(s))

        for c in grid:
            mask1 = s <= c
            mask2 = s > c
            if mask1.sum() < min_obs or mask2.sum() < min_obs:
                continue
            rss = self._ols_rss(y[mask1], x_mat[mask1]) + self._ols_rss(y[mask2], x_mat[mask2])
            if rss < best_rss:
                best_rss = rss
                best_c = float(c)

        mask1 = s <= best_c
        mask2 = s > best_c
        beta1, _, rss1 = self._ols_fit(y[mask1], x_mat[mask1])
        beta2, _, rss2 = self._ols_fit(y[mask2], x_mat[mask2])

        n1, n2 = int(mask1.sum()), int(mask2.sum())
        sigma2_1 = rss1 / n1 if n1 > 0 else 1e-6
        sigma2_2 = rss2 / n2 if n2 > 0 else 1e-6

        ll = 0.0
        if n1 > 0 and sigma2_1 > 0:
            ll += -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
        if n2 > 0 and sigma2_2 > 0:
            ll += -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

        return best_c, best_rss, beta1, beta2, sigma2_1, sigma2_2, ll

    def _fit_three_regimes(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[
        list[float],
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
        dict[str, float],
        float,
    ]:
        """Fit 3-regime SETAR.

        Returns
        -------
        thresholds, beta1, beta2, beta3, sigma2_dict, loglike
        """
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1

        grid_n = min(self.grid_points, 100)  # coarser grid for 3 regimes
        grid = np.linspace(s_sorted[lo], s_sorted[hi], grid_n)

        min_obs = self.order + 2
        best_rss = np.inf
        best_c1 = float(np.percentile(s, 33))
        best_c2 = float(np.percentile(s, 67))

        for i, c1 in enumerate(grid):
            for c2 in grid[i + 1 :]:
                mask1 = s <= c1
                mask2 = (s > c1) & (s <= c2)
                mask3 = s > c2
                if mask1.sum() < min_obs or mask2.sum() < min_obs or mask3.sum() < min_obs:
                    continue
                rss = (
                    self._ols_rss(y[mask1], x_mat[mask1])
                    + self._ols_rss(y[mask2], x_mat[mask2])
                    + self._ols_rss(y[mask3], x_mat[mask3])
                )
                if rss < best_rss:
                    best_rss = rss
                    best_c1, best_c2 = float(c1), float(c2)

        mask1 = s <= best_c1
        mask2 = (s > best_c1) & (s <= best_c2)
        mask3 = s > best_c2

        beta1, _, rss1 = self._ols_fit(y[mask1], x_mat[mask1])
        beta2, _, rss2 = self._ols_fit(y[mask2], x_mat[mask2])
        beta3, _, rss3 = self._ols_fit(y[mask3], x_mat[mask3])

        n1, n2, n3 = int(mask1.sum()), int(mask2.sum()), int(mask3.sum())
        sigma2_1 = rss1 / n1 if n1 > 0 else 1e-6
        sigma2_2 = rss2 / n2 if n2 > 0 else 1e-6
        sigma2_3 = rss3 / n3 if n3 > 0 else 1e-6

        ll = 0.0
        for ni, rss_i, s2_i in [
            (n1, rss1, sigma2_1),
            (n2, rss2, sigma2_2),
            (n3, rss3, sigma2_3),
        ]:
            if ni > 0 and s2_i > 0:
                ll += -0.5 * ni * (np.log(2 * np.pi) + np.log(s2_i)) - rss_i / (2 * s2_i)

        return (
            [best_c1, best_c2],
            beta1,
            beta2,
            beta3,
            {"regime_1": sigma2_1, "regime_2": sigma2_2, "regime_3": sigma2_3},
            ll,
        )

    def _fit_cls(self) -> ThresholdResults:
        """Fit SETAR via Conditional Least Squares.

        Returns
        -------
        ThresholdResults
        """
        if self._auto_delay:
            return self._fit_with_delay_selection()

        if self.n_regimes == 2:
            return self._fit_2regime_fixed_delay()
        return self._fit_3regime_fixed_delay()

    def _fit_with_delay_selection(self) -> ThresholdResults:
        """Select optimal delay via AIC/BIC, then fit."""
        best_ic = np.inf
        best_delay = 1
        best_results: ThresholdResults | None = None

        for d in range(1, self._d_max + 1):
            try:
                y, x_mat, s = self._rebuild_for_delay(d)
            except Exception:  # noqa: BLE001
                continue

            if len(y) < 2 * (self.order + d) + 10:
                continue

            # Save and restore state
            old_delay = self.delay
            old_y, old_x, old_s = self._y, self._X, self._s
            self.delay = d
            self._y, self._X, self._s = y, x_mat, s

            try:
                if self.n_regimes == 2:
                    result = self._fit_2regime_fixed_delay()
                else:
                    result = self._fit_3regime_fixed_delay()

                ic_val = result.aic if self._ic == "aic" else result.bic
                if ic_val < best_ic:
                    best_ic = ic_val
                    best_delay = d
                    best_results = result
            except Exception:  # noqa: BLE001
                pass
            finally:
                self.delay = old_delay
                self._y, self._X, self._s = old_y, old_x, old_s

        if best_results is None:
            # Fallback to delay=1
            self.delay = 1
            self._y, self._X, self._s = self._rebuild_for_delay(1)
            if self.n_regimes == 2:
                best_results = self._fit_2regime_fixed_delay()
            else:
                best_results = self._fit_3regime_fixed_delay()
        else:
            # Set final delay
            self.delay = best_delay
            self._y, self._X, self._s = self._rebuild_for_delay(best_delay)

        return best_results

    def _fit_2regime_fixed_delay(self) -> ThresholdResults:
        """Fit 2-regime SETAR with current delay."""
        y, x_mat, s = self._y, self._X, self._s
        best_c, _, beta1, beta2, sigma2_1, sigma2_2, ll = self._fit_two_regimes(y, x_mat, s)

        mask1 = s <= best_c
        mask2 = s > best_c
        resid = np.empty(len(y))
        resid[mask1] = y[mask1] - x_mat[mask1] @ beta1
        resid[mask2] = y[mask2] - x_mat[mask2] @ beta2

        g = mask2.astype(np.float64)
        t = len(y)
        n_params = (self.order + 1) * 2 + 1 + 1  # +1 for delay
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t) * n_params

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"c": best_c},
            transition_params_array=np.array([best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=float(aic),
            bic=float(bic),
            nobs=t,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def _fit_3regime_fixed_delay(self) -> ThresholdResults:
        """Fit 3-regime SETAR with current delay."""
        y, x_mat, s = self._y, self._X, self._s
        thresholds, beta1, beta2, beta3, sigma2_dict, ll = self._fit_three_regimes(y, x_mat, s)

        c1, c2 = thresholds
        mask1 = s <= c1
        mask2 = (s > c1) & (s <= c2)
        mask3 = s > c2

        resid = np.empty(len(y))
        resid[mask1] = y[mask1] - x_mat[mask1] @ beta1
        resid[mask2] = y[mask2] - x_mat[mask2] @ beta2
        resid[mask3] = y[mask3] - x_mat[mask3] @ beta3

        g = np.zeros(len(y))
        g[mask2] = 0.5
        g[mask3] = 1.0

        t = len(y)
        n_params = (self.order + 1) * 3 + 2 + 1  # 3 regimes + 2 thresholds + delay
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t) * n_params

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2, "regime_3": beta3},
            threshold=thresholds,
            delay=self.delay,
            transition_params={"c_1": c1, "c_2": c2},
            transition_params_array=np.array([c1, c2]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2=sigma2_dict,
            loglike=ll,
            aic=float(aic),
            bic=float(bic),
            nobs=t,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )
