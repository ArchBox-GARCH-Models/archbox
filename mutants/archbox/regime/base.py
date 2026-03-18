"""Base class for Markov-Switching models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from archbox.regime.results import RegimeResults
from collections.abc import Callable
from typing import Annotated, ClassVar

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


class MarkovSwitchingModel(ABC):
    """Abstract base class for Markov-Switching models.

    All Markov-Switching models (MS-AR, MS-GARCH, MS-VAR, etc.) inherit
    from this class.

    Parameters
    ----------
    endog : array-like
        Time series of observations. Shape (T,) for univariate,
        (T, n) for multivariate.
    k_regimes : int
        Number of regimes (states). Default is 2.
    order : int
        Autoregressive order (number of lags). Default is 1.
    switching_mean : bool
        If True, the mean switches between regimes.
    switching_variance : bool
        If True, the variance switches between regimes.
    switching_ar : bool
        If True, the AR coefficients switch between regimes.

    Attributes
    ----------
    endog : NDArray[np.float64]
        Observations array.
    nobs : int
        Number of observations.
    k_regimes : int
        Number of regimes.
    order : int
        Autoregressive order.
    switching_mean : bool
        Whether the mean switches.
    switching_variance : bool
        Whether the variance switches.
    switching_ar : bool
        Whether AR coefficients switch.
    """

    model_name: str = "MarkovSwitching"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        args = [endog, k_regimes, order, switching_mean, switching_variance, switching_ar]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingModelǁ__init____mutmut_orig(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_1(
        self,
        endog: Any,
        k_regimes: int = 3,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_2(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 2,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_3(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = False,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_4(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = False,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_5(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = True,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_6(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = None
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_7(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(None, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_8(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=None)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_9(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_10(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(
            endog,
        )
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_11(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_12(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 2:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_13(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = None
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_14(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = None
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_15(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 2
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_16(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim != 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_17(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 3:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_18(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = None
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_19(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = None
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_20(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(None)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_21(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes <= 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_22(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 3:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_23(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = None
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_24(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(None)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_25(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = None
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_26(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = None
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_27(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = None
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_28(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = None
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_29(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = None

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_30(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = None
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_31(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = True
        self._transition_matrix: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingModelǁ__init____mutmut_32(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching model with regime configuration."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 1:
            self.nobs = len(self.endog)
            self.n_vars = 1
        elif self.endog.ndim == 2:
            self.nobs, self.n_vars = self.endog.shape
        else:
            msg = f"endog must be 1D or 2D, got {self.endog.ndim}D"
            raise ValueError(msg)

        if k_regimes < 2:
            msg = f"k_regimes must be >= 2, got {k_regimes}"
            raise ValueError(msg)

        self.k_regimes = k_regimes
        self.order = order
        self.switching_mean = switching_mean
        self.switching_variance = switching_variance
        self.switching_ar = switching_ar

        self._is_fitted = False
        self._transition_matrix: NDArray[np.float64] | None = ""

    xǁMarkovSwitchingModelǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingModelǁ__init____mutmut_1": xǁMarkovSwitchingModelǁ__init____mutmut_1,
        "xǁMarkovSwitchingModelǁ__init____mutmut_2": xǁMarkovSwitchingModelǁ__init____mutmut_2,
        "xǁMarkovSwitchingModelǁ__init____mutmut_3": xǁMarkovSwitchingModelǁ__init____mutmut_3,
        "xǁMarkovSwitchingModelǁ__init____mutmut_4": xǁMarkovSwitchingModelǁ__init____mutmut_4,
        "xǁMarkovSwitchingModelǁ__init____mutmut_5": xǁMarkovSwitchingModelǁ__init____mutmut_5,
        "xǁMarkovSwitchingModelǁ__init____mutmut_6": xǁMarkovSwitchingModelǁ__init____mutmut_6,
        "xǁMarkovSwitchingModelǁ__init____mutmut_7": xǁMarkovSwitchingModelǁ__init____mutmut_7,
        "xǁMarkovSwitchingModelǁ__init____mutmut_8": xǁMarkovSwitchingModelǁ__init____mutmut_8,
        "xǁMarkovSwitchingModelǁ__init____mutmut_9": xǁMarkovSwitchingModelǁ__init____mutmut_9,
        "xǁMarkovSwitchingModelǁ__init____mutmut_10": xǁMarkovSwitchingModelǁ__init____mutmut_10,
        "xǁMarkovSwitchingModelǁ__init____mutmut_11": xǁMarkovSwitchingModelǁ__init____mutmut_11,
        "xǁMarkovSwitchingModelǁ__init____mutmut_12": xǁMarkovSwitchingModelǁ__init____mutmut_12,
        "xǁMarkovSwitchingModelǁ__init____mutmut_13": xǁMarkovSwitchingModelǁ__init____mutmut_13,
        "xǁMarkovSwitchingModelǁ__init____mutmut_14": xǁMarkovSwitchingModelǁ__init____mutmut_14,
        "xǁMarkovSwitchingModelǁ__init____mutmut_15": xǁMarkovSwitchingModelǁ__init____mutmut_15,
        "xǁMarkovSwitchingModelǁ__init____mutmut_16": xǁMarkovSwitchingModelǁ__init____mutmut_16,
        "xǁMarkovSwitchingModelǁ__init____mutmut_17": xǁMarkovSwitchingModelǁ__init____mutmut_17,
        "xǁMarkovSwitchingModelǁ__init____mutmut_18": xǁMarkovSwitchingModelǁ__init____mutmut_18,
        "xǁMarkovSwitchingModelǁ__init____mutmut_19": xǁMarkovSwitchingModelǁ__init____mutmut_19,
        "xǁMarkovSwitchingModelǁ__init____mutmut_20": xǁMarkovSwitchingModelǁ__init____mutmut_20,
        "xǁMarkovSwitchingModelǁ__init____mutmut_21": xǁMarkovSwitchingModelǁ__init____mutmut_21,
        "xǁMarkovSwitchingModelǁ__init____mutmut_22": xǁMarkovSwitchingModelǁ__init____mutmut_22,
        "xǁMarkovSwitchingModelǁ__init____mutmut_23": xǁMarkovSwitchingModelǁ__init____mutmut_23,
        "xǁMarkovSwitchingModelǁ__init____mutmut_24": xǁMarkovSwitchingModelǁ__init____mutmut_24,
        "xǁMarkovSwitchingModelǁ__init____mutmut_25": xǁMarkovSwitchingModelǁ__init____mutmut_25,
        "xǁMarkovSwitchingModelǁ__init____mutmut_26": xǁMarkovSwitchingModelǁ__init____mutmut_26,
        "xǁMarkovSwitchingModelǁ__init____mutmut_27": xǁMarkovSwitchingModelǁ__init____mutmut_27,
        "xǁMarkovSwitchingModelǁ__init____mutmut_28": xǁMarkovSwitchingModelǁ__init____mutmut_28,
        "xǁMarkovSwitchingModelǁ__init____mutmut_29": xǁMarkovSwitchingModelǁ__init____mutmut_29,
        "xǁMarkovSwitchingModelǁ__init____mutmut_30": xǁMarkovSwitchingModelǁ__init____mutmut_30,
        "xǁMarkovSwitchingModelǁ__init____mutmut_31": xǁMarkovSwitchingModelǁ__init____mutmut_31,
        "xǁMarkovSwitchingModelǁ__init____mutmut_32": xǁMarkovSwitchingModelǁ__init____mutmut_32,
    }
    xǁMarkovSwitchingModelǁ__init____mutmut_orig.__name__ = "xǁMarkovSwitchingModelǁ__init__"

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t = regime, Y_{t-1}, theta) for all t.

        Parameters
        ----------
        params : ndarray
            All model parameters.
        regime : int
            Regime index (0, 1, ..., k_regimes-1).

        Returns
        -------
        ndarray
            Log-likelihood per observation for the given regime, shape (T,).
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

    def fit(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        args = [method, maxiter, em_iter, tol, verbose]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_orig(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_1(
        self,
        method: str = "XXemXX",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_2(
        self,
        method: str = "EM",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_3(
        self,
        method: str = "em",
        maxiter: int = 501,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_4(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 101,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_5(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1.00000001,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_6(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = False,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_7(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """

        estimator = None
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_8(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = None
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_9(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=None,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_10(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=None,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_11(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=None,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_12(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=None,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_13(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_14(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_15(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            verbose=verbose,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_16(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_17(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = None
        return results

    # --- Concrete methods ---

    def xǁMarkovSwitchingModelǁfit__mutmut_18(
        self,
        method: str = "em",
        maxiter: int = 500,
        em_iter: int = 100,
        tol: float = 1e-8,
        verbose: bool = True,
    ) -> RegimeResults:
        """Fit the model.

        Parameters
        ----------
        method : str
            Estimation method. 'em' for EM algorithm (default).
        maxiter : int
            Maximum number of iterations.
        em_iter : int
            Number of EM iterations before switching to direct optimization.
        tol : float
            Convergence tolerance.
        verbose : bool
            Display progress.

        Returns
        -------
        RegimeResults
            Fitted model results.
        """
        from archbox.regime.em import EMEstimator

        estimator = EMEstimator()
        results = estimator.fit(
            model=self,
            maxiter=maxiter,
            tol=tol,
            verbose=verbose,
        )
        self._is_fitted = False
        return results

    xǁMarkovSwitchingModelǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingModelǁfit__mutmut_1": xǁMarkovSwitchingModelǁfit__mutmut_1,
        "xǁMarkovSwitchingModelǁfit__mutmut_2": xǁMarkovSwitchingModelǁfit__mutmut_2,
        "xǁMarkovSwitchingModelǁfit__mutmut_3": xǁMarkovSwitchingModelǁfit__mutmut_3,
        "xǁMarkovSwitchingModelǁfit__mutmut_4": xǁMarkovSwitchingModelǁfit__mutmut_4,
        "xǁMarkovSwitchingModelǁfit__mutmut_5": xǁMarkovSwitchingModelǁfit__mutmut_5,
        "xǁMarkovSwitchingModelǁfit__mutmut_6": xǁMarkovSwitchingModelǁfit__mutmut_6,
        "xǁMarkovSwitchingModelǁfit__mutmut_7": xǁMarkovSwitchingModelǁfit__mutmut_7,
        "xǁMarkovSwitchingModelǁfit__mutmut_8": xǁMarkovSwitchingModelǁfit__mutmut_8,
        "xǁMarkovSwitchingModelǁfit__mutmut_9": xǁMarkovSwitchingModelǁfit__mutmut_9,
        "xǁMarkovSwitchingModelǁfit__mutmut_10": xǁMarkovSwitchingModelǁfit__mutmut_10,
        "xǁMarkovSwitchingModelǁfit__mutmut_11": xǁMarkovSwitchingModelǁfit__mutmut_11,
        "xǁMarkovSwitchingModelǁfit__mutmut_12": xǁMarkovSwitchingModelǁfit__mutmut_12,
        "xǁMarkovSwitchingModelǁfit__mutmut_13": xǁMarkovSwitchingModelǁfit__mutmut_13,
        "xǁMarkovSwitchingModelǁfit__mutmut_14": xǁMarkovSwitchingModelǁfit__mutmut_14,
        "xǁMarkovSwitchingModelǁfit__mutmut_15": xǁMarkovSwitchingModelǁfit__mutmut_15,
        "xǁMarkovSwitchingModelǁfit__mutmut_16": xǁMarkovSwitchingModelǁfit__mutmut_16,
        "xǁMarkovSwitchingModelǁfit__mutmut_17": xǁMarkovSwitchingModelǁfit__mutmut_17,
        "xǁMarkovSwitchingModelǁfit__mutmut_18": xǁMarkovSwitchingModelǁfit__mutmut_18,
    }
    xǁMarkovSwitchingModelǁfit__mutmut_orig.__name__ = "xǁMarkovSwitchingModelǁfit"

    def loglike(self, params: NDArray[np.float64]) -> float:
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁloglike__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁloglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingModelǁloglike__mutmut_orig(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_1(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = None
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_2(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(None)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_3(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = None

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_4(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = None
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_5(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(None, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_6(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, None)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_7(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_8(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(
                params,
            )
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_9(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(None)

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_10(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = None
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_11(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(None, regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_12(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, None, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_13(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, regime_loglike_fn, None)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_14(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(regime_loglike_fn, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_15(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(self.endog, transition_matrix)
        return loglike

    def xǁMarkovSwitchingModelǁloglike__mutmut_16(self, params: NDArray[np.float64]) -> float:
        """Compute total log-likelihood via Hamilton filter.

        Parameters
        ----------
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            Total log-likelihood.
        """
        from archbox.regime.hamilton_filter import HamiltonFilter

        transition_matrix = self._extract_transition_matrix(params)
        hfilter = HamiltonFilter()

        def regime_loglike_fn(t: int, s: int) -> float:
            """Compute regime-specific log-likelihood at time t."""
            all_ll = self._regime_loglike(params, s)
            return float(all_ll[t])

        _, _, loglike, _ = hfilter.filter(
            self.endog,
            regime_loglike_fn,
        )
        return loglike

    xǁMarkovSwitchingModelǁloglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingModelǁloglike__mutmut_1": xǁMarkovSwitchingModelǁloglike__mutmut_1,
        "xǁMarkovSwitchingModelǁloglike__mutmut_2": xǁMarkovSwitchingModelǁloglike__mutmut_2,
        "xǁMarkovSwitchingModelǁloglike__mutmut_3": xǁMarkovSwitchingModelǁloglike__mutmut_3,
        "xǁMarkovSwitchingModelǁloglike__mutmut_4": xǁMarkovSwitchingModelǁloglike__mutmut_4,
        "xǁMarkovSwitchingModelǁloglike__mutmut_5": xǁMarkovSwitchingModelǁloglike__mutmut_5,
        "xǁMarkovSwitchingModelǁloglike__mutmut_6": xǁMarkovSwitchingModelǁloglike__mutmut_6,
        "xǁMarkovSwitchingModelǁloglike__mutmut_7": xǁMarkovSwitchingModelǁloglike__mutmut_7,
        "xǁMarkovSwitchingModelǁloglike__mutmut_8": xǁMarkovSwitchingModelǁloglike__mutmut_8,
        "xǁMarkovSwitchingModelǁloglike__mutmut_9": xǁMarkovSwitchingModelǁloglike__mutmut_9,
        "xǁMarkovSwitchingModelǁloglike__mutmut_10": xǁMarkovSwitchingModelǁloglike__mutmut_10,
        "xǁMarkovSwitchingModelǁloglike__mutmut_11": xǁMarkovSwitchingModelǁloglike__mutmut_11,
        "xǁMarkovSwitchingModelǁloglike__mutmut_12": xǁMarkovSwitchingModelǁloglike__mutmut_12,
        "xǁMarkovSwitchingModelǁloglike__mutmut_13": xǁMarkovSwitchingModelǁloglike__mutmut_13,
        "xǁMarkovSwitchingModelǁloglike__mutmut_14": xǁMarkovSwitchingModelǁloglike__mutmut_14,
        "xǁMarkovSwitchingModelǁloglike__mutmut_15": xǁMarkovSwitchingModelǁloglike__mutmut_15,
        "xǁMarkovSwitchingModelǁloglike__mutmut_16": xǁMarkovSwitchingModelǁloglike__mutmut_16,
    }
    xǁMarkovSwitchingModelǁloglike__mutmut_orig.__name__ = "xǁMarkovSwitchingModelǁloglike"

    def forecast(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        args = [horizon, params, transition_matrix, last_probs]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingModelǁforecast__mutmut_orig(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_1(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None or self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_2(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is not None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_3(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_4(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = None

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_5(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is not None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_6(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = None
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_7(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "XXNo transition matrix available. Fit the model first.XX"
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_8(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "no transition matrix available. fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_9(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "NO TRANSITION MATRIX AVAILABLE. FIT THE MODEL FIRST."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_10(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(None)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_11(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = None
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_12(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = None

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_13(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is not None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_14(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = None

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_15(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) * k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_16(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(None) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_17(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = None
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_18(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros(None)
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_19(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = None

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_20(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(None):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_21(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = None
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_22(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = None

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_23(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = None
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_24(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(None)
        return {"mean": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_25(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"XXmeanXX": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_26(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"MEAN": forecast_mean, "regime_probs": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_27(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "XXregime_probsXX": regime_probs}

    def xǁMarkovSwitchingModelǁforecast__mutmut_28(
        self,
        horizon: int,
        params: NDArray[np.float64] | None = None,
        transition_matrix: NDArray[np.float64] | None = None,
        last_probs: NDArray[np.float64] | None = None,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast future values with regime probabilities.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        params : ndarray, optional
            Model parameters. Uses fitted params if None.
        transition_matrix : ndarray, optional
            Transition matrix. Uses fitted matrix if None.
        last_probs : ndarray, optional
            Last filtered probabilities. Uses fitted probs if None.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'mean': forecasted means, shape (horizon,)
            - 'regime_probs': forecasted regime probabilities, shape (horizon, k)
        """
        if transition_matrix is None and self._transition_matrix is not None:
            transition_matrix = self._transition_matrix

        if transition_matrix is None:
            msg = "No transition matrix available. Fit the model first."
            raise RuntimeError(msg)

        k = self.k_regimes
        trans = transition_matrix

        if last_probs is None:
            last_probs = np.ones(k) / k

        regime_probs = np.zeros((horizon, k))
        probs = last_probs.copy()

        for h in range(horizon):
            probs = trans.T @ probs
            regime_probs[h] = probs

        # Mean forecast is weighted average of regime means
        forecast_mean = np.zeros(horizon)
        return {"mean": forecast_mean, "REGIME_PROBS": regime_probs}

    xǁMarkovSwitchingModelǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingModelǁforecast__mutmut_1": xǁMarkovSwitchingModelǁforecast__mutmut_1,
        "xǁMarkovSwitchingModelǁforecast__mutmut_2": xǁMarkovSwitchingModelǁforecast__mutmut_2,
        "xǁMarkovSwitchingModelǁforecast__mutmut_3": xǁMarkovSwitchingModelǁforecast__mutmut_3,
        "xǁMarkovSwitchingModelǁforecast__mutmut_4": xǁMarkovSwitchingModelǁforecast__mutmut_4,
        "xǁMarkovSwitchingModelǁforecast__mutmut_5": xǁMarkovSwitchingModelǁforecast__mutmut_5,
        "xǁMarkovSwitchingModelǁforecast__mutmut_6": xǁMarkovSwitchingModelǁforecast__mutmut_6,
        "xǁMarkovSwitchingModelǁforecast__mutmut_7": xǁMarkovSwitchingModelǁforecast__mutmut_7,
        "xǁMarkovSwitchingModelǁforecast__mutmut_8": xǁMarkovSwitchingModelǁforecast__mutmut_8,
        "xǁMarkovSwitchingModelǁforecast__mutmut_9": xǁMarkovSwitchingModelǁforecast__mutmut_9,
        "xǁMarkovSwitchingModelǁforecast__mutmut_10": xǁMarkovSwitchingModelǁforecast__mutmut_10,
        "xǁMarkovSwitchingModelǁforecast__mutmut_11": xǁMarkovSwitchingModelǁforecast__mutmut_11,
        "xǁMarkovSwitchingModelǁforecast__mutmut_12": xǁMarkovSwitchingModelǁforecast__mutmut_12,
        "xǁMarkovSwitchingModelǁforecast__mutmut_13": xǁMarkovSwitchingModelǁforecast__mutmut_13,
        "xǁMarkovSwitchingModelǁforecast__mutmut_14": xǁMarkovSwitchingModelǁforecast__mutmut_14,
        "xǁMarkovSwitchingModelǁforecast__mutmut_15": xǁMarkovSwitchingModelǁforecast__mutmut_15,
        "xǁMarkovSwitchingModelǁforecast__mutmut_16": xǁMarkovSwitchingModelǁforecast__mutmut_16,
        "xǁMarkovSwitchingModelǁforecast__mutmut_17": xǁMarkovSwitchingModelǁforecast__mutmut_17,
        "xǁMarkovSwitchingModelǁforecast__mutmut_18": xǁMarkovSwitchingModelǁforecast__mutmut_18,
        "xǁMarkovSwitchingModelǁforecast__mutmut_19": xǁMarkovSwitchingModelǁforecast__mutmut_19,
        "xǁMarkovSwitchingModelǁforecast__mutmut_20": xǁMarkovSwitchingModelǁforecast__mutmut_20,
        "xǁMarkovSwitchingModelǁforecast__mutmut_21": xǁMarkovSwitchingModelǁforecast__mutmut_21,
        "xǁMarkovSwitchingModelǁforecast__mutmut_22": xǁMarkovSwitchingModelǁforecast__mutmut_22,
        "xǁMarkovSwitchingModelǁforecast__mutmut_23": xǁMarkovSwitchingModelǁforecast__mutmut_23,
        "xǁMarkovSwitchingModelǁforecast__mutmut_24": xǁMarkovSwitchingModelǁforecast__mutmut_24,
        "xǁMarkovSwitchingModelǁforecast__mutmut_25": xǁMarkovSwitchingModelǁforecast__mutmut_25,
        "xǁMarkovSwitchingModelǁforecast__mutmut_26": xǁMarkovSwitchingModelǁforecast__mutmut_26,
        "xǁMarkovSwitchingModelǁforecast__mutmut_27": xǁMarkovSwitchingModelǁforecast__mutmut_27,
        "xǁMarkovSwitchingModelǁforecast__mutmut_28": xǁMarkovSwitchingModelǁforecast__mutmut_28,
    }
    xǁMarkovSwitchingModelǁforecast__mutmut_orig.__name__ = "xǁMarkovSwitchingModelǁforecast"

    def simulate(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        args = [n, params, transition_matrix, seed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingModelǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingModelǁsimulate__mutmut_orig(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_1(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = None

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_2(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(None)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_3(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is not None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_4(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = None

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_5(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(None)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_6(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = None
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_7(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = None

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_8(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = None
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_9(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack(None)
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_10(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T + np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_11(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(None), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_12(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(None)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_13(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = None
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_14(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(None)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_15(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k - 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_16(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 2)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_17(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = None
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_18(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[+1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_19(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-2] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_20(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 2.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_21(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = None
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_22(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(None, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_23(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, None, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_24(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_25(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_26(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(
            a_mat,
            b,
        )[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_27(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[1]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_28(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = None
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_29(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(None, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_30(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, None)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_31(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_32(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(
            ergodic,
        )
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_33(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 1.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_34(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic = ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_35(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic *= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_36(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = None
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_37(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(None, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_38(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=None)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_39(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_40(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(
            n,
        )
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_41(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = None

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_42(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[1] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_43(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(None, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_44(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=None)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_45(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_46(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(
            k,
        )

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_47(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(None, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_48(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, None):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_49(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_50(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(
            1,
        ):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_51(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(2, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_52(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = None

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_53(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(None, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_54(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=None)

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_55(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_56(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(
                k,
            )

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_57(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t + 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_58(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 2]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_59(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = None
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_60(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(None)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_61(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = None
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_62(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros(None)
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_63(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(None):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_64(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = None

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_65(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 2.0

        return y, regimes.astype(np.float64), probs

    def xǁMarkovSwitchingModelǁsimulate__mutmut_66(
        self,
        n: int,
        params: NDArray[np.float64],
        transition_matrix: NDArray[np.float64] | None = None,
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Simulate data from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        transition_matrix : ndarray, optional
            Transition matrix. Extracted from params if None.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (y, regimes, probs) where:
            - y: simulated observations, shape (n,)
            - regimes: simulated regime sequence, shape (n,)
            - probs: regime probabilities, shape (n, k)
        """
        rng = np.random.default_rng(seed)

        if transition_matrix is None:
            transition_matrix = self._extract_transition_matrix(params)

        k = self.k_regimes
        trans = transition_matrix

        # Compute ergodic probabilities for initialization
        a_mat = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        ergodic = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        ergodic = np.maximum(ergodic, 0.0)
        ergodic /= ergodic.sum()

        # Simulate regime sequence
        regimes = np.zeros(n, dtype=np.int64)
        regimes[0] = rng.choice(k, p=ergodic)

        for t in range(1, n):
            regimes[t] = rng.choice(k, p=trans[regimes[t - 1]])

        # Simulate observations (subclass-specific, default is N(0,1))
        y = rng.standard_normal(n)
        probs = np.zeros((n, k))
        for t in range(n):
            probs[t, regimes[t]] = 1.0

        return y, regimes.astype(None), probs

    xǁMarkovSwitchingModelǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingModelǁsimulate__mutmut_1": xǁMarkovSwitchingModelǁsimulate__mutmut_1,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_2": xǁMarkovSwitchingModelǁsimulate__mutmut_2,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_3": xǁMarkovSwitchingModelǁsimulate__mutmut_3,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_4": xǁMarkovSwitchingModelǁsimulate__mutmut_4,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_5": xǁMarkovSwitchingModelǁsimulate__mutmut_5,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_6": xǁMarkovSwitchingModelǁsimulate__mutmut_6,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_7": xǁMarkovSwitchingModelǁsimulate__mutmut_7,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_8": xǁMarkovSwitchingModelǁsimulate__mutmut_8,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_9": xǁMarkovSwitchingModelǁsimulate__mutmut_9,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_10": xǁMarkovSwitchingModelǁsimulate__mutmut_10,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_11": xǁMarkovSwitchingModelǁsimulate__mutmut_11,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_12": xǁMarkovSwitchingModelǁsimulate__mutmut_12,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_13": xǁMarkovSwitchingModelǁsimulate__mutmut_13,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_14": xǁMarkovSwitchingModelǁsimulate__mutmut_14,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_15": xǁMarkovSwitchingModelǁsimulate__mutmut_15,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_16": xǁMarkovSwitchingModelǁsimulate__mutmut_16,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_17": xǁMarkovSwitchingModelǁsimulate__mutmut_17,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_18": xǁMarkovSwitchingModelǁsimulate__mutmut_18,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_19": xǁMarkovSwitchingModelǁsimulate__mutmut_19,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_20": xǁMarkovSwitchingModelǁsimulate__mutmut_20,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_21": xǁMarkovSwitchingModelǁsimulate__mutmut_21,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_22": xǁMarkovSwitchingModelǁsimulate__mutmut_22,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_23": xǁMarkovSwitchingModelǁsimulate__mutmut_23,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_24": xǁMarkovSwitchingModelǁsimulate__mutmut_24,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_25": xǁMarkovSwitchingModelǁsimulate__mutmut_25,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_26": xǁMarkovSwitchingModelǁsimulate__mutmut_26,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_27": xǁMarkovSwitchingModelǁsimulate__mutmut_27,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_28": xǁMarkovSwitchingModelǁsimulate__mutmut_28,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_29": xǁMarkovSwitchingModelǁsimulate__mutmut_29,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_30": xǁMarkovSwitchingModelǁsimulate__mutmut_30,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_31": xǁMarkovSwitchingModelǁsimulate__mutmut_31,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_32": xǁMarkovSwitchingModelǁsimulate__mutmut_32,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_33": xǁMarkovSwitchingModelǁsimulate__mutmut_33,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_34": xǁMarkovSwitchingModelǁsimulate__mutmut_34,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_35": xǁMarkovSwitchingModelǁsimulate__mutmut_35,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_36": xǁMarkovSwitchingModelǁsimulate__mutmut_36,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_37": xǁMarkovSwitchingModelǁsimulate__mutmut_37,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_38": xǁMarkovSwitchingModelǁsimulate__mutmut_38,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_39": xǁMarkovSwitchingModelǁsimulate__mutmut_39,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_40": xǁMarkovSwitchingModelǁsimulate__mutmut_40,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_41": xǁMarkovSwitchingModelǁsimulate__mutmut_41,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_42": xǁMarkovSwitchingModelǁsimulate__mutmut_42,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_43": xǁMarkovSwitchingModelǁsimulate__mutmut_43,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_44": xǁMarkovSwitchingModelǁsimulate__mutmut_44,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_45": xǁMarkovSwitchingModelǁsimulate__mutmut_45,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_46": xǁMarkovSwitchingModelǁsimulate__mutmut_46,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_47": xǁMarkovSwitchingModelǁsimulate__mutmut_47,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_48": xǁMarkovSwitchingModelǁsimulate__mutmut_48,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_49": xǁMarkovSwitchingModelǁsimulate__mutmut_49,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_50": xǁMarkovSwitchingModelǁsimulate__mutmut_50,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_51": xǁMarkovSwitchingModelǁsimulate__mutmut_51,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_52": xǁMarkovSwitchingModelǁsimulate__mutmut_52,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_53": xǁMarkovSwitchingModelǁsimulate__mutmut_53,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_54": xǁMarkovSwitchingModelǁsimulate__mutmut_54,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_55": xǁMarkovSwitchingModelǁsimulate__mutmut_55,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_56": xǁMarkovSwitchingModelǁsimulate__mutmut_56,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_57": xǁMarkovSwitchingModelǁsimulate__mutmut_57,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_58": xǁMarkovSwitchingModelǁsimulate__mutmut_58,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_59": xǁMarkovSwitchingModelǁsimulate__mutmut_59,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_60": xǁMarkovSwitchingModelǁsimulate__mutmut_60,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_61": xǁMarkovSwitchingModelǁsimulate__mutmut_61,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_62": xǁMarkovSwitchingModelǁsimulate__mutmut_62,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_63": xǁMarkovSwitchingModelǁsimulate__mutmut_63,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_64": xǁMarkovSwitchingModelǁsimulate__mutmut_64,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_65": xǁMarkovSwitchingModelǁsimulate__mutmut_65,
        "xǁMarkovSwitchingModelǁsimulate__mutmut_66": xǁMarkovSwitchingModelǁsimulate__mutmut_66,
    }
    xǁMarkovSwitchingModelǁsimulate__mutmut_orig.__name__ = "xǁMarkovSwitchingModelǁsimulate"

    def _extract_transition_matrix(self, params: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_orig(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_1(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = None
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_2(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = None
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_3(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k / (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_4(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k + 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_5(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 2)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_6(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = None

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_7(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[+n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_8(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = None
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_9(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros(None)
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_10(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = None
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_11(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 1
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_12(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(None):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_13(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(None):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_14(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i == j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_15(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = None
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_16(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 * (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_17(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 2.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_18(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 - np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_19(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (2.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_20(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(None))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_21(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(+trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_22(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx = 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_23(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx -= 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_24(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 2
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_25(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = None
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_26(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 + np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_27(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 2.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_28(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(None)
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_29(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] <= 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_30(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 1.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_31(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = None
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_32(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(None, 0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_33(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], None)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_34(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(0.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_35(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(
                    p_mat[i],
                )
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_36(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 1.01)
                p_mat[i] /= p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_37(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] = p_mat[i].sum()

        return p_mat

    def xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_38(
        self, params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Extract transition matrix from parameter vector.

        Default implementation: last k*(k-1) params are transition probs.
        Each row of P: [p_{i,0}, p_{i,1}, ..., p_{i,k-1}].
        Only k*(k-1) free params since rows sum to 1.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = self.k_regimes
        n_trans = k * (k - 1)
        trans_params = params[-n_trans:]

        p_mat = np.zeros((k, k))
        idx = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    p_mat[i, j] = 1.0 / (1.0 + np.exp(-trans_params[idx]))
                    idx += 1
            p_mat[i, i] = 1.0 - np.sum(p_mat[i, :])
            # Ensure valid probabilities
            if p_mat[i, i] < 0.01:
                p_mat[i] = np.maximum(p_mat[i], 0.01)
                p_mat[i] *= p_mat[i].sum()

        return p_mat

    xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_1": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_1,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_2": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_2,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_3": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_3,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_4": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_4,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_5": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_5,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_6": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_6,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_7": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_7,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_8": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_8,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_9": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_9,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_10": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_10,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_11": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_11,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_12": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_12,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_13": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_13,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_14": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_14,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_15": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_15,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_16": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_16,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_17": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_17,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_18": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_18,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_19": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_19,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_20": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_20,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_21": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_21,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_22": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_22,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_23": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_23,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_24": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_24,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_25": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_25,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_26": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_26,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_27": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_27,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_28": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_28,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_29": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_29,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_30": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_30,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_31": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_31,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_32": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_32,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_33": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_33,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_34": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_34,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_35": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_35,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_36": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_36,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_37": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_37,
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_38": xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_38,
    }
    xǁMarkovSwitchingModelǁ_extract_transition_matrix__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingModelǁ_extract_transition_matrix"
    )

    @staticmethod
    def _build_transition_matrix_from_diag(
        stay_probs: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Build transition matrix from staying probabilities (diagonal).

        For k=2: P = [[p00, 1-p00], [1-p11, p11]]

        Parameters
        ----------
        stay_probs : ndarray
            Staying probabilities [p_00, p_11, ...], shape (k,).

        Returns
        -------
        ndarray
            Transition matrix, shape (k, k).
        """
        k = len(stay_probs)
        p_mat = np.zeros((k, k))
        for i in range(k):
            p_mat[i, i] = stay_probs[i]
            off_diag = (1.0 - stay_probs[i]) / max(k - 1, 1)
            for j in range(k):
                if i != j:
                    p_mat[i, j] = off_diag
        return p_mat
