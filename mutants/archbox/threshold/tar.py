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

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from archbox.threshold.base import ThresholdModel
from archbox.threshold.results import ThresholdResults

MutantDict = Annotated[dict[str, Callable], "Mutant"]  # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):  # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os  # type: ignore

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]  # type: ignore
    if mutant_under_test == "fail":  # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException  # type: ignore

        raise MutmutProgrammaticFailException("Failed programmatically")  # type: ignore
    elif mutant_under_test == "stats":  # type: ignore
        from mutmut.__main__ import record_trampoline_hit  # type: ignore

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)  # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"  # type: ignore
    if not mutant_under_test.startswith(prefix):  # type: ignore
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    mutant_name = mutant_under_test.rpartition(".")[-1]  # type: ignore
    if self_arg is not None:  # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)  # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)  # type: ignore
    return result  # type: ignore


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
        args = [endog, order, delay, n_regimes, threshold_var, grid_points]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁTARǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁTARǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁTARǁ__init____mutmut_orig(
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

    def xǁTARǁ__init____mutmut_1(
        self,
        endog: Any,
        order: int = 2,
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

    def xǁTARǁ__init____mutmut_2(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 2,
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

    def xǁTARǁ__init____mutmut_3(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 3,
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

    def xǁTARǁ__init____mutmut_4(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 301,
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

    def xǁTARǁ__init____mutmut_5(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(None, order=order, delay=delay, n_regimes=n_regimes)
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

    def xǁTARǁ__init____mutmut_6(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(endog, order=None, delay=delay, n_regimes=n_regimes)
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

    def xǁTARǁ__init____mutmut_7(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(endog, order=order, delay=None, n_regimes=n_regimes)
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

    def xǁTARǁ__init____mutmut_8(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=None)
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

    def xǁTARǁ__init____mutmut_9(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(order=order, delay=delay, n_regimes=n_regimes)
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

    def xǁTARǁ__init____mutmut_10(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(endog, delay=delay, n_regimes=n_regimes)
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

    def xǁTARǁ__init____mutmut_11(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(endog, order=order, n_regimes=n_regimes)
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

    def xǁTARǁ__init____mutmut_12(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
        threshold_var: Any | None = None,
        grid_points: int = 300,
    ) -> None:
        """Initialize TAR model with threshold configuration."""
        super().__init__(
            endog,
            order=order,
            delay=delay,
        )
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

    def xǁTARǁ__init____mutmut_13(
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
        self.grid_points = None

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

    def xǁTARǁ__init____mutmut_14(
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

        if threshold_var is None:
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

    def xǁTARǁ__init____mutmut_15(
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
            threshold_var = None
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

    def xǁTARǁ__init____mutmut_16(
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
            threshold_var = np.asarray(None, dtype=np.float64).ravel()
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

    def xǁTARǁ__init____mutmut_17(
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
            threshold_var = np.asarray(threshold_var, dtype=None).ravel()
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

    def xǁTARǁ__init____mutmut_18(
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
            threshold_var = np.asarray(dtype=np.float64).ravel()
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

    def xǁTARǁ__init____mutmut_19(
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
            threshold_var = np.asarray(
                threshold_var,
            ).ravel()
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

    def xǁTARǁ__init____mutmut_20(
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
            start = None
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

    def xǁTARǁ__init____mutmut_21(
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
            start = max(None, self.delay)
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

    def xǁTARǁ__init____mutmut_22(
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
            start = max(self.order, None)
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

    def xǁTARǁ__init____mutmut_23(
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
            start = max(self.delay)
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

    def xǁTARǁ__init____mutmut_24(
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
            start = max(
                self.order,
            )
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

    def xǁTARǁ__init____mutmut_25(
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
            if len(threshold_var) != self.nobs:
                self._s = threshold_var[start:]
            elif len(threshold_var) == len(self._s):
                self._s = threshold_var
            else:
                msg = (
                    f"threshold_var length ({len(threshold_var)}) must match "
                    f"endog ({self.nobs}) or effective sample ({len(self._s)})"
                )
                raise ValueError(msg)

    def xǁTARǁ__init____mutmut_26(
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
                self._s = None
            elif len(threshold_var) == len(self._s):
                self._s = threshold_var
            else:
                msg = (
                    f"threshold_var length ({len(threshold_var)}) must match "
                    f"endog ({self.nobs}) or effective sample ({len(self._s)})"
                )
                raise ValueError(msg)

    def xǁTARǁ__init____mutmut_27(
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
            elif len(threshold_var) != len(self._s):
                self._s = threshold_var
            else:
                msg = (
                    f"threshold_var length ({len(threshold_var)}) must match "
                    f"endog ({self.nobs}) or effective sample ({len(self._s)})"
                )
                raise ValueError(msg)

    def xǁTARǁ__init____mutmut_28(
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
                self._s = None
            else:
                msg = (
                    f"threshold_var length ({len(threshold_var)}) must match "
                    f"endog ({self.nobs}) or effective sample ({len(self._s)})"
                )
                raise ValueError(msg)

    def xǁTARǁ__init____mutmut_29(
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
                msg = None
                raise ValueError(msg)

    def xǁTARǁ__init____mutmut_30(
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
                raise ValueError(None)

    xǁTARǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁTARǁ__init____mutmut_1": xǁTARǁ__init____mutmut_1,
        "xǁTARǁ__init____mutmut_2": xǁTARǁ__init____mutmut_2,
        "xǁTARǁ__init____mutmut_3": xǁTARǁ__init____mutmut_3,
        "xǁTARǁ__init____mutmut_4": xǁTARǁ__init____mutmut_4,
        "xǁTARǁ__init____mutmut_5": xǁTARǁ__init____mutmut_5,
        "xǁTARǁ__init____mutmut_6": xǁTARǁ__init____mutmut_6,
        "xǁTARǁ__init____mutmut_7": xǁTARǁ__init____mutmut_7,
        "xǁTARǁ__init____mutmut_8": xǁTARǁ__init____mutmut_8,
        "xǁTARǁ__init____mutmut_9": xǁTARǁ__init____mutmut_9,
        "xǁTARǁ__init____mutmut_10": xǁTARǁ__init____mutmut_10,
        "xǁTARǁ__init____mutmut_11": xǁTARǁ__init____mutmut_11,
        "xǁTARǁ__init____mutmut_12": xǁTARǁ__init____mutmut_12,
        "xǁTARǁ__init____mutmut_13": xǁTARǁ__init____mutmut_13,
        "xǁTARǁ__init____mutmut_14": xǁTARǁ__init____mutmut_14,
        "xǁTARǁ__init____mutmut_15": xǁTARǁ__init____mutmut_15,
        "xǁTARǁ__init____mutmut_16": xǁTARǁ__init____mutmut_16,
        "xǁTARǁ__init____mutmut_17": xǁTARǁ__init____mutmut_17,
        "xǁTARǁ__init____mutmut_18": xǁTARǁ__init____mutmut_18,
        "xǁTARǁ__init____mutmut_19": xǁTARǁ__init____mutmut_19,
        "xǁTARǁ__init____mutmut_20": xǁTARǁ__init____mutmut_20,
        "xǁTARǁ__init____mutmut_21": xǁTARǁ__init____mutmut_21,
        "xǁTARǁ__init____mutmut_22": xǁTARǁ__init____mutmut_22,
        "xǁTARǁ__init____mutmut_23": xǁTARǁ__init____mutmut_23,
        "xǁTARǁ__init____mutmut_24": xǁTARǁ__init____mutmut_24,
        "xǁTARǁ__init____mutmut_25": xǁTARǁ__init____mutmut_25,
        "xǁTARǁ__init____mutmut_26": xǁTARǁ__init____mutmut_26,
        "xǁTARǁ__init____mutmut_27": xǁTARǁ__init____mutmut_27,
        "xǁTARǁ__init____mutmut_28": xǁTARǁ__init____mutmut_28,
        "xǁTARǁ__init____mutmut_29": xǁTARǁ__init____mutmut_29,
        "xǁTARǁ__init____mutmut_30": xǁTARǁ__init____mutmut_30,
    }
    xǁTARǁ__init____mutmut_orig.__name__ = "xǁTARǁ__init__"

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        args = [s, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁTARǁ_transition_function__mutmut_orig"),
            object.__getattribute__(self, "xǁTARǁ_transition_function__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁTARǁ_transition_function__mutmut_orig(
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

    def xǁTARǁ_transition_function__mutmut_1(
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
        c = None
        return (s > c).astype(np.float64)

    def xǁTARǁ_transition_function__mutmut_2(
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
        c = params[1]
        return (s > c).astype(np.float64)

    def xǁTARǁ_transition_function__mutmut_3(
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
        return (s > c).astype(None)

    def xǁTARǁ_transition_function__mutmut_4(
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
        return (s >= c).astype(np.float64)

    xǁTARǁ_transition_function__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁTARǁ_transition_function__mutmut_1": xǁTARǁ_transition_function__mutmut_1,
        "xǁTARǁ_transition_function__mutmut_2": xǁTARǁ_transition_function__mutmut_2,
        "xǁTARǁ_transition_function__mutmut_3": xǁTARǁ_transition_function__mutmut_3,
        "xǁTARǁ_transition_function__mutmut_4": xǁTARǁ_transition_function__mutmut_4,
    }
    xǁTARǁ_transition_function__mutmut_orig.__name__ = "xǁTARǁ_transition_function"

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
        args = [s, y, x_mat, grid_points]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁTARǁ_estimate_threshold__mutmut_orig"),
            object.__getattribute__(self, "xǁTARǁ_estimate_threshold__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁTARǁ_estimate_threshold__mutmut_orig(
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

    def xǁTARǁ_estimate_threshold__mutmut_1(
        self,
        s: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        grid_points: int = 301,
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

    def xǁTARǁ_estimate_threshold__mutmut_2(
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
        s_sorted = None
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

    def xǁTARǁ_estimate_threshold__mutmut_3(
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
        s_sorted = np.sort(None)
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

    def xǁTARǁ_estimate_threshold__mutmut_4(
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
        n = None
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

    def xǁTARǁ_estimate_threshold__mutmut_5(
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
        lo = None
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

    def xǁTARǁ_estimate_threshold__mutmut_6(
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
        lo = int(None)
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

    def xǁTARǁ_estimate_threshold__mutmut_7(
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
        lo = int(0.15 / n)
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

    def xǁTARǁ_estimate_threshold__mutmut_8(
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
        lo = int(1.15 * n)
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

    def xǁTARǁ_estimate_threshold__mutmut_9(
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
        hi = None
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

    def xǁTARǁ_estimate_threshold__mutmut_10(
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
        hi = int(None)
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

    def xǁTARǁ_estimate_threshold__mutmut_11(
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
        hi = int(0.85 / n)
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

    def xǁTARǁ_estimate_threshold__mutmut_12(
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
        hi = int(1.85 * n)
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

    def xǁTARǁ_estimate_threshold__mutmut_13(
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
        if lo > hi:
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

    def xǁTARǁ_estimate_threshold__mutmut_14(
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
            lo = None
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

    def xǁTARǁ_estimate_threshold__mutmut_15(
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
            lo = 1
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

    def xǁTARǁ_estimate_threshold__mutmut_16(
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
            hi = None
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

    def xǁTARǁ_estimate_threshold__mutmut_17(
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
            hi = n + 1
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

    def xǁTARǁ_estimate_threshold__mutmut_18(
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
            hi = n - 2
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

    def xǁTARǁ_estimate_threshold__mutmut_19(
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
        candidates = None

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

    def xǁTARǁ_estimate_threshold__mutmut_20(
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
        candidates = np.linspace(None, s_sorted[hi], grid_points)

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

    def xǁTARǁ_estimate_threshold__mutmut_21(
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
        candidates = np.linspace(s_sorted[lo], None, grid_points)

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

    def xǁTARǁ_estimate_threshold__mutmut_22(
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
        candidates = np.linspace(s_sorted[lo], s_sorted[hi], None)

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

    def xǁTARǁ_estimate_threshold__mutmut_23(
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
        candidates = np.linspace(s_sorted[hi], grid_points)

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

    def xǁTARǁ_estimate_threshold__mutmut_24(
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
        candidates = np.linspace(s_sorted[lo], grid_points)

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

    def xǁTARǁ_estimate_threshold__mutmut_25(
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
        candidates = np.linspace(
            s_sorted[lo],
            s_sorted[hi],
        )

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

    def xǁTARǁ_estimate_threshold__mutmut_26(
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

        min_obs = None  # minimum observations per regime

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

    def xǁTARǁ_estimate_threshold__mutmut_27(
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

        min_obs = self.order - 2  # minimum observations per regime

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

    def xǁTARǁ_estimate_threshold__mutmut_28(
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

        min_obs = self.order + 3  # minimum observations per regime

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

    def xǁTARǁ_estimate_threshold__mutmut_29(
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

        best_rss = None
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

    def xǁTARǁ_estimate_threshold__mutmut_30(
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
        best_c = None

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

    def xǁTARǁ_estimate_threshold__mutmut_31(
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
        best_c = float(None)

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

    def xǁTARǁ_estimate_threshold__mutmut_32(
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
        best_c = float(np.median(None))

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

    def xǁTARǁ_estimate_threshold__mutmut_33(
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
            mask1 = None
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

    def xǁTARǁ_estimate_threshold__mutmut_34(
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
            mask1 = s < c_val
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

    def xǁTARǁ_estimate_threshold__mutmut_35(
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
            mask2 = None
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

    def xǁTARǁ_estimate_threshold__mutmut_36(
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
            mask2 = s >= c_val
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

    def xǁTARǁ_estimate_threshold__mutmut_37(
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
            n1 = None
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

    def xǁTARǁ_estimate_threshold__mutmut_38(
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
            n2 = None
            if n1 < min_obs or n2 < min_obs:
                continue
            rss1 = self._ols_rss(y[mask1], x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_39(
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
            if n1 < min_obs and n2 < min_obs:
                continue
            rss1 = self._ols_rss(y[mask1], x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_40(
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
            if n1 <= min_obs or n2 < min_obs:
                continue
            rss1 = self._ols_rss(y[mask1], x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_41(
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
            if n1 < min_obs or n2 <= min_obs:
                continue
            rss1 = self._ols_rss(y[mask1], x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_42(
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
                break
            rss1 = self._ols_rss(y[mask1], x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_43(
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
            rss1 = None
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_44(
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
            rss1 = self._ols_rss(None, x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_45(
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
            rss1 = self._ols_rss(y[mask1], None)
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_46(
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
            rss1 = self._ols_rss(x_mat[mask1])
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_47(
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
            rss1 = self._ols_rss(
                y[mask1],
            )
            rss2 = self._ols_rss(y[mask2], x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_48(
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
            rss2 = None
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_49(
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
            rss2 = self._ols_rss(None, x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_50(
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
            rss2 = self._ols_rss(y[mask2], None)
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_51(
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
            rss2 = self._ols_rss(x_mat[mask2])
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_52(
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
            rss2 = self._ols_rss(
                y[mask2],
            )
            rss = rss1 + rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_53(
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
            rss = None
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_54(
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
            rss = rss1 - rss2
            if rss < best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_55(
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
            if rss <= best_rss:
                best_rss = rss
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_56(
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
                best_rss = None
                best_c = float(c_val)

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_57(
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
                best_c = None

        return best_c, best_rss

    def xǁTARǁ_estimate_threshold__mutmut_58(
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
                best_c = float(None)

        return best_c, best_rss

    xǁTARǁ_estimate_threshold__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁTARǁ_estimate_threshold__mutmut_1": xǁTARǁ_estimate_threshold__mutmut_1,
        "xǁTARǁ_estimate_threshold__mutmut_2": xǁTARǁ_estimate_threshold__mutmut_2,
        "xǁTARǁ_estimate_threshold__mutmut_3": xǁTARǁ_estimate_threshold__mutmut_3,
        "xǁTARǁ_estimate_threshold__mutmut_4": xǁTARǁ_estimate_threshold__mutmut_4,
        "xǁTARǁ_estimate_threshold__mutmut_5": xǁTARǁ_estimate_threshold__mutmut_5,
        "xǁTARǁ_estimate_threshold__mutmut_6": xǁTARǁ_estimate_threshold__mutmut_6,
        "xǁTARǁ_estimate_threshold__mutmut_7": xǁTARǁ_estimate_threshold__mutmut_7,
        "xǁTARǁ_estimate_threshold__mutmut_8": xǁTARǁ_estimate_threshold__mutmut_8,
        "xǁTARǁ_estimate_threshold__mutmut_9": xǁTARǁ_estimate_threshold__mutmut_9,
        "xǁTARǁ_estimate_threshold__mutmut_10": xǁTARǁ_estimate_threshold__mutmut_10,
        "xǁTARǁ_estimate_threshold__mutmut_11": xǁTARǁ_estimate_threshold__mutmut_11,
        "xǁTARǁ_estimate_threshold__mutmut_12": xǁTARǁ_estimate_threshold__mutmut_12,
        "xǁTARǁ_estimate_threshold__mutmut_13": xǁTARǁ_estimate_threshold__mutmut_13,
        "xǁTARǁ_estimate_threshold__mutmut_14": xǁTARǁ_estimate_threshold__mutmut_14,
        "xǁTARǁ_estimate_threshold__mutmut_15": xǁTARǁ_estimate_threshold__mutmut_15,
        "xǁTARǁ_estimate_threshold__mutmut_16": xǁTARǁ_estimate_threshold__mutmut_16,
        "xǁTARǁ_estimate_threshold__mutmut_17": xǁTARǁ_estimate_threshold__mutmut_17,
        "xǁTARǁ_estimate_threshold__mutmut_18": xǁTARǁ_estimate_threshold__mutmut_18,
        "xǁTARǁ_estimate_threshold__mutmut_19": xǁTARǁ_estimate_threshold__mutmut_19,
        "xǁTARǁ_estimate_threshold__mutmut_20": xǁTARǁ_estimate_threshold__mutmut_20,
        "xǁTARǁ_estimate_threshold__mutmut_21": xǁTARǁ_estimate_threshold__mutmut_21,
        "xǁTARǁ_estimate_threshold__mutmut_22": xǁTARǁ_estimate_threshold__mutmut_22,
        "xǁTARǁ_estimate_threshold__mutmut_23": xǁTARǁ_estimate_threshold__mutmut_23,
        "xǁTARǁ_estimate_threshold__mutmut_24": xǁTARǁ_estimate_threshold__mutmut_24,
        "xǁTARǁ_estimate_threshold__mutmut_25": xǁTARǁ_estimate_threshold__mutmut_25,
        "xǁTARǁ_estimate_threshold__mutmut_26": xǁTARǁ_estimate_threshold__mutmut_26,
        "xǁTARǁ_estimate_threshold__mutmut_27": xǁTARǁ_estimate_threshold__mutmut_27,
        "xǁTARǁ_estimate_threshold__mutmut_28": xǁTARǁ_estimate_threshold__mutmut_28,
        "xǁTARǁ_estimate_threshold__mutmut_29": xǁTARǁ_estimate_threshold__mutmut_29,
        "xǁTARǁ_estimate_threshold__mutmut_30": xǁTARǁ_estimate_threshold__mutmut_30,
        "xǁTARǁ_estimate_threshold__mutmut_31": xǁTARǁ_estimate_threshold__mutmut_31,
        "xǁTARǁ_estimate_threshold__mutmut_32": xǁTARǁ_estimate_threshold__mutmut_32,
        "xǁTARǁ_estimate_threshold__mutmut_33": xǁTARǁ_estimate_threshold__mutmut_33,
        "xǁTARǁ_estimate_threshold__mutmut_34": xǁTARǁ_estimate_threshold__mutmut_34,
        "xǁTARǁ_estimate_threshold__mutmut_35": xǁTARǁ_estimate_threshold__mutmut_35,
        "xǁTARǁ_estimate_threshold__mutmut_36": xǁTARǁ_estimate_threshold__mutmut_36,
        "xǁTARǁ_estimate_threshold__mutmut_37": xǁTARǁ_estimate_threshold__mutmut_37,
        "xǁTARǁ_estimate_threshold__mutmut_38": xǁTARǁ_estimate_threshold__mutmut_38,
        "xǁTARǁ_estimate_threshold__mutmut_39": xǁTARǁ_estimate_threshold__mutmut_39,
        "xǁTARǁ_estimate_threshold__mutmut_40": xǁTARǁ_estimate_threshold__mutmut_40,
        "xǁTARǁ_estimate_threshold__mutmut_41": xǁTARǁ_estimate_threshold__mutmut_41,
        "xǁTARǁ_estimate_threshold__mutmut_42": xǁTARǁ_estimate_threshold__mutmut_42,
        "xǁTARǁ_estimate_threshold__mutmut_43": xǁTARǁ_estimate_threshold__mutmut_43,
        "xǁTARǁ_estimate_threshold__mutmut_44": xǁTARǁ_estimate_threshold__mutmut_44,
        "xǁTARǁ_estimate_threshold__mutmut_45": xǁTARǁ_estimate_threshold__mutmut_45,
        "xǁTARǁ_estimate_threshold__mutmut_46": xǁTARǁ_estimate_threshold__mutmut_46,
        "xǁTARǁ_estimate_threshold__mutmut_47": xǁTARǁ_estimate_threshold__mutmut_47,
        "xǁTARǁ_estimate_threshold__mutmut_48": xǁTARǁ_estimate_threshold__mutmut_48,
        "xǁTARǁ_estimate_threshold__mutmut_49": xǁTARǁ_estimate_threshold__mutmut_49,
        "xǁTARǁ_estimate_threshold__mutmut_50": xǁTARǁ_estimate_threshold__mutmut_50,
        "xǁTARǁ_estimate_threshold__mutmut_51": xǁTARǁ_estimate_threshold__mutmut_51,
        "xǁTARǁ_estimate_threshold__mutmut_52": xǁTARǁ_estimate_threshold__mutmut_52,
        "xǁTARǁ_estimate_threshold__mutmut_53": xǁTARǁ_estimate_threshold__mutmut_53,
        "xǁTARǁ_estimate_threshold__mutmut_54": xǁTARǁ_estimate_threshold__mutmut_54,
        "xǁTARǁ_estimate_threshold__mutmut_55": xǁTARǁ_estimate_threshold__mutmut_55,
        "xǁTARǁ_estimate_threshold__mutmut_56": xǁTARǁ_estimate_threshold__mutmut_56,
        "xǁTARǁ_estimate_threshold__mutmut_57": xǁTARǁ_estimate_threshold__mutmut_57,
        "xǁTARǁ_estimate_threshold__mutmut_58": xǁTARǁ_estimate_threshold__mutmut_58,
    }
    xǁTARǁ_estimate_threshold__mutmut_orig.__name__ = "xǁTARǁ_estimate_threshold"

    def _fit_cls(self) -> ThresholdResults:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁTARǁ_fit_cls__mutmut_orig"),
            object.__getattribute__(self, "xǁTARǁ_fit_cls__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁTARǁ_fit_cls__mutmut_orig(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_1(self) -> ThresholdResults:
        """Fit TAR model via Conditional Least Squares.

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        y = None
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

    def xǁTARǁ_fit_cls__mutmut_2(self) -> ThresholdResults:
        """Fit TAR model via Conditional Least Squares.

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        y = self._y
        x_mat = None
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

    def xǁTARǁ_fit_cls__mutmut_3(self) -> ThresholdResults:
        """Fit TAR model via Conditional Least Squares.

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        y = self._y
        x_mat = self._X
        s = None

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

    def xǁTARǁ_fit_cls__mutmut_4(self) -> ThresholdResults:
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
        best_c, _ = None

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

    def xǁTARǁ_fit_cls__mutmut_5(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(None, y, x_mat, self.grid_points)

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

    def xǁTARǁ_fit_cls__mutmut_6(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(s, None, x_mat, self.grid_points)

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

    def xǁTARǁ_fit_cls__mutmut_7(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(s, y, None, self.grid_points)

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

    def xǁTARǁ_fit_cls__mutmut_8(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(s, y, x_mat, None)

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

    def xǁTARǁ_fit_cls__mutmut_9(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(y, x_mat, self.grid_points)

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

    def xǁTARǁ_fit_cls__mutmut_10(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(s, x_mat, self.grid_points)

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

    def xǁTARǁ_fit_cls__mutmut_11(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(s, y, self.grid_points)

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

    def xǁTARǁ_fit_cls__mutmut_12(self) -> ThresholdResults:
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
        best_c, _ = self._estimate_threshold(
            s,
            y,
            x_mat,
        )

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

    def xǁTARǁ_fit_cls__mutmut_13(self) -> ThresholdResults:
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
        mask1 = None
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

    def xǁTARǁ_fit_cls__mutmut_14(self) -> ThresholdResults:
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
        mask1 = s < best_c
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

    def xǁTARǁ_fit_cls__mutmut_15(self) -> ThresholdResults:
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
        mask2 = None

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

    def xǁTARǁ_fit_cls__mutmut_16(self) -> ThresholdResults:
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
        mask2 = s >= best_c

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

    def xǁTARǁ_fit_cls__mutmut_17(self) -> ThresholdResults:
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
        beta1, resid1, rss1 = None
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

    def xǁTARǁ_fit_cls__mutmut_18(self) -> ThresholdResults:
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
        beta1, resid1, rss1 = self._ols_fit(None, x_mat[mask1])
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

    def xǁTARǁ_fit_cls__mutmut_19(self) -> ThresholdResults:
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
        beta1, resid1, rss1 = self._ols_fit(y[mask1], None)
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

    def xǁTARǁ_fit_cls__mutmut_20(self) -> ThresholdResults:
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
        beta1, resid1, rss1 = self._ols_fit(x_mat[mask1])
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

    def xǁTARǁ_fit_cls__mutmut_21(self) -> ThresholdResults:
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
        beta1, resid1, rss1 = self._ols_fit(
            y[mask1],
        )
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

    def xǁTARǁ_fit_cls__mutmut_22(self) -> ThresholdResults:
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
        beta2, resid2, rss2 = None

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

    def xǁTARǁ_fit_cls__mutmut_23(self) -> ThresholdResults:
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
        beta2, resid2, rss2 = self._ols_fit(None, x_mat[mask2])

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

    def xǁTARǁ_fit_cls__mutmut_24(self) -> ThresholdResults:
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
        beta2, resid2, rss2 = self._ols_fit(y[mask2], None)

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

    def xǁTARǁ_fit_cls__mutmut_25(self) -> ThresholdResults:
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
        beta2, resid2, rss2 = self._ols_fit(x_mat[mask2])

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

    def xǁTARǁ_fit_cls__mutmut_26(self) -> ThresholdResults:
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
        beta2, resid2, rss2 = self._ols_fit(
            y[mask2],
        )

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

    def xǁTARǁ_fit_cls__mutmut_27(self) -> ThresholdResults:
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

        n1 = None
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

    def xǁTARǁ_fit_cls__mutmut_28(self) -> ThresholdResults:
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
        n2 = None
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

    def xǁTARǁ_fit_cls__mutmut_29(self) -> ThresholdResults:
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
        sigma2_1 = None
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

    def xǁTARǁ_fit_cls__mutmut_30(self) -> ThresholdResults:
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
        sigma2_1 = rss1 * n1 if n1 > 0 else 0.0
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

    def xǁTARǁ_fit_cls__mutmut_31(self) -> ThresholdResults:
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
        sigma2_1 = rss1 / n1 if n1 >= 0 else 0.0
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

    def xǁTARǁ_fit_cls__mutmut_32(self) -> ThresholdResults:
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
        sigma2_1 = rss1 / n1 if n1 > 1 else 0.0
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

    def xǁTARǁ_fit_cls__mutmut_33(self) -> ThresholdResults:
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
        sigma2_1 = rss1 / n1 if n1 > 0 else 1.0
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

    def xǁTARǁ_fit_cls__mutmut_34(self) -> ThresholdResults:
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
        sigma2_2 = None

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

    def xǁTARǁ_fit_cls__mutmut_35(self) -> ThresholdResults:
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
        sigma2_2 = rss2 * n2 if n2 > 0 else 0.0

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

    def xǁTARǁ_fit_cls__mutmut_36(self) -> ThresholdResults:
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
        sigma2_2 = rss2 / n2 if n2 >= 0 else 0.0

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

    def xǁTARǁ_fit_cls__mutmut_37(self) -> ThresholdResults:
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
        sigma2_2 = rss2 / n2 if n2 > 1 else 0.0

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

    def xǁTARǁ_fit_cls__mutmut_38(self) -> ThresholdResults:
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
        sigma2_2 = rss2 / n2 if n2 > 0 else 1.0

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

    def xǁTARǁ_fit_cls__mutmut_39(self) -> ThresholdResults:
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
        resid = None
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

    def xǁTARǁ_fit_cls__mutmut_40(self) -> ThresholdResults:
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
        resid = np.empty(None)
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

    def xǁTARǁ_fit_cls__mutmut_41(self) -> ThresholdResults:
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
        resid[mask1] = None
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

    def xǁTARǁ_fit_cls__mutmut_42(self) -> ThresholdResults:
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
        resid[mask2] = None

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

    def xǁTARǁ_fit_cls__mutmut_43(self) -> ThresholdResults:
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
        g_values = None

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

    def xǁTARǁ_fit_cls__mutmut_44(self) -> ThresholdResults:
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
        g_values = mask2.astype(None)

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

    def xǁTARǁ_fit_cls__mutmut_45(self) -> ThresholdResults:
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
        t_eff = None
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

    def xǁTARǁ_fit_cls__mutmut_46(self) -> ThresholdResults:
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
        ll = None
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

    def xǁTARǁ_fit_cls__mutmut_47(self) -> ThresholdResults:
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
        ll = 1.0
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

    def xǁTARǁ_fit_cls__mutmut_48(self) -> ThresholdResults:
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
        if n1 > 0 or sigma2_1 > 0:
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

    def xǁTARǁ_fit_cls__mutmut_49(self) -> ThresholdResults:
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
        if n1 >= 0 and sigma2_1 > 0:
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

    def xǁTARǁ_fit_cls__mutmut_50(self) -> ThresholdResults:
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
        if n1 > 1 and sigma2_1 > 0:
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

    def xǁTARǁ_fit_cls__mutmut_51(self) -> ThresholdResults:
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
        if n1 > 0 and sigma2_1 >= 0:
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

    def xǁTARǁ_fit_cls__mutmut_52(self) -> ThresholdResults:
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
        if n1 > 0 and sigma2_1 > 1:
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

    def xǁTARǁ_fit_cls__mutmut_53(self) -> ThresholdResults:
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
            ll = -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_54(self) -> ThresholdResults:
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
            ll -= -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_55(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) + rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_56(self) -> ThresholdResults:
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
            ll += -0.5 * n1 / (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_57(self) -> ThresholdResults:
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
            ll += -0.5 / n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_58(self) -> ThresholdResults:
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
            ll += +0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_59(self) -> ThresholdResults:
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
            ll += -1.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_60(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(2 * np.pi) - np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_61(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(None) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_62(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(2 / np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_63(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(3 * np.pi) + np.log(sigma2_1)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_64(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(2 * np.pi) + np.log(None)) - rss1 / (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_65(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 * (2 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_66(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (2 / sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_67(self) -> ThresholdResults:
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
            ll += -0.5 * n1 * (np.log(2 * np.pi) + np.log(sigma2_1)) - rss1 / (3 * sigma2_1)
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

    def xǁTARǁ_fit_cls__mutmut_68(self) -> ThresholdResults:
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
        if n2 > 0 or sigma2_2 > 0:
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

    def xǁTARǁ_fit_cls__mutmut_69(self) -> ThresholdResults:
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
        if n2 >= 0 and sigma2_2 > 0:
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

    def xǁTARǁ_fit_cls__mutmut_70(self) -> ThresholdResults:
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
        if n2 > 1 and sigma2_2 > 0:
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

    def xǁTARǁ_fit_cls__mutmut_71(self) -> ThresholdResults:
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
        if n2 > 0 and sigma2_2 >= 0:
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

    def xǁTARǁ_fit_cls__mutmut_72(self) -> ThresholdResults:
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
        if n2 > 0 and sigma2_2 > 1:
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

    def xǁTARǁ_fit_cls__mutmut_73(self) -> ThresholdResults:
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
            ll = -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_74(self) -> ThresholdResults:
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
            ll -= -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_75(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) + rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_76(self) -> ThresholdResults:
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
            ll += -0.5 * n2 / (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_77(self) -> ThresholdResults:
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
            ll += -0.5 / n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_78(self) -> ThresholdResults:
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
            ll += +0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_79(self) -> ThresholdResults:
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
            ll += -1.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_80(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(2 * np.pi) - np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_81(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(None) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_82(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(2 / np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_83(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(3 * np.pi) + np.log(sigma2_2)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_84(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(2 * np.pi) + np.log(None)) - rss2 / (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_85(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 * (2 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_86(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (2 / sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_87(self) -> ThresholdResults:
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
            ll += -0.5 * n2 * (np.log(2 * np.pi) + np.log(sigma2_2)) - rss2 / (3 * sigma2_2)

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

    def xǁTARǁ_fit_cls__mutmut_88(self) -> ThresholdResults:
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
        n_params = None
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

    def xǁTARǁ_fit_cls__mutmut_89(self) -> ThresholdResults:
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
        n_params = (self.order + 1) * 2 - 1
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

    def xǁTARǁ_fit_cls__mutmut_90(self) -> ThresholdResults:
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
        n_params = (self.order + 1) / 2 + 1
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

    def xǁTARǁ_fit_cls__mutmut_91(self) -> ThresholdResults:
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
        n_params = (self.order - 1) * 2 + 1
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

    def xǁTARǁ_fit_cls__mutmut_92(self) -> ThresholdResults:
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
        n_params = (self.order + 2) * 2 + 1
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

    def xǁTARǁ_fit_cls__mutmut_93(self) -> ThresholdResults:
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
        n_params = (self.order + 1) * 3 + 1
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

    def xǁTARǁ_fit_cls__mutmut_94(self) -> ThresholdResults:
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
        n_params = (self.order + 1) * 2 + 2
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

    def xǁTARǁ_fit_cls__mutmut_95(self) -> ThresholdResults:
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
        aic = None
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

    def xǁTARǁ_fit_cls__mutmut_96(self) -> ThresholdResults:
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
        aic = -2 * ll - 2 * n_params
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

    def xǁTARǁ_fit_cls__mutmut_97(self) -> ThresholdResults:
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
        aic = -2 / ll + 2 * n_params
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

    def xǁTARǁ_fit_cls__mutmut_98(self) -> ThresholdResults:
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
        aic = +2 * ll + 2 * n_params
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

    def xǁTARǁ_fit_cls__mutmut_99(self) -> ThresholdResults:
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
        aic = -3 * ll + 2 * n_params
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

    def xǁTARǁ_fit_cls__mutmut_100(self) -> ThresholdResults:
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
        aic = -2 * ll + 2 / n_params
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

    def xǁTARǁ_fit_cls__mutmut_101(self) -> ThresholdResults:
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
        aic = -2 * ll + 3 * n_params
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

    def xǁTARǁ_fit_cls__mutmut_102(self) -> ThresholdResults:
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
        bic = None

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

    def xǁTARǁ_fit_cls__mutmut_103(self) -> ThresholdResults:
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
        bic = -2 * ll - np.log(t_eff) * n_params

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

    def xǁTARǁ_fit_cls__mutmut_104(self) -> ThresholdResults:
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
        bic = -2 / ll + np.log(t_eff) * n_params

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

    def xǁTARǁ_fit_cls__mutmut_105(self) -> ThresholdResults:
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
        bic = +2 * ll + np.log(t_eff) * n_params

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

    def xǁTARǁ_fit_cls__mutmut_106(self) -> ThresholdResults:
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
        bic = -3 * ll + np.log(t_eff) * n_params

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

    def xǁTARǁ_fit_cls__mutmut_107(self) -> ThresholdResults:
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
        bic = -2 * ll + np.log(t_eff) / n_params

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

    def xǁTARǁ_fit_cls__mutmut_108(self) -> ThresholdResults:
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
        bic = -2 * ll + np.log(None) * n_params

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

    def xǁTARǁ_fit_cls__mutmut_109(self) -> ThresholdResults:
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
            model_name=None,
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

    def xǁTARǁ_fit_cls__mutmut_110(self) -> ThresholdResults:
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
            params=None,
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

    def xǁTARǁ_fit_cls__mutmut_111(self) -> ThresholdResults:
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
            threshold=None,
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

    def xǁTARǁ_fit_cls__mutmut_112(self) -> ThresholdResults:
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
            delay=None,
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

    def xǁTARǁ_fit_cls__mutmut_113(self) -> ThresholdResults:
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
            transition_params=None,
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

    def xǁTARǁ_fit_cls__mutmut_114(self) -> ThresholdResults:
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
            transition_params_array=None,
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

    def xǁTARǁ_fit_cls__mutmut_115(self) -> ThresholdResults:
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
            params_regime1=None,
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

    def xǁTARǁ_fit_cls__mutmut_116(self) -> ThresholdResults:
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
            params_regime2=None,
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

    def xǁTARǁ_fit_cls__mutmut_117(self) -> ThresholdResults:
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
            regime_assignments=None,
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

    def xǁTARǁ_fit_cls__mutmut_118(self) -> ThresholdResults:
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
            transition_values=None,
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

    def xǁTARǁ_fit_cls__mutmut_119(self) -> ThresholdResults:
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
            resid=None,
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

    def xǁTARǁ_fit_cls__mutmut_120(self) -> ThresholdResults:
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
            sigma2=None,
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_121(self) -> ThresholdResults:
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
            loglike=None,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_122(self) -> ThresholdResults:
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
            aic=None,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_123(self) -> ThresholdResults:
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
            bic=None,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_124(self) -> ThresholdResults:
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
            nobs=None,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_125(self) -> ThresholdResults:
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
            order=None,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_126(self) -> ThresholdResults:
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
            n_regimes=None,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_127(self) -> ThresholdResults:
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
            endog=None,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_128(self) -> ThresholdResults:
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
            _model=None,
        )

    def xǁTARǁ_fit_cls__mutmut_129(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_130(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_131(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_132(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_133(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_134(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_135(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_136(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_137(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_138(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_139(self) -> ThresholdResults:
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

    def xǁTARǁ_fit_cls__mutmut_140(self) -> ThresholdResults:
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
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_141(self) -> ThresholdResults:
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
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_142(self) -> ThresholdResults:
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
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_143(self) -> ThresholdResults:
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
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_144(self) -> ThresholdResults:
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
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_145(self) -> ThresholdResults:
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
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_146(self) -> ThresholdResults:
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
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_147(self) -> ThresholdResults:
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
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_148(self) -> ThresholdResults:
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
        )

    def xǁTARǁ_fit_cls__mutmut_149(self) -> ThresholdResults:
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
            params={"XXregime_1XX": beta1, "regime_2": beta2},
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

    def xǁTARǁ_fit_cls__mutmut_150(self) -> ThresholdResults:
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
            params={"REGIME_1": beta1, "regime_2": beta2},
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

    def xǁTARǁ_fit_cls__mutmut_151(self) -> ThresholdResults:
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
            params={"regime_1": beta1, "XXregime_2XX": beta2},
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

    def xǁTARǁ_fit_cls__mutmut_152(self) -> ThresholdResults:
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
            params={"regime_1": beta1, "REGIME_2": beta2},
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

    def xǁTARǁ_fit_cls__mutmut_153(self) -> ThresholdResults:
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
            transition_params={"XXcXX": best_c},
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

    def xǁTARǁ_fit_cls__mutmut_154(self) -> ThresholdResults:
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
            transition_params={"C": best_c},
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

    def xǁTARǁ_fit_cls__mutmut_155(self) -> ThresholdResults:
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
            transition_params_array=np.array(None),
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

    def xǁTARǁ_fit_cls__mutmut_156(self) -> ThresholdResults:
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
            sigma2={"XXregime_1XX": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_157(self) -> ThresholdResults:
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
            sigma2={"REGIME_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_158(self) -> ThresholdResults:
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
            sigma2={"regime_1": sigma2_1, "XXregime_2XX": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁTARǁ_fit_cls__mutmut_159(self) -> ThresholdResults:
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
            sigma2={"regime_1": sigma2_1, "REGIME_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    xǁTARǁ_fit_cls__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁTARǁ_fit_cls__mutmut_1": xǁTARǁ_fit_cls__mutmut_1,
        "xǁTARǁ_fit_cls__mutmut_2": xǁTARǁ_fit_cls__mutmut_2,
        "xǁTARǁ_fit_cls__mutmut_3": xǁTARǁ_fit_cls__mutmut_3,
        "xǁTARǁ_fit_cls__mutmut_4": xǁTARǁ_fit_cls__mutmut_4,
        "xǁTARǁ_fit_cls__mutmut_5": xǁTARǁ_fit_cls__mutmut_5,
        "xǁTARǁ_fit_cls__mutmut_6": xǁTARǁ_fit_cls__mutmut_6,
        "xǁTARǁ_fit_cls__mutmut_7": xǁTARǁ_fit_cls__mutmut_7,
        "xǁTARǁ_fit_cls__mutmut_8": xǁTARǁ_fit_cls__mutmut_8,
        "xǁTARǁ_fit_cls__mutmut_9": xǁTARǁ_fit_cls__mutmut_9,
        "xǁTARǁ_fit_cls__mutmut_10": xǁTARǁ_fit_cls__mutmut_10,
        "xǁTARǁ_fit_cls__mutmut_11": xǁTARǁ_fit_cls__mutmut_11,
        "xǁTARǁ_fit_cls__mutmut_12": xǁTARǁ_fit_cls__mutmut_12,
        "xǁTARǁ_fit_cls__mutmut_13": xǁTARǁ_fit_cls__mutmut_13,
        "xǁTARǁ_fit_cls__mutmut_14": xǁTARǁ_fit_cls__mutmut_14,
        "xǁTARǁ_fit_cls__mutmut_15": xǁTARǁ_fit_cls__mutmut_15,
        "xǁTARǁ_fit_cls__mutmut_16": xǁTARǁ_fit_cls__mutmut_16,
        "xǁTARǁ_fit_cls__mutmut_17": xǁTARǁ_fit_cls__mutmut_17,
        "xǁTARǁ_fit_cls__mutmut_18": xǁTARǁ_fit_cls__mutmut_18,
        "xǁTARǁ_fit_cls__mutmut_19": xǁTARǁ_fit_cls__mutmut_19,
        "xǁTARǁ_fit_cls__mutmut_20": xǁTARǁ_fit_cls__mutmut_20,
        "xǁTARǁ_fit_cls__mutmut_21": xǁTARǁ_fit_cls__mutmut_21,
        "xǁTARǁ_fit_cls__mutmut_22": xǁTARǁ_fit_cls__mutmut_22,
        "xǁTARǁ_fit_cls__mutmut_23": xǁTARǁ_fit_cls__mutmut_23,
        "xǁTARǁ_fit_cls__mutmut_24": xǁTARǁ_fit_cls__mutmut_24,
        "xǁTARǁ_fit_cls__mutmut_25": xǁTARǁ_fit_cls__mutmut_25,
        "xǁTARǁ_fit_cls__mutmut_26": xǁTARǁ_fit_cls__mutmut_26,
        "xǁTARǁ_fit_cls__mutmut_27": xǁTARǁ_fit_cls__mutmut_27,
        "xǁTARǁ_fit_cls__mutmut_28": xǁTARǁ_fit_cls__mutmut_28,
        "xǁTARǁ_fit_cls__mutmut_29": xǁTARǁ_fit_cls__mutmut_29,
        "xǁTARǁ_fit_cls__mutmut_30": xǁTARǁ_fit_cls__mutmut_30,
        "xǁTARǁ_fit_cls__mutmut_31": xǁTARǁ_fit_cls__mutmut_31,
        "xǁTARǁ_fit_cls__mutmut_32": xǁTARǁ_fit_cls__mutmut_32,
        "xǁTARǁ_fit_cls__mutmut_33": xǁTARǁ_fit_cls__mutmut_33,
        "xǁTARǁ_fit_cls__mutmut_34": xǁTARǁ_fit_cls__mutmut_34,
        "xǁTARǁ_fit_cls__mutmut_35": xǁTARǁ_fit_cls__mutmut_35,
        "xǁTARǁ_fit_cls__mutmut_36": xǁTARǁ_fit_cls__mutmut_36,
        "xǁTARǁ_fit_cls__mutmut_37": xǁTARǁ_fit_cls__mutmut_37,
        "xǁTARǁ_fit_cls__mutmut_38": xǁTARǁ_fit_cls__mutmut_38,
        "xǁTARǁ_fit_cls__mutmut_39": xǁTARǁ_fit_cls__mutmut_39,
        "xǁTARǁ_fit_cls__mutmut_40": xǁTARǁ_fit_cls__mutmut_40,
        "xǁTARǁ_fit_cls__mutmut_41": xǁTARǁ_fit_cls__mutmut_41,
        "xǁTARǁ_fit_cls__mutmut_42": xǁTARǁ_fit_cls__mutmut_42,
        "xǁTARǁ_fit_cls__mutmut_43": xǁTARǁ_fit_cls__mutmut_43,
        "xǁTARǁ_fit_cls__mutmut_44": xǁTARǁ_fit_cls__mutmut_44,
        "xǁTARǁ_fit_cls__mutmut_45": xǁTARǁ_fit_cls__mutmut_45,
        "xǁTARǁ_fit_cls__mutmut_46": xǁTARǁ_fit_cls__mutmut_46,
        "xǁTARǁ_fit_cls__mutmut_47": xǁTARǁ_fit_cls__mutmut_47,
        "xǁTARǁ_fit_cls__mutmut_48": xǁTARǁ_fit_cls__mutmut_48,
        "xǁTARǁ_fit_cls__mutmut_49": xǁTARǁ_fit_cls__mutmut_49,
        "xǁTARǁ_fit_cls__mutmut_50": xǁTARǁ_fit_cls__mutmut_50,
        "xǁTARǁ_fit_cls__mutmut_51": xǁTARǁ_fit_cls__mutmut_51,
        "xǁTARǁ_fit_cls__mutmut_52": xǁTARǁ_fit_cls__mutmut_52,
        "xǁTARǁ_fit_cls__mutmut_53": xǁTARǁ_fit_cls__mutmut_53,
        "xǁTARǁ_fit_cls__mutmut_54": xǁTARǁ_fit_cls__mutmut_54,
        "xǁTARǁ_fit_cls__mutmut_55": xǁTARǁ_fit_cls__mutmut_55,
        "xǁTARǁ_fit_cls__mutmut_56": xǁTARǁ_fit_cls__mutmut_56,
        "xǁTARǁ_fit_cls__mutmut_57": xǁTARǁ_fit_cls__mutmut_57,
        "xǁTARǁ_fit_cls__mutmut_58": xǁTARǁ_fit_cls__mutmut_58,
        "xǁTARǁ_fit_cls__mutmut_59": xǁTARǁ_fit_cls__mutmut_59,
        "xǁTARǁ_fit_cls__mutmut_60": xǁTARǁ_fit_cls__mutmut_60,
        "xǁTARǁ_fit_cls__mutmut_61": xǁTARǁ_fit_cls__mutmut_61,
        "xǁTARǁ_fit_cls__mutmut_62": xǁTARǁ_fit_cls__mutmut_62,
        "xǁTARǁ_fit_cls__mutmut_63": xǁTARǁ_fit_cls__mutmut_63,
        "xǁTARǁ_fit_cls__mutmut_64": xǁTARǁ_fit_cls__mutmut_64,
        "xǁTARǁ_fit_cls__mutmut_65": xǁTARǁ_fit_cls__mutmut_65,
        "xǁTARǁ_fit_cls__mutmut_66": xǁTARǁ_fit_cls__mutmut_66,
        "xǁTARǁ_fit_cls__mutmut_67": xǁTARǁ_fit_cls__mutmut_67,
        "xǁTARǁ_fit_cls__mutmut_68": xǁTARǁ_fit_cls__mutmut_68,
        "xǁTARǁ_fit_cls__mutmut_69": xǁTARǁ_fit_cls__mutmut_69,
        "xǁTARǁ_fit_cls__mutmut_70": xǁTARǁ_fit_cls__mutmut_70,
        "xǁTARǁ_fit_cls__mutmut_71": xǁTARǁ_fit_cls__mutmut_71,
        "xǁTARǁ_fit_cls__mutmut_72": xǁTARǁ_fit_cls__mutmut_72,
        "xǁTARǁ_fit_cls__mutmut_73": xǁTARǁ_fit_cls__mutmut_73,
        "xǁTARǁ_fit_cls__mutmut_74": xǁTARǁ_fit_cls__mutmut_74,
        "xǁTARǁ_fit_cls__mutmut_75": xǁTARǁ_fit_cls__mutmut_75,
        "xǁTARǁ_fit_cls__mutmut_76": xǁTARǁ_fit_cls__mutmut_76,
        "xǁTARǁ_fit_cls__mutmut_77": xǁTARǁ_fit_cls__mutmut_77,
        "xǁTARǁ_fit_cls__mutmut_78": xǁTARǁ_fit_cls__mutmut_78,
        "xǁTARǁ_fit_cls__mutmut_79": xǁTARǁ_fit_cls__mutmut_79,
        "xǁTARǁ_fit_cls__mutmut_80": xǁTARǁ_fit_cls__mutmut_80,
        "xǁTARǁ_fit_cls__mutmut_81": xǁTARǁ_fit_cls__mutmut_81,
        "xǁTARǁ_fit_cls__mutmut_82": xǁTARǁ_fit_cls__mutmut_82,
        "xǁTARǁ_fit_cls__mutmut_83": xǁTARǁ_fit_cls__mutmut_83,
        "xǁTARǁ_fit_cls__mutmut_84": xǁTARǁ_fit_cls__mutmut_84,
        "xǁTARǁ_fit_cls__mutmut_85": xǁTARǁ_fit_cls__mutmut_85,
        "xǁTARǁ_fit_cls__mutmut_86": xǁTARǁ_fit_cls__mutmut_86,
        "xǁTARǁ_fit_cls__mutmut_87": xǁTARǁ_fit_cls__mutmut_87,
        "xǁTARǁ_fit_cls__mutmut_88": xǁTARǁ_fit_cls__mutmut_88,
        "xǁTARǁ_fit_cls__mutmut_89": xǁTARǁ_fit_cls__mutmut_89,
        "xǁTARǁ_fit_cls__mutmut_90": xǁTARǁ_fit_cls__mutmut_90,
        "xǁTARǁ_fit_cls__mutmut_91": xǁTARǁ_fit_cls__mutmut_91,
        "xǁTARǁ_fit_cls__mutmut_92": xǁTARǁ_fit_cls__mutmut_92,
        "xǁTARǁ_fit_cls__mutmut_93": xǁTARǁ_fit_cls__mutmut_93,
        "xǁTARǁ_fit_cls__mutmut_94": xǁTARǁ_fit_cls__mutmut_94,
        "xǁTARǁ_fit_cls__mutmut_95": xǁTARǁ_fit_cls__mutmut_95,
        "xǁTARǁ_fit_cls__mutmut_96": xǁTARǁ_fit_cls__mutmut_96,
        "xǁTARǁ_fit_cls__mutmut_97": xǁTARǁ_fit_cls__mutmut_97,
        "xǁTARǁ_fit_cls__mutmut_98": xǁTARǁ_fit_cls__mutmut_98,
        "xǁTARǁ_fit_cls__mutmut_99": xǁTARǁ_fit_cls__mutmut_99,
        "xǁTARǁ_fit_cls__mutmut_100": xǁTARǁ_fit_cls__mutmut_100,
        "xǁTARǁ_fit_cls__mutmut_101": xǁTARǁ_fit_cls__mutmut_101,
        "xǁTARǁ_fit_cls__mutmut_102": xǁTARǁ_fit_cls__mutmut_102,
        "xǁTARǁ_fit_cls__mutmut_103": xǁTARǁ_fit_cls__mutmut_103,
        "xǁTARǁ_fit_cls__mutmut_104": xǁTARǁ_fit_cls__mutmut_104,
        "xǁTARǁ_fit_cls__mutmut_105": xǁTARǁ_fit_cls__mutmut_105,
        "xǁTARǁ_fit_cls__mutmut_106": xǁTARǁ_fit_cls__mutmut_106,
        "xǁTARǁ_fit_cls__mutmut_107": xǁTARǁ_fit_cls__mutmut_107,
        "xǁTARǁ_fit_cls__mutmut_108": xǁTARǁ_fit_cls__mutmut_108,
        "xǁTARǁ_fit_cls__mutmut_109": xǁTARǁ_fit_cls__mutmut_109,
        "xǁTARǁ_fit_cls__mutmut_110": xǁTARǁ_fit_cls__mutmut_110,
        "xǁTARǁ_fit_cls__mutmut_111": xǁTARǁ_fit_cls__mutmut_111,
        "xǁTARǁ_fit_cls__mutmut_112": xǁTARǁ_fit_cls__mutmut_112,
        "xǁTARǁ_fit_cls__mutmut_113": xǁTARǁ_fit_cls__mutmut_113,
        "xǁTARǁ_fit_cls__mutmut_114": xǁTARǁ_fit_cls__mutmut_114,
        "xǁTARǁ_fit_cls__mutmut_115": xǁTARǁ_fit_cls__mutmut_115,
        "xǁTARǁ_fit_cls__mutmut_116": xǁTARǁ_fit_cls__mutmut_116,
        "xǁTARǁ_fit_cls__mutmut_117": xǁTARǁ_fit_cls__mutmut_117,
        "xǁTARǁ_fit_cls__mutmut_118": xǁTARǁ_fit_cls__mutmut_118,
        "xǁTARǁ_fit_cls__mutmut_119": xǁTARǁ_fit_cls__mutmut_119,
        "xǁTARǁ_fit_cls__mutmut_120": xǁTARǁ_fit_cls__mutmut_120,
        "xǁTARǁ_fit_cls__mutmut_121": xǁTARǁ_fit_cls__mutmut_121,
        "xǁTARǁ_fit_cls__mutmut_122": xǁTARǁ_fit_cls__mutmut_122,
        "xǁTARǁ_fit_cls__mutmut_123": xǁTARǁ_fit_cls__mutmut_123,
        "xǁTARǁ_fit_cls__mutmut_124": xǁTARǁ_fit_cls__mutmut_124,
        "xǁTARǁ_fit_cls__mutmut_125": xǁTARǁ_fit_cls__mutmut_125,
        "xǁTARǁ_fit_cls__mutmut_126": xǁTARǁ_fit_cls__mutmut_126,
        "xǁTARǁ_fit_cls__mutmut_127": xǁTARǁ_fit_cls__mutmut_127,
        "xǁTARǁ_fit_cls__mutmut_128": xǁTARǁ_fit_cls__mutmut_128,
        "xǁTARǁ_fit_cls__mutmut_129": xǁTARǁ_fit_cls__mutmut_129,
        "xǁTARǁ_fit_cls__mutmut_130": xǁTARǁ_fit_cls__mutmut_130,
        "xǁTARǁ_fit_cls__mutmut_131": xǁTARǁ_fit_cls__mutmut_131,
        "xǁTARǁ_fit_cls__mutmut_132": xǁTARǁ_fit_cls__mutmut_132,
        "xǁTARǁ_fit_cls__mutmut_133": xǁTARǁ_fit_cls__mutmut_133,
        "xǁTARǁ_fit_cls__mutmut_134": xǁTARǁ_fit_cls__mutmut_134,
        "xǁTARǁ_fit_cls__mutmut_135": xǁTARǁ_fit_cls__mutmut_135,
        "xǁTARǁ_fit_cls__mutmut_136": xǁTARǁ_fit_cls__mutmut_136,
        "xǁTARǁ_fit_cls__mutmut_137": xǁTARǁ_fit_cls__mutmut_137,
        "xǁTARǁ_fit_cls__mutmut_138": xǁTARǁ_fit_cls__mutmut_138,
        "xǁTARǁ_fit_cls__mutmut_139": xǁTARǁ_fit_cls__mutmut_139,
        "xǁTARǁ_fit_cls__mutmut_140": xǁTARǁ_fit_cls__mutmut_140,
        "xǁTARǁ_fit_cls__mutmut_141": xǁTARǁ_fit_cls__mutmut_141,
        "xǁTARǁ_fit_cls__mutmut_142": xǁTARǁ_fit_cls__mutmut_142,
        "xǁTARǁ_fit_cls__mutmut_143": xǁTARǁ_fit_cls__mutmut_143,
        "xǁTARǁ_fit_cls__mutmut_144": xǁTARǁ_fit_cls__mutmut_144,
        "xǁTARǁ_fit_cls__mutmut_145": xǁTARǁ_fit_cls__mutmut_145,
        "xǁTARǁ_fit_cls__mutmut_146": xǁTARǁ_fit_cls__mutmut_146,
        "xǁTARǁ_fit_cls__mutmut_147": xǁTARǁ_fit_cls__mutmut_147,
        "xǁTARǁ_fit_cls__mutmut_148": xǁTARǁ_fit_cls__mutmut_148,
        "xǁTARǁ_fit_cls__mutmut_149": xǁTARǁ_fit_cls__mutmut_149,
        "xǁTARǁ_fit_cls__mutmut_150": xǁTARǁ_fit_cls__mutmut_150,
        "xǁTARǁ_fit_cls__mutmut_151": xǁTARǁ_fit_cls__mutmut_151,
        "xǁTARǁ_fit_cls__mutmut_152": xǁTARǁ_fit_cls__mutmut_152,
        "xǁTARǁ_fit_cls__mutmut_153": xǁTARǁ_fit_cls__mutmut_153,
        "xǁTARǁ_fit_cls__mutmut_154": xǁTARǁ_fit_cls__mutmut_154,
        "xǁTARǁ_fit_cls__mutmut_155": xǁTARǁ_fit_cls__mutmut_155,
        "xǁTARǁ_fit_cls__mutmut_156": xǁTARǁ_fit_cls__mutmut_156,
        "xǁTARǁ_fit_cls__mutmut_157": xǁTARǁ_fit_cls__mutmut_157,
        "xǁTARǁ_fit_cls__mutmut_158": xǁTARǁ_fit_cls__mutmut_158,
        "xǁTARǁ_fit_cls__mutmut_159": xǁTARǁ_fit_cls__mutmut_159,
    }
    xǁTARǁ_fit_cls__mutmut_orig.__name__ = "xǁTARǁ_fit_cls"
