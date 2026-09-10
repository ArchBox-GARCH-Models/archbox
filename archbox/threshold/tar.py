"""TAR - Threshold Autoregressive Model (Tong, 1978).

The TAR model uses an abrupt (indicator) transition function based on
a threshold variable s_t:

    y_t = phi^{(1)}'x_t * I(s_t <= c) + phi^{(2)}'x_t * I(s_t > c) + eps_t

where x_t = [1, y_{t-1}, ..., y_{t-p}]'. With three regimes two thresholds
c_1 < c_2 split the sample into s_t <= c_1, c_1 < s_t <= c_2 and s_t > c_2.

References
----------
- Tong, H. (1978). On a Threshold Model. In *Pattern Recognition and
  Signal Processing*, Sijthoff & Noordhoff.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.threshold import _hard_fit
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
        Delay parameter d (default 1). The transition variable is
        s_t = y_{t-d}, or z_{t-d} when ``threshold_var`` is supplied.
    n_regimes : int
        Number of regimes, 2 or 3 (default 2).
    threshold_var : array-like, optional
        External threshold variable z. If None, uses y_{t-d}.
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
            z = np.asarray(threshold_var, dtype=np.float64).ravel()
            if not np.all(np.isfinite(z)):
                msg = "threshold_var contains non-finite values (NaN or inf)"
                raise ValueError(msg)
            start = max(self.order, self.delay)
            if len(z) == self.nobs:
                # z is aligned with endog: s_t = z_{t-d}, as in the
                # self-exciting case, so the delay keeps its meaning.
                self._threshold_var = z
            elif len(z) == len(self._s):
                # z is already given on the effective sample (s_t = z_t there);
                # re-express it on the endog timeline so that s_t = z_{t-d}.
                pos = np.clip(np.arange(self.nobs) + self.delay - start, 0, len(z) - 1)
                self._threshold_var = z[pos]
            else:
                msg = (
                    f"threshold_var length ({len(z)}) must match "
                    f"endog ({self.nobs}) or effective sample ({len(self._s)})"
                )
                raise ValueError(msg)
            self._y, self._X, self._s = self._build_matrices()

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Indicator transition based on the estimated threshold(s).

        For two regimes: G(s) = I(s > c). For three regimes the values are
        0 (s <= c_1), 0.5 (c_1 < s <= c_2) and 1 (s > c_2), which
        :meth:`ThresholdModel.regime_weights` maps to the correct regime.

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            [c] for two regimes, [c_1, c_2] for three regimes.

        Returns
        -------
        ndarray
            Transition values.
        """
        s = np.asarray(s, dtype=np.float64)
        if self.n_regimes == 2:
            return (s > params[0]).astype(np.float64)
        c1, c2 = float(params[0]), float(params[1])
        g = np.zeros_like(s, dtype=np.float64)
        g[(s > c1) & (s <= c2)] = 0.5
        g[s > c2] = 1.0
        return g

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["c"] if self.n_regimes == 2 else ["c_1", "c_2"]
        for regime in range(1, self.n_regimes + 1):
            names.append(f"phi_0_regime{regime}")
            for lag in range(1, self.order + 1):
                names.append(f"phi_{lag}_regime{regime}")
        for regime in range(1, self.n_regimes + 1):
            names.append(f"sigma2_regime{regime}")
        return names

    def _estimate_threshold(
        self,
        s: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        grid_points: int = 300,
    ) -> tuple[float, float]:
        """Grid search for the optimal threshold c (two regimes).

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
        thresholds = _hard_fit.search_thresholds(
            y, x_mat, s, 2, grid_points, min_obs=self.order + 2
        )
        fit = _hard_fit.fit_given_thresholds(y, x_mat, s, thresholds)
        return thresholds[0], fit.rss

    def _fit_cls(self) -> ThresholdResults:
        """Fit TAR model via Conditional Least Squares.

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        return _hard_fit.build_results(self, self._y, self._X, self._s, self.delay)
