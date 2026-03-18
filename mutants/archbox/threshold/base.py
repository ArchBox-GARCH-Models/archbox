"""Base class for threshold and STAR models.

All threshold models (TAR, SETAR, LSTAR, ESTAR) inherit from ThresholdModel.

References
----------
- Tong, H. (1978). On a Threshold Model.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

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


class ThresholdModel(ABC):
    """Abstract base class for threshold and smooth transition AR models.

    Parameters
    ----------
    endog : array-like
        Endogenous time series (1D).
    order : int
        AR order p.
    delay : int
        Delay parameter d for the transition variable s_t = y_{t-d}.
    n_regimes : int
        Number of regimes (2 or 3).

    Attributes
    ----------
    endog : NDArray[np.float64]
        Endogenous time series.
    nobs : int
        Number of observations.
    order : int
        AR order p.
    delay : int
        Delay parameter d.
    n_regimes : int
        Number of regimes.
    """

    model_name: str = "ThresholdModel"

    def __init__(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        args = [endog, order, delay, n_regimes]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁThresholdModelǁ__init____mutmut_orig(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_1(
        self,
        endog: Any,
        order: int = 2,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_2(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 2,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_3(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 3,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_4(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = None
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_5(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(None, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_6(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=None).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_7(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_8(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(
            endog,
        ).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_9(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = None
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_10(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = None
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_11(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = None
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_12(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = None

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_13(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs <= 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_14(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) - 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_15(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 / (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_16(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 3 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_17(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order - delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_18(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 11:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_19(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = None
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_20(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) - 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_21(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 / (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_22(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {3 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_23(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order - delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_24(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 11}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_25(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(None)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_26(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order <= 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_27(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 2:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_28(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = None
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_29(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(None)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_30(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay <= 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_31(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 2:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_32(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = None
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_33(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(None)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_34(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_35(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (3, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_36(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 4):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_37(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = None
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_38(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(None)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = self._build_matrices()

    def xǁThresholdModelǁ__init____mutmut_39(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        n_regimes: int = 2,
    ) -> None:
        """Initialize threshold model with data and configuration."""
        self.endog = np.asarray(endog, dtype=np.float64).ravel()
        self.nobs = len(self.endog)
        self.order = order
        self.delay = delay
        self.n_regimes = n_regimes

        if self.nobs < 2 * (order + delay) + 10:
            msg = (
                f"Insufficient observations ({self.nobs}) for order={order}, "
                f"delay={delay}. Need at least {2 * (order + delay) + 10}."
            )
            raise ValueError(msg)

        if order < 1:
            msg = f"order must be >= 1, got {order}"
            raise ValueError(msg)

        if delay < 1:
            msg = f"delay must be >= 1, got {delay}"
            raise ValueError(msg)

        if n_regimes not in (2, 3):
            msg = f"n_regimes must be 2 or 3, got {n_regimes}"
            raise ValueError(msg)

        # Build lagged design matrix and transition variable
        self._y, self._X, self._s = None

    xǁThresholdModelǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁ__init____mutmut_1": xǁThresholdModelǁ__init____mutmut_1,
        "xǁThresholdModelǁ__init____mutmut_2": xǁThresholdModelǁ__init____mutmut_2,
        "xǁThresholdModelǁ__init____mutmut_3": xǁThresholdModelǁ__init____mutmut_3,
        "xǁThresholdModelǁ__init____mutmut_4": xǁThresholdModelǁ__init____mutmut_4,
        "xǁThresholdModelǁ__init____mutmut_5": xǁThresholdModelǁ__init____mutmut_5,
        "xǁThresholdModelǁ__init____mutmut_6": xǁThresholdModelǁ__init____mutmut_6,
        "xǁThresholdModelǁ__init____mutmut_7": xǁThresholdModelǁ__init____mutmut_7,
        "xǁThresholdModelǁ__init____mutmut_8": xǁThresholdModelǁ__init____mutmut_8,
        "xǁThresholdModelǁ__init____mutmut_9": xǁThresholdModelǁ__init____mutmut_9,
        "xǁThresholdModelǁ__init____mutmut_10": xǁThresholdModelǁ__init____mutmut_10,
        "xǁThresholdModelǁ__init____mutmut_11": xǁThresholdModelǁ__init____mutmut_11,
        "xǁThresholdModelǁ__init____mutmut_12": xǁThresholdModelǁ__init____mutmut_12,
        "xǁThresholdModelǁ__init____mutmut_13": xǁThresholdModelǁ__init____mutmut_13,
        "xǁThresholdModelǁ__init____mutmut_14": xǁThresholdModelǁ__init____mutmut_14,
        "xǁThresholdModelǁ__init____mutmut_15": xǁThresholdModelǁ__init____mutmut_15,
        "xǁThresholdModelǁ__init____mutmut_16": xǁThresholdModelǁ__init____mutmut_16,
        "xǁThresholdModelǁ__init____mutmut_17": xǁThresholdModelǁ__init____mutmut_17,
        "xǁThresholdModelǁ__init____mutmut_18": xǁThresholdModelǁ__init____mutmut_18,
        "xǁThresholdModelǁ__init____mutmut_19": xǁThresholdModelǁ__init____mutmut_19,
        "xǁThresholdModelǁ__init____mutmut_20": xǁThresholdModelǁ__init____mutmut_20,
        "xǁThresholdModelǁ__init____mutmut_21": xǁThresholdModelǁ__init____mutmut_21,
        "xǁThresholdModelǁ__init____mutmut_22": xǁThresholdModelǁ__init____mutmut_22,
        "xǁThresholdModelǁ__init____mutmut_23": xǁThresholdModelǁ__init____mutmut_23,
        "xǁThresholdModelǁ__init____mutmut_24": xǁThresholdModelǁ__init____mutmut_24,
        "xǁThresholdModelǁ__init____mutmut_25": xǁThresholdModelǁ__init____mutmut_25,
        "xǁThresholdModelǁ__init____mutmut_26": xǁThresholdModelǁ__init____mutmut_26,
        "xǁThresholdModelǁ__init____mutmut_27": xǁThresholdModelǁ__init____mutmut_27,
        "xǁThresholdModelǁ__init____mutmut_28": xǁThresholdModelǁ__init____mutmut_28,
        "xǁThresholdModelǁ__init____mutmut_29": xǁThresholdModelǁ__init____mutmut_29,
        "xǁThresholdModelǁ__init____mutmut_30": xǁThresholdModelǁ__init____mutmut_30,
        "xǁThresholdModelǁ__init____mutmut_31": xǁThresholdModelǁ__init____mutmut_31,
        "xǁThresholdModelǁ__init____mutmut_32": xǁThresholdModelǁ__init____mutmut_32,
        "xǁThresholdModelǁ__init____mutmut_33": xǁThresholdModelǁ__init____mutmut_33,
        "xǁThresholdModelǁ__init____mutmut_34": xǁThresholdModelǁ__init____mutmut_34,
        "xǁThresholdModelǁ__init____mutmut_35": xǁThresholdModelǁ__init____mutmut_35,
        "xǁThresholdModelǁ__init____mutmut_36": xǁThresholdModelǁ__init____mutmut_36,
        "xǁThresholdModelǁ__init____mutmut_37": xǁThresholdModelǁ__init____mutmut_37,
        "xǁThresholdModelǁ__init____mutmut_38": xǁThresholdModelǁ__init____mutmut_38,
        "xǁThresholdModelǁ__init____mutmut_39": xǁThresholdModelǁ__init____mutmut_39,
    }
    xǁThresholdModelǁ__init____mutmut_orig.__name__ = "xǁThresholdModelǁ__init__"

    def _build_matrices(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁ_build_matrices__mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁ_build_matrices__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁThresholdModelǁ_build_matrices__mutmut_orig(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_1(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = None
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_2(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = None
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_3(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = None
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_4(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(None, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_5(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, None)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_6(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_7(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(
            p,
        )
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_8(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = None

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_9(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs + start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_10(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = None
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_11(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = None
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_12(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones(None)
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_13(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p - 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_14(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 2))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_15(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(None, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_16(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, None):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_17(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_18(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(
            1,
        ):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_19(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(2, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_20(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p - 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_21(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 2):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_22(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = None

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_23(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start + lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_24(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs + lag]

        s = self.endog[start - d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_25(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = None

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_26(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start + d : self.nobs - d]

        return y, x_mat, s

    def xǁThresholdModelǁ_build_matrices__mutmut_27(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Build dependent variable, lagged regressors, and transition variable.

        Returns
        -------
        y : ndarray, shape (T_eff,)
            Dependent variable y_t.
        X : ndarray, shape (T_eff, order + 1)
            Design matrix [1, y_{t-1}, ..., y_{t-p}].
        s : ndarray, shape (T_eff,)
            Transition variable s_t = y_{t-d}.
        """
        p = self.order
        d = self.delay
        start = max(p, d)
        t_eff = self.nobs - start

        y = self.endog[start:]
        x_mat = np.ones((t_eff, p + 1))
        for lag in range(1, p + 1):
            x_mat[:, lag] = self.endog[start - lag : self.nobs - lag]

        s = self.endog[start - d : self.nobs + d]

        return y, x_mat, s

    xǁThresholdModelǁ_build_matrices__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁ_build_matrices__mutmut_1": xǁThresholdModelǁ_build_matrices__mutmut_1,
        "xǁThresholdModelǁ_build_matrices__mutmut_2": xǁThresholdModelǁ_build_matrices__mutmut_2,
        "xǁThresholdModelǁ_build_matrices__mutmut_3": xǁThresholdModelǁ_build_matrices__mutmut_3,
        "xǁThresholdModelǁ_build_matrices__mutmut_4": xǁThresholdModelǁ_build_matrices__mutmut_4,
        "xǁThresholdModelǁ_build_matrices__mutmut_5": xǁThresholdModelǁ_build_matrices__mutmut_5,
        "xǁThresholdModelǁ_build_matrices__mutmut_6": xǁThresholdModelǁ_build_matrices__mutmut_6,
        "xǁThresholdModelǁ_build_matrices__mutmut_7": xǁThresholdModelǁ_build_matrices__mutmut_7,
        "xǁThresholdModelǁ_build_matrices__mutmut_8": xǁThresholdModelǁ_build_matrices__mutmut_8,
        "xǁThresholdModelǁ_build_matrices__mutmut_9": xǁThresholdModelǁ_build_matrices__mutmut_9,
        "xǁThresholdModelǁ_build_matrices__mutmut_10": xǁThresholdModelǁ_build_matrices__mutmut_10,
        "xǁThresholdModelǁ_build_matrices__mutmut_11": xǁThresholdModelǁ_build_matrices__mutmut_11,
        "xǁThresholdModelǁ_build_matrices__mutmut_12": xǁThresholdModelǁ_build_matrices__mutmut_12,
        "xǁThresholdModelǁ_build_matrices__mutmut_13": xǁThresholdModelǁ_build_matrices__mutmut_13,
        "xǁThresholdModelǁ_build_matrices__mutmut_14": xǁThresholdModelǁ_build_matrices__mutmut_14,
        "xǁThresholdModelǁ_build_matrices__mutmut_15": xǁThresholdModelǁ_build_matrices__mutmut_15,
        "xǁThresholdModelǁ_build_matrices__mutmut_16": xǁThresholdModelǁ_build_matrices__mutmut_16,
        "xǁThresholdModelǁ_build_matrices__mutmut_17": xǁThresholdModelǁ_build_matrices__mutmut_17,
        "xǁThresholdModelǁ_build_matrices__mutmut_18": xǁThresholdModelǁ_build_matrices__mutmut_18,
        "xǁThresholdModelǁ_build_matrices__mutmut_19": xǁThresholdModelǁ_build_matrices__mutmut_19,
        "xǁThresholdModelǁ_build_matrices__mutmut_20": xǁThresholdModelǁ_build_matrices__mutmut_20,
        "xǁThresholdModelǁ_build_matrices__mutmut_21": xǁThresholdModelǁ_build_matrices__mutmut_21,
        "xǁThresholdModelǁ_build_matrices__mutmut_22": xǁThresholdModelǁ_build_matrices__mutmut_22,
        "xǁThresholdModelǁ_build_matrices__mutmut_23": xǁThresholdModelǁ_build_matrices__mutmut_23,
        "xǁThresholdModelǁ_build_matrices__mutmut_24": xǁThresholdModelǁ_build_matrices__mutmut_24,
        "xǁThresholdModelǁ_build_matrices__mutmut_25": xǁThresholdModelǁ_build_matrices__mutmut_25,
        "xǁThresholdModelǁ_build_matrices__mutmut_26": xǁThresholdModelǁ_build_matrices__mutmut_26,
        "xǁThresholdModelǁ_build_matrices__mutmut_27": xǁThresholdModelǁ_build_matrices__mutmut_27,
    }
    xǁThresholdModelǁ_build_matrices__mutmut_orig.__name__ = "xǁThresholdModelǁ_build_matrices"

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute transition function G(s; params).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Transition function parameters (e.g., gamma, c).

        Returns
        -------
        ndarray
            Transition values in [0, 1], same shape as s.
        """

    @property
    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names."""

    # --- Concrete methods ---

    def fit(self, method: str = "cls") -> Any:
        args = [method]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_orig(self, method: str = "cls") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "cls":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(msg)

        return self._fit_cls()

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_1(self, method: str = "XXclsXX") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "cls":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(msg)

        return self._fit_cls()

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_2(self, method: str = "CLS") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "cls":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(msg)

        return self._fit_cls()

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_3(self, method: str = "cls") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method == "cls":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(msg)

        return self._fit_cls()

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_4(self, method: str = "cls") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "XXclsXX":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(msg)

        return self._fit_cls()

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_5(self, method: str = "cls") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "CLS":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(msg)

        return self._fit_cls()

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_6(self, method: str = "cls") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "cls":
            msg = None
            raise ValueError(msg)

        return self._fit_cls()

    # --- Concrete methods ---

    def xǁThresholdModelǁfit__mutmut_7(self, method: str = "cls") -> Any:
        """Fit the model via Conditional Least Squares.

        Parameters
        ----------
        method : str
            Estimation method. Default 'cls' (Conditional Least Squares).

        Returns
        -------
        ThresholdResults
            Fitted model results.
        """
        if method != "cls":
            msg = f"Unknown estimation method: {method}. Use 'cls'."
            raise ValueError(None)

        return self._fit_cls()

    xǁThresholdModelǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁfit__mutmut_1": xǁThresholdModelǁfit__mutmut_1,
        "xǁThresholdModelǁfit__mutmut_2": xǁThresholdModelǁfit__mutmut_2,
        "xǁThresholdModelǁfit__mutmut_3": xǁThresholdModelǁfit__mutmut_3,
        "xǁThresholdModelǁfit__mutmut_4": xǁThresholdModelǁfit__mutmut_4,
        "xǁThresholdModelǁfit__mutmut_5": xǁThresholdModelǁfit__mutmut_5,
        "xǁThresholdModelǁfit__mutmut_6": xǁThresholdModelǁfit__mutmut_6,
        "xǁThresholdModelǁfit__mutmut_7": xǁThresholdModelǁfit__mutmut_7,
    }
    xǁThresholdModelǁfit__mutmut_orig.__name__ = "xǁThresholdModelǁfit"

    @abstractmethod
    def _fit_cls(self) -> Any:
        """Conditional Least Squares estimation (subclass implements)."""

    def loglike(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        args = [params_regime1, params_regime2, sigma2_1, sigma2_2, g_values]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁloglike__mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁloglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁThresholdModelǁloglike__mutmut_orig(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_1(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = None
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_2(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = None
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_3(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = None
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_4(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = None
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_5(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = None
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_6(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) - fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_7(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 / (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_8(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 + g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_9(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (2 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_10(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 / g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_11(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = None

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_12(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y + fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_13(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = None
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_14(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) - sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_15(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 / (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_16(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 + g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_17(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (2 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_18(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 / g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_19(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = None

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_20(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(None, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_21(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, None)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_22(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_23(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(
            sigma2,
        )

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_24(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1.000000000001)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_25(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = None
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_26(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 / np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_27(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = +0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_28(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -1.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_29(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(None)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_30(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) - resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_31(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) - np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_32(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(None) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_33(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 / np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_34(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(3 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_35(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(None) + resid**2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_36(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 * sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_37(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid * 2 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_38(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**3 / sigma2)
        return float(ll)

    def xǁThresholdModelǁloglike__mutmut_39(
        self,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        sigma2_1: float,
        sigma2_2: float,
        g_values: NDArray[np.float64],
    ) -> float:
        """Compute log-likelihood for the threshold model.

        Parameters
        ----------
        params_regime1 : ndarray
            Parameters for regime 1.
        params_regime2 : ndarray
            Parameters for regime 2.
        sigma2_1 : float
            Variance of regime 1.
        sigma2_2 : float
            Variance of regime 2.
        g_values : ndarray
            Transition values G(s_t) in [0, 1].

        Returns
        -------
        float
            Total log-likelihood.
        """
        y = self._y
        x_mat = self._X
        fitted1 = x_mat @ params_regime1
        fitted2 = x_mat @ params_regime2
        fitted = fitted1 * (1 - g_values) + fitted2 * g_values
        resid = y - fitted

        # Weighted variance
        sigma2 = sigma2_1 * (1 - g_values) + sigma2_2 * g_values
        sigma2 = np.maximum(sigma2, 1e-12)

        ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + resid**2 / sigma2)
        return float(None)

    xǁThresholdModelǁloglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁloglike__mutmut_1": xǁThresholdModelǁloglike__mutmut_1,
        "xǁThresholdModelǁloglike__mutmut_2": xǁThresholdModelǁloglike__mutmut_2,
        "xǁThresholdModelǁloglike__mutmut_3": xǁThresholdModelǁloglike__mutmut_3,
        "xǁThresholdModelǁloglike__mutmut_4": xǁThresholdModelǁloglike__mutmut_4,
        "xǁThresholdModelǁloglike__mutmut_5": xǁThresholdModelǁloglike__mutmut_5,
        "xǁThresholdModelǁloglike__mutmut_6": xǁThresholdModelǁloglike__mutmut_6,
        "xǁThresholdModelǁloglike__mutmut_7": xǁThresholdModelǁloglike__mutmut_7,
        "xǁThresholdModelǁloglike__mutmut_8": xǁThresholdModelǁloglike__mutmut_8,
        "xǁThresholdModelǁloglike__mutmut_9": xǁThresholdModelǁloglike__mutmut_9,
        "xǁThresholdModelǁloglike__mutmut_10": xǁThresholdModelǁloglike__mutmut_10,
        "xǁThresholdModelǁloglike__mutmut_11": xǁThresholdModelǁloglike__mutmut_11,
        "xǁThresholdModelǁloglike__mutmut_12": xǁThresholdModelǁloglike__mutmut_12,
        "xǁThresholdModelǁloglike__mutmut_13": xǁThresholdModelǁloglike__mutmut_13,
        "xǁThresholdModelǁloglike__mutmut_14": xǁThresholdModelǁloglike__mutmut_14,
        "xǁThresholdModelǁloglike__mutmut_15": xǁThresholdModelǁloglike__mutmut_15,
        "xǁThresholdModelǁloglike__mutmut_16": xǁThresholdModelǁloglike__mutmut_16,
        "xǁThresholdModelǁloglike__mutmut_17": xǁThresholdModelǁloglike__mutmut_17,
        "xǁThresholdModelǁloglike__mutmut_18": xǁThresholdModelǁloglike__mutmut_18,
        "xǁThresholdModelǁloglike__mutmut_19": xǁThresholdModelǁloglike__mutmut_19,
        "xǁThresholdModelǁloglike__mutmut_20": xǁThresholdModelǁloglike__mutmut_20,
        "xǁThresholdModelǁloglike__mutmut_21": xǁThresholdModelǁloglike__mutmut_21,
        "xǁThresholdModelǁloglike__mutmut_22": xǁThresholdModelǁloglike__mutmut_22,
        "xǁThresholdModelǁloglike__mutmut_23": xǁThresholdModelǁloglike__mutmut_23,
        "xǁThresholdModelǁloglike__mutmut_24": xǁThresholdModelǁloglike__mutmut_24,
        "xǁThresholdModelǁloglike__mutmut_25": xǁThresholdModelǁloglike__mutmut_25,
        "xǁThresholdModelǁloglike__mutmut_26": xǁThresholdModelǁloglike__mutmut_26,
        "xǁThresholdModelǁloglike__mutmut_27": xǁThresholdModelǁloglike__mutmut_27,
        "xǁThresholdModelǁloglike__mutmut_28": xǁThresholdModelǁloglike__mutmut_28,
        "xǁThresholdModelǁloglike__mutmut_29": xǁThresholdModelǁloglike__mutmut_29,
        "xǁThresholdModelǁloglike__mutmut_30": xǁThresholdModelǁloglike__mutmut_30,
        "xǁThresholdModelǁloglike__mutmut_31": xǁThresholdModelǁloglike__mutmut_31,
        "xǁThresholdModelǁloglike__mutmut_32": xǁThresholdModelǁloglike__mutmut_32,
        "xǁThresholdModelǁloglike__mutmut_33": xǁThresholdModelǁloglike__mutmut_33,
        "xǁThresholdModelǁloglike__mutmut_34": xǁThresholdModelǁloglike__mutmut_34,
        "xǁThresholdModelǁloglike__mutmut_35": xǁThresholdModelǁloglike__mutmut_35,
        "xǁThresholdModelǁloglike__mutmut_36": xǁThresholdModelǁloglike__mutmut_36,
        "xǁThresholdModelǁloglike__mutmut_37": xǁThresholdModelǁloglike__mutmut_37,
        "xǁThresholdModelǁloglike__mutmut_38": xǁThresholdModelǁloglike__mutmut_38,
        "xǁThresholdModelǁloglike__mutmut_39": xǁThresholdModelǁloglike__mutmut_39,
    }
    xǁThresholdModelǁloglike__mutmut_orig.__name__ = "xǁThresholdModelǁloglike"

    def forecast(self, results: Any, horizon: int = 10) -> dict[str, NDArray[np.float64]]:
        args = [results, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁThresholdModelǁforecast__mutmut_orig(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_1(
        self, results: Any, horizon: int = 11
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_2(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = None
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_3(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = None

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_4(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(None)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_5(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(None):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_6(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = None
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_7(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(None)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_8(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order - 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_9(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 2)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_10(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(None, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_11(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, None):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_12(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_13(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(
                1,
            ):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_14(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(2, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_15(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order - 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_16(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 2):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_17(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = None
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_18(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) + lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_19(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = None

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_20(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx > 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_21(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 1 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_22(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 1.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_23(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = None
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_24(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) + self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_25(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) > self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_26(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 1.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_27(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = None
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_28(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array(None)
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_29(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = None

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_30(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(None, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_31(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, None)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_32(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_33(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(
                s_arr,
            )

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_34(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = None
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_35(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = None
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_36(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = None

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_37(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) - f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_38(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 / (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_39(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 + g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_40(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (2 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_41(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[1]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_42(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 / g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_43(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[1]

            y_hist = np.append(y_hist, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_44(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = None

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_45(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(None, forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_46(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, None)

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_47(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(forecasts[h])

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_48(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(
                y_hist,
            )

        return {"mean": forecasts}

    def xǁThresholdModelǁforecast__mutmut_49(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"XXmeanXX": forecasts}

    def xǁThresholdModelǁforecast__mutmut_50(
        self, results: Any, horizon: int = 10
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast using fitted model.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results object.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'mean' forecast array.
        """
        y_hist = self.endog.copy()
        forecasts = np.empty(horizon)

        for h in range(horizon):
            # Build regressors from last p values
            x = np.ones(self.order + 1)
            for lag in range(1, self.order + 1):
                idx = len(y_hist) - lag
                x[lag] = y_hist[idx] if idx >= 0 else 0.0

            # Transition variable
            s_val = y_hist[len(y_hist) - self.delay] if len(y_hist) >= self.delay else 0.0
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, results.transition_params_array)

            # Forecast
            f1 = x @ results.params_regime1
            f2 = x @ results.params_regime2
            forecasts[h] = f1 * (1 - g_val[0]) + f2 * g_val[0]

            y_hist = np.append(y_hist, forecasts[h])

        return {"MEAN": forecasts}

    xǁThresholdModelǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁforecast__mutmut_1": xǁThresholdModelǁforecast__mutmut_1,
        "xǁThresholdModelǁforecast__mutmut_2": xǁThresholdModelǁforecast__mutmut_2,
        "xǁThresholdModelǁforecast__mutmut_3": xǁThresholdModelǁforecast__mutmut_3,
        "xǁThresholdModelǁforecast__mutmut_4": xǁThresholdModelǁforecast__mutmut_4,
        "xǁThresholdModelǁforecast__mutmut_5": xǁThresholdModelǁforecast__mutmut_5,
        "xǁThresholdModelǁforecast__mutmut_6": xǁThresholdModelǁforecast__mutmut_6,
        "xǁThresholdModelǁforecast__mutmut_7": xǁThresholdModelǁforecast__mutmut_7,
        "xǁThresholdModelǁforecast__mutmut_8": xǁThresholdModelǁforecast__mutmut_8,
        "xǁThresholdModelǁforecast__mutmut_9": xǁThresholdModelǁforecast__mutmut_9,
        "xǁThresholdModelǁforecast__mutmut_10": xǁThresholdModelǁforecast__mutmut_10,
        "xǁThresholdModelǁforecast__mutmut_11": xǁThresholdModelǁforecast__mutmut_11,
        "xǁThresholdModelǁforecast__mutmut_12": xǁThresholdModelǁforecast__mutmut_12,
        "xǁThresholdModelǁforecast__mutmut_13": xǁThresholdModelǁforecast__mutmut_13,
        "xǁThresholdModelǁforecast__mutmut_14": xǁThresholdModelǁforecast__mutmut_14,
        "xǁThresholdModelǁforecast__mutmut_15": xǁThresholdModelǁforecast__mutmut_15,
        "xǁThresholdModelǁforecast__mutmut_16": xǁThresholdModelǁforecast__mutmut_16,
        "xǁThresholdModelǁforecast__mutmut_17": xǁThresholdModelǁforecast__mutmut_17,
        "xǁThresholdModelǁforecast__mutmut_18": xǁThresholdModelǁforecast__mutmut_18,
        "xǁThresholdModelǁforecast__mutmut_19": xǁThresholdModelǁforecast__mutmut_19,
        "xǁThresholdModelǁforecast__mutmut_20": xǁThresholdModelǁforecast__mutmut_20,
        "xǁThresholdModelǁforecast__mutmut_21": xǁThresholdModelǁforecast__mutmut_21,
        "xǁThresholdModelǁforecast__mutmut_22": xǁThresholdModelǁforecast__mutmut_22,
        "xǁThresholdModelǁforecast__mutmut_23": xǁThresholdModelǁforecast__mutmut_23,
        "xǁThresholdModelǁforecast__mutmut_24": xǁThresholdModelǁforecast__mutmut_24,
        "xǁThresholdModelǁforecast__mutmut_25": xǁThresholdModelǁforecast__mutmut_25,
        "xǁThresholdModelǁforecast__mutmut_26": xǁThresholdModelǁforecast__mutmut_26,
        "xǁThresholdModelǁforecast__mutmut_27": xǁThresholdModelǁforecast__mutmut_27,
        "xǁThresholdModelǁforecast__mutmut_28": xǁThresholdModelǁforecast__mutmut_28,
        "xǁThresholdModelǁforecast__mutmut_29": xǁThresholdModelǁforecast__mutmut_29,
        "xǁThresholdModelǁforecast__mutmut_30": xǁThresholdModelǁforecast__mutmut_30,
        "xǁThresholdModelǁforecast__mutmut_31": xǁThresholdModelǁforecast__mutmut_31,
        "xǁThresholdModelǁforecast__mutmut_32": xǁThresholdModelǁforecast__mutmut_32,
        "xǁThresholdModelǁforecast__mutmut_33": xǁThresholdModelǁforecast__mutmut_33,
        "xǁThresholdModelǁforecast__mutmut_34": xǁThresholdModelǁforecast__mutmut_34,
        "xǁThresholdModelǁforecast__mutmut_35": xǁThresholdModelǁforecast__mutmut_35,
        "xǁThresholdModelǁforecast__mutmut_36": xǁThresholdModelǁforecast__mutmut_36,
        "xǁThresholdModelǁforecast__mutmut_37": xǁThresholdModelǁforecast__mutmut_37,
        "xǁThresholdModelǁforecast__mutmut_38": xǁThresholdModelǁforecast__mutmut_38,
        "xǁThresholdModelǁforecast__mutmut_39": xǁThresholdModelǁforecast__mutmut_39,
        "xǁThresholdModelǁforecast__mutmut_40": xǁThresholdModelǁforecast__mutmut_40,
        "xǁThresholdModelǁforecast__mutmut_41": xǁThresholdModelǁforecast__mutmut_41,
        "xǁThresholdModelǁforecast__mutmut_42": xǁThresholdModelǁforecast__mutmut_42,
        "xǁThresholdModelǁforecast__mutmut_43": xǁThresholdModelǁforecast__mutmut_43,
        "xǁThresholdModelǁforecast__mutmut_44": xǁThresholdModelǁforecast__mutmut_44,
        "xǁThresholdModelǁforecast__mutmut_45": xǁThresholdModelǁforecast__mutmut_45,
        "xǁThresholdModelǁforecast__mutmut_46": xǁThresholdModelǁforecast__mutmut_46,
        "xǁThresholdModelǁforecast__mutmut_47": xǁThresholdModelǁforecast__mutmut_47,
        "xǁThresholdModelǁforecast__mutmut_48": xǁThresholdModelǁforecast__mutmut_48,
        "xǁThresholdModelǁforecast__mutmut_49": xǁThresholdModelǁforecast__mutmut_49,
        "xǁThresholdModelǁforecast__mutmut_50": xǁThresholdModelǁforecast__mutmut_50,
    }
    xǁThresholdModelǁforecast__mutmut_orig.__name__ = "xǁThresholdModelǁforecast"

    def simulate(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        args = [n, params_regime1, params_regime2, transition_params, sigma, seed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁThresholdModelǁsimulate__mutmut_orig(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_1(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 2.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_2(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = None
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_3(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(None)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_4(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = None
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_5(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = None
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_6(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = None
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_7(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(None, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_8(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, None)
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_9(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_10(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(
            100,
        )
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_11(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(101, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_12(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 / max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_13(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 3 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_14(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(None, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_15(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, None))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_16(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_17(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(
            100,
            2
            * max(
                p,
            ),
        )
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_18(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = None

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_19(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n - burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_20(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = None
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_21(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(None)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_22(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = None

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_23(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) / sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_24(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(None) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_25(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(None, total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_26(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), None):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_27(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_28(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(
            max(p, d),
        ):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_29(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(None, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_30(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, None), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_31(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_32(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(
            max(
                p,
            ),
            total,
        ):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_33(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = None
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_34(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(None)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_35(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p - 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_36(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 2)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_37(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(None, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_38(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, None):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_39(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_40(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(
                1,
            ):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_41(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(2, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_42(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p - 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_43(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 2):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_44(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = None

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_45(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t + lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_46(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = None
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_47(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t + d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_48(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = None
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_49(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array(None)
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_50(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = None

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_51(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(None, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_52(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, None)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_53(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_54(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(
                s_arr,
            )

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_55(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = None

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_56(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[0] - eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_57(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) - (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_58(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) / (1 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_59(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 + g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_60(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (2 - g_val[0]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_61(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[1]) + (x @ params_regime2) * g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_62(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) / g_val[0] + eps[t]

        return y[burn:]

    def xǁThresholdModelǁsimulate__mutmut_63(
        self,
        n: int,
        params_regime1: NDArray[np.float64],
        params_regime2: NDArray[np.float64],
        transition_params: NDArray[np.float64],
        sigma: float = 1.0,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the threshold model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params_regime1 : ndarray
            AR parameters for regime 1 [const, phi_1, ..., phi_p].
        params_regime2 : ndarray
            AR parameters for regime 2 [const, phi_1, ..., phi_p].
        transition_params : ndarray
            Transition function parameters.
        sigma : float
            Innovation standard deviation.
        seed : int, optional
            Random seed.

        Returns
        -------
        ndarray
            Simulated time series of length n.
        """
        rng = np.random.default_rng(seed)
        p = self.order
        d = self.delay
        burn = max(100, 2 * max(p, d))
        total = n + burn

        y = np.zeros(total)
        eps = rng.standard_normal(total) * sigma

        for t in range(max(p, d), total):
            x = np.ones(p + 1)
            for lag in range(1, p + 1):
                x[lag] = y[t - lag]

            s_val = y[t - d]
            s_arr = np.array([s_val])
            g_val = self._transition_function(s_arr, transition_params)

            y[t] = (x @ params_regime1) * (1 - g_val[0]) + (x @ params_regime2) * g_val[1] + eps[t]

        return y[burn:]

    xǁThresholdModelǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁsimulate__mutmut_1": xǁThresholdModelǁsimulate__mutmut_1,
        "xǁThresholdModelǁsimulate__mutmut_2": xǁThresholdModelǁsimulate__mutmut_2,
        "xǁThresholdModelǁsimulate__mutmut_3": xǁThresholdModelǁsimulate__mutmut_3,
        "xǁThresholdModelǁsimulate__mutmut_4": xǁThresholdModelǁsimulate__mutmut_4,
        "xǁThresholdModelǁsimulate__mutmut_5": xǁThresholdModelǁsimulate__mutmut_5,
        "xǁThresholdModelǁsimulate__mutmut_6": xǁThresholdModelǁsimulate__mutmut_6,
        "xǁThresholdModelǁsimulate__mutmut_7": xǁThresholdModelǁsimulate__mutmut_7,
        "xǁThresholdModelǁsimulate__mutmut_8": xǁThresholdModelǁsimulate__mutmut_8,
        "xǁThresholdModelǁsimulate__mutmut_9": xǁThresholdModelǁsimulate__mutmut_9,
        "xǁThresholdModelǁsimulate__mutmut_10": xǁThresholdModelǁsimulate__mutmut_10,
        "xǁThresholdModelǁsimulate__mutmut_11": xǁThresholdModelǁsimulate__mutmut_11,
        "xǁThresholdModelǁsimulate__mutmut_12": xǁThresholdModelǁsimulate__mutmut_12,
        "xǁThresholdModelǁsimulate__mutmut_13": xǁThresholdModelǁsimulate__mutmut_13,
        "xǁThresholdModelǁsimulate__mutmut_14": xǁThresholdModelǁsimulate__mutmut_14,
        "xǁThresholdModelǁsimulate__mutmut_15": xǁThresholdModelǁsimulate__mutmut_15,
        "xǁThresholdModelǁsimulate__mutmut_16": xǁThresholdModelǁsimulate__mutmut_16,
        "xǁThresholdModelǁsimulate__mutmut_17": xǁThresholdModelǁsimulate__mutmut_17,
        "xǁThresholdModelǁsimulate__mutmut_18": xǁThresholdModelǁsimulate__mutmut_18,
        "xǁThresholdModelǁsimulate__mutmut_19": xǁThresholdModelǁsimulate__mutmut_19,
        "xǁThresholdModelǁsimulate__mutmut_20": xǁThresholdModelǁsimulate__mutmut_20,
        "xǁThresholdModelǁsimulate__mutmut_21": xǁThresholdModelǁsimulate__mutmut_21,
        "xǁThresholdModelǁsimulate__mutmut_22": xǁThresholdModelǁsimulate__mutmut_22,
        "xǁThresholdModelǁsimulate__mutmut_23": xǁThresholdModelǁsimulate__mutmut_23,
        "xǁThresholdModelǁsimulate__mutmut_24": xǁThresholdModelǁsimulate__mutmut_24,
        "xǁThresholdModelǁsimulate__mutmut_25": xǁThresholdModelǁsimulate__mutmut_25,
        "xǁThresholdModelǁsimulate__mutmut_26": xǁThresholdModelǁsimulate__mutmut_26,
        "xǁThresholdModelǁsimulate__mutmut_27": xǁThresholdModelǁsimulate__mutmut_27,
        "xǁThresholdModelǁsimulate__mutmut_28": xǁThresholdModelǁsimulate__mutmut_28,
        "xǁThresholdModelǁsimulate__mutmut_29": xǁThresholdModelǁsimulate__mutmut_29,
        "xǁThresholdModelǁsimulate__mutmut_30": xǁThresholdModelǁsimulate__mutmut_30,
        "xǁThresholdModelǁsimulate__mutmut_31": xǁThresholdModelǁsimulate__mutmut_31,
        "xǁThresholdModelǁsimulate__mutmut_32": xǁThresholdModelǁsimulate__mutmut_32,
        "xǁThresholdModelǁsimulate__mutmut_33": xǁThresholdModelǁsimulate__mutmut_33,
        "xǁThresholdModelǁsimulate__mutmut_34": xǁThresholdModelǁsimulate__mutmut_34,
        "xǁThresholdModelǁsimulate__mutmut_35": xǁThresholdModelǁsimulate__mutmut_35,
        "xǁThresholdModelǁsimulate__mutmut_36": xǁThresholdModelǁsimulate__mutmut_36,
        "xǁThresholdModelǁsimulate__mutmut_37": xǁThresholdModelǁsimulate__mutmut_37,
        "xǁThresholdModelǁsimulate__mutmut_38": xǁThresholdModelǁsimulate__mutmut_38,
        "xǁThresholdModelǁsimulate__mutmut_39": xǁThresholdModelǁsimulate__mutmut_39,
        "xǁThresholdModelǁsimulate__mutmut_40": xǁThresholdModelǁsimulate__mutmut_40,
        "xǁThresholdModelǁsimulate__mutmut_41": xǁThresholdModelǁsimulate__mutmut_41,
        "xǁThresholdModelǁsimulate__mutmut_42": xǁThresholdModelǁsimulate__mutmut_42,
        "xǁThresholdModelǁsimulate__mutmut_43": xǁThresholdModelǁsimulate__mutmut_43,
        "xǁThresholdModelǁsimulate__mutmut_44": xǁThresholdModelǁsimulate__mutmut_44,
        "xǁThresholdModelǁsimulate__mutmut_45": xǁThresholdModelǁsimulate__mutmut_45,
        "xǁThresholdModelǁsimulate__mutmut_46": xǁThresholdModelǁsimulate__mutmut_46,
        "xǁThresholdModelǁsimulate__mutmut_47": xǁThresholdModelǁsimulate__mutmut_47,
        "xǁThresholdModelǁsimulate__mutmut_48": xǁThresholdModelǁsimulate__mutmut_48,
        "xǁThresholdModelǁsimulate__mutmut_49": xǁThresholdModelǁsimulate__mutmut_49,
        "xǁThresholdModelǁsimulate__mutmut_50": xǁThresholdModelǁsimulate__mutmut_50,
        "xǁThresholdModelǁsimulate__mutmut_51": xǁThresholdModelǁsimulate__mutmut_51,
        "xǁThresholdModelǁsimulate__mutmut_52": xǁThresholdModelǁsimulate__mutmut_52,
        "xǁThresholdModelǁsimulate__mutmut_53": xǁThresholdModelǁsimulate__mutmut_53,
        "xǁThresholdModelǁsimulate__mutmut_54": xǁThresholdModelǁsimulate__mutmut_54,
        "xǁThresholdModelǁsimulate__mutmut_55": xǁThresholdModelǁsimulate__mutmut_55,
        "xǁThresholdModelǁsimulate__mutmut_56": xǁThresholdModelǁsimulate__mutmut_56,
        "xǁThresholdModelǁsimulate__mutmut_57": xǁThresholdModelǁsimulate__mutmut_57,
        "xǁThresholdModelǁsimulate__mutmut_58": xǁThresholdModelǁsimulate__mutmut_58,
        "xǁThresholdModelǁsimulate__mutmut_59": xǁThresholdModelǁsimulate__mutmut_59,
        "xǁThresholdModelǁsimulate__mutmut_60": xǁThresholdModelǁsimulate__mutmut_60,
        "xǁThresholdModelǁsimulate__mutmut_61": xǁThresholdModelǁsimulate__mutmut_61,
        "xǁThresholdModelǁsimulate__mutmut_62": xǁThresholdModelǁsimulate__mutmut_62,
        "xǁThresholdModelǁsimulate__mutmut_63": xǁThresholdModelǁsimulate__mutmut_63,
    }
    xǁThresholdModelǁsimulate__mutmut_orig.__name__ = "xǁThresholdModelǁsimulate"

    def plot_transition(self, results: Any) -> Any:
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁplot_transition__mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁplot_transition__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁThresholdModelǁplot_transition__mutmut_orig(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_1(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = None
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_2(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(None)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_3(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = None

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_4(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(None, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_5(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, None)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_6(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_7(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(
            s_sorted,
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_8(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = None
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_9(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=None)
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_10(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(11, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_11(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 7))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_12(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(None, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_13(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, None, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_14(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, None, linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_15(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=None)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_16(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_17(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_18(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_19(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(
            s_sorted,
            g_vals,
            "b-",
        )
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_20(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "XXb-XX", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_21(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "B-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_22(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=3)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_23(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel(None)
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_24(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("XXs (transition variable)XX")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_25(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("S (TRANSITION VARIABLE)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_26(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel(None)
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_27(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("XXG(s)XX")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_28(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("g(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_29(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(S)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_30(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(None)
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_31(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=None, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_32(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color=None, linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_33(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle=None, alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_34(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=None)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_35(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_36(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_37(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_38(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(
            y=0.5,
            color="gray",
            linestyle="--",
        )
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_39(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=1.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_40(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="XXgrayXX", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_41(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="GRAY", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_42(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="XX--XX", alpha=0.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_43(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=1.5)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_44(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(None, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_45(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=None)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_46(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_47(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(
            True,
        )
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_48(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(False, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_transition__mutmut_49(self, results: Any) -> Any:
        """Plot the estimated transition function.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        s_sorted = np.sort(self._s)
        g_vals = self._transition_function(s_sorted, results.transition_params_array)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(s_sorted, g_vals, "b-", linewidth=2)
        ax.set_xlabel("s (transition variable)")
        ax.set_ylabel("G(s)")
        ax.set_title(f"{self.model_name} - Transition Function")
        ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
        ax.grid(True, alpha=1.3)
        plt.tight_layout()
        return fig

    xǁThresholdModelǁplot_transition__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁplot_transition__mutmut_1": xǁThresholdModelǁplot_transition__mutmut_1,
        "xǁThresholdModelǁplot_transition__mutmut_2": xǁThresholdModelǁplot_transition__mutmut_2,
        "xǁThresholdModelǁplot_transition__mutmut_3": xǁThresholdModelǁplot_transition__mutmut_3,
        "xǁThresholdModelǁplot_transition__mutmut_4": xǁThresholdModelǁplot_transition__mutmut_4,
        "xǁThresholdModelǁplot_transition__mutmut_5": xǁThresholdModelǁplot_transition__mutmut_5,
        "xǁThresholdModelǁplot_transition__mutmut_6": xǁThresholdModelǁplot_transition__mutmut_6,
        "xǁThresholdModelǁplot_transition__mutmut_7": xǁThresholdModelǁplot_transition__mutmut_7,
        "xǁThresholdModelǁplot_transition__mutmut_8": xǁThresholdModelǁplot_transition__mutmut_8,
        "xǁThresholdModelǁplot_transition__mutmut_9": xǁThresholdModelǁplot_transition__mutmut_9,
        "xǁThresholdModelǁplot_transition__mutmut_10": xǁThresholdModelǁplot_transition__mutmut_10,
        "xǁThresholdModelǁplot_transition__mutmut_11": xǁThresholdModelǁplot_transition__mutmut_11,
        "xǁThresholdModelǁplot_transition__mutmut_12": xǁThresholdModelǁplot_transition__mutmut_12,
        "xǁThresholdModelǁplot_transition__mutmut_13": xǁThresholdModelǁplot_transition__mutmut_13,
        "xǁThresholdModelǁplot_transition__mutmut_14": xǁThresholdModelǁplot_transition__mutmut_14,
        "xǁThresholdModelǁplot_transition__mutmut_15": xǁThresholdModelǁplot_transition__mutmut_15,
        "xǁThresholdModelǁplot_transition__mutmut_16": xǁThresholdModelǁplot_transition__mutmut_16,
        "xǁThresholdModelǁplot_transition__mutmut_17": xǁThresholdModelǁplot_transition__mutmut_17,
        "xǁThresholdModelǁplot_transition__mutmut_18": xǁThresholdModelǁplot_transition__mutmut_18,
        "xǁThresholdModelǁplot_transition__mutmut_19": xǁThresholdModelǁplot_transition__mutmut_19,
        "xǁThresholdModelǁplot_transition__mutmut_20": xǁThresholdModelǁplot_transition__mutmut_20,
        "xǁThresholdModelǁplot_transition__mutmut_21": xǁThresholdModelǁplot_transition__mutmut_21,
        "xǁThresholdModelǁplot_transition__mutmut_22": xǁThresholdModelǁplot_transition__mutmut_22,
        "xǁThresholdModelǁplot_transition__mutmut_23": xǁThresholdModelǁplot_transition__mutmut_23,
        "xǁThresholdModelǁplot_transition__mutmut_24": xǁThresholdModelǁplot_transition__mutmut_24,
        "xǁThresholdModelǁplot_transition__mutmut_25": xǁThresholdModelǁplot_transition__mutmut_25,
        "xǁThresholdModelǁplot_transition__mutmut_26": xǁThresholdModelǁplot_transition__mutmut_26,
        "xǁThresholdModelǁplot_transition__mutmut_27": xǁThresholdModelǁplot_transition__mutmut_27,
        "xǁThresholdModelǁplot_transition__mutmut_28": xǁThresholdModelǁplot_transition__mutmut_28,
        "xǁThresholdModelǁplot_transition__mutmut_29": xǁThresholdModelǁplot_transition__mutmut_29,
        "xǁThresholdModelǁplot_transition__mutmut_30": xǁThresholdModelǁplot_transition__mutmut_30,
        "xǁThresholdModelǁplot_transition__mutmut_31": xǁThresholdModelǁplot_transition__mutmut_31,
        "xǁThresholdModelǁplot_transition__mutmut_32": xǁThresholdModelǁplot_transition__mutmut_32,
        "xǁThresholdModelǁplot_transition__mutmut_33": xǁThresholdModelǁplot_transition__mutmut_33,
        "xǁThresholdModelǁplot_transition__mutmut_34": xǁThresholdModelǁplot_transition__mutmut_34,
        "xǁThresholdModelǁplot_transition__mutmut_35": xǁThresholdModelǁplot_transition__mutmut_35,
        "xǁThresholdModelǁplot_transition__mutmut_36": xǁThresholdModelǁplot_transition__mutmut_36,
        "xǁThresholdModelǁplot_transition__mutmut_37": xǁThresholdModelǁplot_transition__mutmut_37,
        "xǁThresholdModelǁplot_transition__mutmut_38": xǁThresholdModelǁplot_transition__mutmut_38,
        "xǁThresholdModelǁplot_transition__mutmut_39": xǁThresholdModelǁplot_transition__mutmut_39,
        "xǁThresholdModelǁplot_transition__mutmut_40": xǁThresholdModelǁplot_transition__mutmut_40,
        "xǁThresholdModelǁplot_transition__mutmut_41": xǁThresholdModelǁplot_transition__mutmut_41,
        "xǁThresholdModelǁplot_transition__mutmut_42": xǁThresholdModelǁplot_transition__mutmut_42,
        "xǁThresholdModelǁplot_transition__mutmut_43": xǁThresholdModelǁplot_transition__mutmut_43,
        "xǁThresholdModelǁplot_transition__mutmut_44": xǁThresholdModelǁplot_transition__mutmut_44,
        "xǁThresholdModelǁplot_transition__mutmut_45": xǁThresholdModelǁplot_transition__mutmut_45,
        "xǁThresholdModelǁplot_transition__mutmut_46": xǁThresholdModelǁplot_transition__mutmut_46,
        "xǁThresholdModelǁplot_transition__mutmut_47": xǁThresholdModelǁplot_transition__mutmut_47,
        "xǁThresholdModelǁplot_transition__mutmut_48": xǁThresholdModelǁplot_transition__mutmut_48,
        "xǁThresholdModelǁplot_transition__mutmut_49": xǁThresholdModelǁplot_transition__mutmut_49,
    }
    xǁThresholdModelǁplot_transition__mutmut_orig.__name__ = "xǁThresholdModelǁplot_transition"

    def plot_phase_diagram(self, results: Any) -> Any:
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁThresholdModelǁplot_phase_diagram__mutmut_orig"),
            object.__getattribute__(self, "xǁThresholdModelǁplot_phase_diagram__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁThresholdModelǁplot_phase_diagram__mutmut_orig(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_1(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = None

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_2(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=None)

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_3(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(11, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_4(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 9))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_5(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = None
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_6(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = None
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_7(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = None

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_8(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 2] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_9(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order > 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_10(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 2 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_11(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = None
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_12(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(None, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_13(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, None, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_14(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=None, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_15(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap=None, alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_16(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=None, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_17(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=None)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_18(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_19(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_20(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_21(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_22(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_23(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(
            y_tm1,
            y_t,
            c=g_vals,
            cmap="coolwarm",
            alpha=0.6,
        )
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_24(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="XXcoolwarmXX", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_25(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="COOLWARM", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_26(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=1.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_27(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=11)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_28(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(None, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_29(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=None, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_30(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label=None)
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_31(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_32(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_33(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(
            scatter,
            ax=ax,
        )
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_34(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="XXG(s_t)XX")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_35(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="g(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_36(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(S_T)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_37(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel(None)
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_38(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("XXy_{t-1}XX")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_39(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("Y_{T-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_40(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel(None)
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_41(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("XXy_tXX")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_42(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("Y_T")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_43(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(None)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_44(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(None, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_45(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=None)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_46(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_47(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(
            True,
        )
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_48(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(False, alpha=0.3)
        plt.tight_layout()
        return fig

    def xǁThresholdModelǁplot_phase_diagram__mutmut_49(self, results: Any) -> Any:
        """Plot phase diagram y_t vs y_{t-1} with regime coloring.

        Parameters
        ----------
        results : ThresholdResults
            Fitted results.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))

        g_vals = results.transition_values
        y_t = self._y
        y_tm1 = self._X[:, 1] if self.order >= 1 else self._y

        scatter = ax.scatter(y_tm1, y_t, c=g_vals, cmap="coolwarm", alpha=0.6, s=10)
        plt.colorbar(scatter, ax=ax, label="G(s_t)")
        ax.set_xlabel("y_{t-1}")
        ax.set_ylabel("y_t")
        ax.set_title(f"{self.model_name} - Phase Diagram")
        ax.grid(True, alpha=1.3)
        plt.tight_layout()
        return fig

    xǁThresholdModelǁplot_phase_diagram__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁThresholdModelǁplot_phase_diagram__mutmut_1": xǁThresholdModelǁplot_phase_diagram__mutmut_1,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_2": xǁThresholdModelǁplot_phase_diagram__mutmut_2,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_3": xǁThresholdModelǁplot_phase_diagram__mutmut_3,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_4": xǁThresholdModelǁplot_phase_diagram__mutmut_4,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_5": xǁThresholdModelǁplot_phase_diagram__mutmut_5,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_6": xǁThresholdModelǁplot_phase_diagram__mutmut_6,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_7": xǁThresholdModelǁplot_phase_diagram__mutmut_7,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_8": xǁThresholdModelǁplot_phase_diagram__mutmut_8,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_9": xǁThresholdModelǁplot_phase_diagram__mutmut_9,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_10": xǁThresholdModelǁplot_phase_diagram__mutmut_10,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_11": xǁThresholdModelǁplot_phase_diagram__mutmut_11,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_12": xǁThresholdModelǁplot_phase_diagram__mutmut_12,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_13": xǁThresholdModelǁplot_phase_diagram__mutmut_13,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_14": xǁThresholdModelǁplot_phase_diagram__mutmut_14,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_15": xǁThresholdModelǁplot_phase_diagram__mutmut_15,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_16": xǁThresholdModelǁplot_phase_diagram__mutmut_16,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_17": xǁThresholdModelǁplot_phase_diagram__mutmut_17,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_18": xǁThresholdModelǁplot_phase_diagram__mutmut_18,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_19": xǁThresholdModelǁplot_phase_diagram__mutmut_19,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_20": xǁThresholdModelǁplot_phase_diagram__mutmut_20,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_21": xǁThresholdModelǁplot_phase_diagram__mutmut_21,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_22": xǁThresholdModelǁplot_phase_diagram__mutmut_22,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_23": xǁThresholdModelǁplot_phase_diagram__mutmut_23,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_24": xǁThresholdModelǁplot_phase_diagram__mutmut_24,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_25": xǁThresholdModelǁplot_phase_diagram__mutmut_25,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_26": xǁThresholdModelǁplot_phase_diagram__mutmut_26,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_27": xǁThresholdModelǁplot_phase_diagram__mutmut_27,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_28": xǁThresholdModelǁplot_phase_diagram__mutmut_28,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_29": xǁThresholdModelǁplot_phase_diagram__mutmut_29,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_30": xǁThresholdModelǁplot_phase_diagram__mutmut_30,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_31": xǁThresholdModelǁplot_phase_diagram__mutmut_31,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_32": xǁThresholdModelǁplot_phase_diagram__mutmut_32,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_33": xǁThresholdModelǁplot_phase_diagram__mutmut_33,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_34": xǁThresholdModelǁplot_phase_diagram__mutmut_34,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_35": xǁThresholdModelǁplot_phase_diagram__mutmut_35,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_36": xǁThresholdModelǁplot_phase_diagram__mutmut_36,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_37": xǁThresholdModelǁplot_phase_diagram__mutmut_37,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_38": xǁThresholdModelǁplot_phase_diagram__mutmut_38,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_39": xǁThresholdModelǁplot_phase_diagram__mutmut_39,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_40": xǁThresholdModelǁplot_phase_diagram__mutmut_40,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_41": xǁThresholdModelǁplot_phase_diagram__mutmut_41,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_42": xǁThresholdModelǁplot_phase_diagram__mutmut_42,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_43": xǁThresholdModelǁplot_phase_diagram__mutmut_43,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_44": xǁThresholdModelǁplot_phase_diagram__mutmut_44,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_45": xǁThresholdModelǁplot_phase_diagram__mutmut_45,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_46": xǁThresholdModelǁplot_phase_diagram__mutmut_46,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_47": xǁThresholdModelǁplot_phase_diagram__mutmut_47,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_48": xǁThresholdModelǁplot_phase_diagram__mutmut_48,
        "xǁThresholdModelǁplot_phase_diagram__mutmut_49": xǁThresholdModelǁplot_phase_diagram__mutmut_49,
    }
    xǁThresholdModelǁplot_phase_diagram__mutmut_orig.__name__ = (
        "xǁThresholdModelǁplot_phase_diagram"
    )

    @staticmethod
    def _ols_fit(
        y: NDArray[np.float64], x_mat: NDArray[np.float64]
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS regression returning coefficients, residuals, and RSS.

        Parameters
        ----------
        y : ndarray, shape (n,)
            Dependent variable.
        x_mat : ndarray, shape (n, k)
            Regressors.

        Returns
        -------
        beta : ndarray, shape (k,)
            OLS coefficients.
        resid : ndarray, shape (n,)
            Residuals.
        rss : float
            Residual sum of squares.
        """
        beta = np.linalg.lstsq(x_mat, y, rcond=None)[0]
        resid = y - x_mat @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    @staticmethod
    def _ols_rss(y: NDArray[np.float64], x_mat: NDArray[np.float64]) -> float:
        """Compute RSS from OLS regression.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Regressors.

        Returns
        -------
        float
            Residual sum of squares.
        """
        beta = np.linalg.lstsq(x_mat, y, rcond=None)[0]
        resid = y - x_mat @ beta
        return float(np.sum(resid**2))
