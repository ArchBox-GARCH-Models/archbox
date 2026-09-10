"""SETAR - Self-Exciting Threshold Autoregressive Model (Tong & Lim, 1980).

The SETAR model is a TAR where the threshold variable is the lagged
endogenous variable: s_t = y_{t-d}.

    y_t = phi^{(1)}'x_t * I(y_{t-d} <= c) + phi^{(2)}'x_t * I(y_{t-d} > c) + eps_t

Features:
- Automatic delay (d) selection via AIC/BIC on a common effective sample
- Extension to 3 regimes with 2 thresholds

References
----------
- Tong, H. & Lim, K.S. (1980). Threshold Autoregression, Limit Cycles
  and Cyclical Data. JRSS-B, 42(3), 245-292.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from archbox.threshold import _hard_fit
from archbox.threshold.results import ThresholdResults
from archbox.threshold.tar import TAR


class SETAR(TAR):
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
        if d_max < 1:
            msg = f"d_max must be >= 1, got {d_max}"
            raise ValueError(msg)

        effective_delay = delay if delay is not None else 1
        super().__init__(
            endog,
            order=order,
            delay=effective_delay,
            n_regimes=n_regimes,
            grid_points=grid_points,
        )

    @property
    def param_names(self) -> list[str]:
        """Parameter names (the delay is a parameter when auto-selected)."""
        names = ["delay"] if self._auto_delay else []
        names.extend(super().param_names)
        return names

    def _rebuild_for_delay(
        self, d: int, start: int | None = None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Rebuild (y, X, s) for a specific delay d.

        Parameters
        ----------
        d : int
            Delay parameter.
        start : int, optional
            First index of the effective sample (default ``max(order, d)``).

        Returns
        -------
        y, X, s : tuple of ndarrays
        """
        return self._build_for_delay(d, start=start)

    def _fit_cls(self) -> ThresholdResults:
        """Fit SETAR via Conditional Least Squares.

        Returns
        -------
        ThresholdResults
        """
        if self._auto_delay:
            return self._fit_with_delay_selection()
        return _hard_fit.build_results(self, self._y, self._X, self._s, self.delay)

    def _fit_with_delay_selection(self) -> ThresholdResults:
        """Select the delay by AIC/BIC on a common effective sample, then fit.

        Candidate delays imply different effective samples (t starts at
        ``max(p, d)``), and information criteria computed on samples of
        different length are not comparable. The comparison is therefore run
        with a common start ``max(p, d_max)`` for every candidate; the final
        model is re-estimated on the full effective sample of the winning
        delay.
        """
        d_max = self._d_max
        common_start = max(self.order, d_max)
        min_obs = 2 * (self.order + 1) + 10

        while d_max >= 1 and self.nobs - max(self.order, d_max) < min_obs:
            d_max -= 1
            common_start = max(self.order, d_max)

        best_ic = np.inf
        best_delay = 1

        for d in range(1, d_max + 1):
            y, x_mat, s = self._rebuild_for_delay(d, start=common_start)
            try:
                result = _hard_fit.build_results(self, y, x_mat, s, d, include_delay_param=True)
            except (np.linalg.LinAlgError, ValueError):
                continue
            ic_val = result.aic if self._ic == "aic" else result.bic
            if ic_val < best_ic:
                best_ic = ic_val
                best_delay = d

        # Re-estimate the winning delay on its own (longest) effective sample.
        self.delay = best_delay
        self._y, self._X, self._s = self._rebuild_for_delay(best_delay)
        return _hard_fit.build_results(
            self, self._y, self._X, self._s, best_delay, include_delay_param=True
        )
