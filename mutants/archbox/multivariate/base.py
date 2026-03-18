"""Base class for multivariate volatility models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

if TYPE_CHECKING:
    pass
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


class MultivariateVolatilityModel(ABC):
    """Abstract base class for multivariate GARCH models.

    All multivariate models (DCC, CCC, BEKK, GO-GARCH, DECO) inherit from this class.

    Parameters
    ----------
    endog : ndarray
        Array of shape (T, k) with k return series.
    univariate_model : str
        Univariate GARCH variant to use for each series. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for the univariate GARCH. Default (1, 1).

    Attributes
    ----------
    endog : NDArray[np.float64]
        Returns array (T, k).
    T : int
        Number of observations.
    k : int
        Number of series.
    """

    model_name: str = "Unknown"

    def __init__(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        args = [endog, univariate_model, univariate_order]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivariateVolatilityModelǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMultivariateVolatilityModelǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁ__init____mutmut_orig(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_1(
        self,
        endog: Any,
        univariate_model: str = "XXGARCHXX",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_2(
        self,
        endog: Any,
        univariate_model: str = "garch",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_3(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = None
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_4(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(None, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_5(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=None)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_6(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_7(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(
            endog,
        )
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_8(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim == 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_9(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 3:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_10(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = None
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_11(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(None)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_12(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[2] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_13(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] <= 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_14(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 3:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_15(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = None
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_16(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[2]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_17(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(None)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_18(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[1] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_19(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] <= 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_20(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 21:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_21(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = None
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_22(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_23(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(None)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_24(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(None):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_25(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(None)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_26(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = None
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_27(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "XXendog contains NaN valuesXX"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_28(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains nan values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_29(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "ENDOG CONTAINS NAN VALUES"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_30(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(None)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_31(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(None):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_32(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(None)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_33(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = None
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_34(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "XXendog contains Inf valuesXX"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_35(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_36(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "ENDOG CONTAINS INF VALUES"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_37(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(None)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_38(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = None
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_39(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = None
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_40(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = None
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_41(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = None
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_42(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = True
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_43(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = ""
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_44(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = ""
        self._conditional_volatility: NDArray[np.float64] | None = None

    def xǁMultivariateVolatilityModelǁ__init____mutmut_45(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.endog = np.asarray(endog, dtype=np.float64)
        if self.endog.ndim != 2:
            msg = f"endog must be 2D (T, k), got {self.endog.ndim}D"
            raise ValueError(msg)
        if self.endog.shape[1] < 2:
            msg = f"Need at least 2 series, got {self.endog.shape[1]}"
            raise ValueError(msg)
        if self.endog.shape[0] < 20:
            msg = f"Need at least 20 observations, got {self.endog.shape[0]}"
            raise ValueError(msg)
        if np.any(np.isnan(self.endog)):
            msg = "endog contains NaN values"
            raise ValueError(msg)
        if np.any(np.isinf(self.endog)):
            msg = "endog contains Inf values"
            raise ValueError(msg)

        self.T, self.k = self.endog.shape
        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = ""

    xǁMultivariateVolatilityModelǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁ__init____mutmut_1": xǁMultivariateVolatilityModelǁ__init____mutmut_1,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_2": xǁMultivariateVolatilityModelǁ__init____mutmut_2,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_3": xǁMultivariateVolatilityModelǁ__init____mutmut_3,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_4": xǁMultivariateVolatilityModelǁ__init____mutmut_4,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_5": xǁMultivariateVolatilityModelǁ__init____mutmut_5,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_6": xǁMultivariateVolatilityModelǁ__init____mutmut_6,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_7": xǁMultivariateVolatilityModelǁ__init____mutmut_7,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_8": xǁMultivariateVolatilityModelǁ__init____mutmut_8,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_9": xǁMultivariateVolatilityModelǁ__init____mutmut_9,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_10": xǁMultivariateVolatilityModelǁ__init____mutmut_10,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_11": xǁMultivariateVolatilityModelǁ__init____mutmut_11,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_12": xǁMultivariateVolatilityModelǁ__init____mutmut_12,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_13": xǁMultivariateVolatilityModelǁ__init____mutmut_13,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_14": xǁMultivariateVolatilityModelǁ__init____mutmut_14,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_15": xǁMultivariateVolatilityModelǁ__init____mutmut_15,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_16": xǁMultivariateVolatilityModelǁ__init____mutmut_16,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_17": xǁMultivariateVolatilityModelǁ__init____mutmut_17,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_18": xǁMultivariateVolatilityModelǁ__init____mutmut_18,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_19": xǁMultivariateVolatilityModelǁ__init____mutmut_19,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_20": xǁMultivariateVolatilityModelǁ__init____mutmut_20,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_21": xǁMultivariateVolatilityModelǁ__init____mutmut_21,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_22": xǁMultivariateVolatilityModelǁ__init____mutmut_22,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_23": xǁMultivariateVolatilityModelǁ__init____mutmut_23,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_24": xǁMultivariateVolatilityModelǁ__init____mutmut_24,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_25": xǁMultivariateVolatilityModelǁ__init____mutmut_25,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_26": xǁMultivariateVolatilityModelǁ__init____mutmut_26,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_27": xǁMultivariateVolatilityModelǁ__init____mutmut_27,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_28": xǁMultivariateVolatilityModelǁ__init____mutmut_28,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_29": xǁMultivariateVolatilityModelǁ__init____mutmut_29,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_30": xǁMultivariateVolatilityModelǁ__init____mutmut_30,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_31": xǁMultivariateVolatilityModelǁ__init____mutmut_31,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_32": xǁMultivariateVolatilityModelǁ__init____mutmut_32,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_33": xǁMultivariateVolatilityModelǁ__init____mutmut_33,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_34": xǁMultivariateVolatilityModelǁ__init____mutmut_34,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_35": xǁMultivariateVolatilityModelǁ__init____mutmut_35,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_36": xǁMultivariateVolatilityModelǁ__init____mutmut_36,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_37": xǁMultivariateVolatilityModelǁ__init____mutmut_37,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_38": xǁMultivariateVolatilityModelǁ__init____mutmut_38,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_39": xǁMultivariateVolatilityModelǁ__init____mutmut_39,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_40": xǁMultivariateVolatilityModelǁ__init____mutmut_40,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_41": xǁMultivariateVolatilityModelǁ__init____mutmut_41,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_42": xǁMultivariateVolatilityModelǁ__init____mutmut_42,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_43": xǁMultivariateVolatilityModelǁ__init____mutmut_43,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_44": xǁMultivariateVolatilityModelǁ__init____mutmut_44,
        "xǁMultivariateVolatilityModelǁ__init____mutmut_45": xǁMultivariateVolatilityModelǁ__init____mutmut_45,
    }
    xǁMultivariateVolatilityModelǁ__init____mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁ__init__"
    )

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t.

        Parameters
        ----------
        params : ndarray
            Correlation model parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """

    @property
    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for correlation model optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names for the correlation model."""

    # --- Concrete methods ---

    def _fit_univariate(self) -> None:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_orig(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_1(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = None
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_2(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = None
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_3(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = None
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_4(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros(None)
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_5(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = None

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_6(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros(None)

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_7(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(None):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_8(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = None
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_9(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = None
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_10(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(None, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_11(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=None, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_12(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=None, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_13(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean=None)
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_14(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_15(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_16(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_17(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(
                series,
                p=p,
                q=q,
            )
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_18(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="XXconstantXX")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_19(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="CONSTANT")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_20(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = None
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_21(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=None)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_22(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=True)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_23(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(None)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_24(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = None
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_25(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = None
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_26(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = None
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_27(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids * sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_28(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = None

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_29(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = None
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_30(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = None
        self._conditional_volatility = cond_vol

    # --- Concrete methods ---

    def xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_31(self) -> None:
        """Fit univariate GARCH to each series (Step 1 of two-step).

        Populates self._univariate_results, self._std_resids,
        and self._conditional_volatility.
        """
        from archbox.models.garch import GARCH

        p, q = self.univariate_order
        results_list = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            series = self.endog[:, i]
            model = GARCH(series, p=p, q=q, mean="constant")
            res = model.fit(disp=False)
            results_list.append(res)

            # Standardized residuals: z_{i,t} = eps_{i,t} / sigma_{i,t}
            resids = res.resid
            sigma = res.conditional_volatility
            std_resids[:, i] = resids / sigma
            cond_vol[:, i] = sigma

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = None

    xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_1": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_1,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_2": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_2,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_3": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_3,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_4": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_4,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_5": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_5,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_6": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_6,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_7": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_7,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_8": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_8,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_9": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_9,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_10": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_10,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_11": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_11,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_12": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_12,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_13": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_13,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_14": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_14,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_15": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_15,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_16": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_16,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_17": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_17,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_18": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_18,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_19": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_19,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_20": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_20,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_21": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_21,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_22": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_22,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_23": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_23,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_24": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_24,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_25": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_25,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_26": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_26,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_27": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_27,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_28": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_28,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_29": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_29,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_30": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_30,
        "xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_31": xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_31,
    }
    xǁMultivariateVolatilityModelǁ_fit_univariate__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁ_fit_univariate"
    )

    def fit(self, method: str = "two_step", disp: bool = True) -> MultivarResults:
        args = [method, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivariateVolatilityModelǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁMultivariateVolatilityModelǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_orig(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_1(
        self, method: str = "XXtwo_stepXX", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_2(
        self, method: str = "TWO_STEP", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_3(
        self, method: str = "two_step", disp: bool = False
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_4(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_5(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_6(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_7(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = None

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_8(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(None, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_9(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=None)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_10(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_11(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(
            self._std_resids,
        )

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_12(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = None
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_13(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(None, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_14(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, None)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_15(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_16(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(
            params,
        )
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_17(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = None

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_18(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(None, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_19(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, None)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_20(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_21(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(
            corr_t,
        )

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_22(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = None

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_23(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(None, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_24(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, None, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_25(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, None)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_26(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_27(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_28(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(
            corr_t,
            self._std_resids,
        )

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_29(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = None
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_30(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(None)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_31(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = None
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_32(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = None

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_33(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params - n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_34(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = None
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_35(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike - 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_36(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 / loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_37(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = +2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_38(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -3.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_39(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 / n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_40(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 3.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_41(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = None

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_42(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike - np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_43(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 / loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_44(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = +2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_45(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -3.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_46(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) / n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_47(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(None) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_48(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = None

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_49(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = False

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_50(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=None,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_51(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=None,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_52(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=None,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_53(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=None,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_54(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=None,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_55(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=None,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_56(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=None,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_57(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=None,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_58(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=None,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_59(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=None,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_60(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=None,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_61(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=None,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_62(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_63(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_64(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_65(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_66(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_67(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_68(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_69(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_70(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_71(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_72(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_series=self.k,
        )

    def xǁMultivariateVolatilityModelǁfit__mutmut_73(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        params = self._estimate_correlation(self._std_resids, disp=disp)

        # Compute dynamic correlation and covariance
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_corr_params = len(params)
        n_total = n_univ_params + n_corr_params

        # Information criteria
        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
        )

    xǁMultivariateVolatilityModelǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁfit__mutmut_1": xǁMultivariateVolatilityModelǁfit__mutmut_1,
        "xǁMultivariateVolatilityModelǁfit__mutmut_2": xǁMultivariateVolatilityModelǁfit__mutmut_2,
        "xǁMultivariateVolatilityModelǁfit__mutmut_3": xǁMultivariateVolatilityModelǁfit__mutmut_3,
        "xǁMultivariateVolatilityModelǁfit__mutmut_4": xǁMultivariateVolatilityModelǁfit__mutmut_4,
        "xǁMultivariateVolatilityModelǁfit__mutmut_5": xǁMultivariateVolatilityModelǁfit__mutmut_5,
        "xǁMultivariateVolatilityModelǁfit__mutmut_6": xǁMultivariateVolatilityModelǁfit__mutmut_6,
        "xǁMultivariateVolatilityModelǁfit__mutmut_7": xǁMultivariateVolatilityModelǁfit__mutmut_7,
        "xǁMultivariateVolatilityModelǁfit__mutmut_8": xǁMultivariateVolatilityModelǁfit__mutmut_8,
        "xǁMultivariateVolatilityModelǁfit__mutmut_9": xǁMultivariateVolatilityModelǁfit__mutmut_9,
        "xǁMultivariateVolatilityModelǁfit__mutmut_10": xǁMultivariateVolatilityModelǁfit__mutmut_10,
        "xǁMultivariateVolatilityModelǁfit__mutmut_11": xǁMultivariateVolatilityModelǁfit__mutmut_11,
        "xǁMultivariateVolatilityModelǁfit__mutmut_12": xǁMultivariateVolatilityModelǁfit__mutmut_12,
        "xǁMultivariateVolatilityModelǁfit__mutmut_13": xǁMultivariateVolatilityModelǁfit__mutmut_13,
        "xǁMultivariateVolatilityModelǁfit__mutmut_14": xǁMultivariateVolatilityModelǁfit__mutmut_14,
        "xǁMultivariateVolatilityModelǁfit__mutmut_15": xǁMultivariateVolatilityModelǁfit__mutmut_15,
        "xǁMultivariateVolatilityModelǁfit__mutmut_16": xǁMultivariateVolatilityModelǁfit__mutmut_16,
        "xǁMultivariateVolatilityModelǁfit__mutmut_17": xǁMultivariateVolatilityModelǁfit__mutmut_17,
        "xǁMultivariateVolatilityModelǁfit__mutmut_18": xǁMultivariateVolatilityModelǁfit__mutmut_18,
        "xǁMultivariateVolatilityModelǁfit__mutmut_19": xǁMultivariateVolatilityModelǁfit__mutmut_19,
        "xǁMultivariateVolatilityModelǁfit__mutmut_20": xǁMultivariateVolatilityModelǁfit__mutmut_20,
        "xǁMultivariateVolatilityModelǁfit__mutmut_21": xǁMultivariateVolatilityModelǁfit__mutmut_21,
        "xǁMultivariateVolatilityModelǁfit__mutmut_22": xǁMultivariateVolatilityModelǁfit__mutmut_22,
        "xǁMultivariateVolatilityModelǁfit__mutmut_23": xǁMultivariateVolatilityModelǁfit__mutmut_23,
        "xǁMultivariateVolatilityModelǁfit__mutmut_24": xǁMultivariateVolatilityModelǁfit__mutmut_24,
        "xǁMultivariateVolatilityModelǁfit__mutmut_25": xǁMultivariateVolatilityModelǁfit__mutmut_25,
        "xǁMultivariateVolatilityModelǁfit__mutmut_26": xǁMultivariateVolatilityModelǁfit__mutmut_26,
        "xǁMultivariateVolatilityModelǁfit__mutmut_27": xǁMultivariateVolatilityModelǁfit__mutmut_27,
        "xǁMultivariateVolatilityModelǁfit__mutmut_28": xǁMultivariateVolatilityModelǁfit__mutmut_28,
        "xǁMultivariateVolatilityModelǁfit__mutmut_29": xǁMultivariateVolatilityModelǁfit__mutmut_29,
        "xǁMultivariateVolatilityModelǁfit__mutmut_30": xǁMultivariateVolatilityModelǁfit__mutmut_30,
        "xǁMultivariateVolatilityModelǁfit__mutmut_31": xǁMultivariateVolatilityModelǁfit__mutmut_31,
        "xǁMultivariateVolatilityModelǁfit__mutmut_32": xǁMultivariateVolatilityModelǁfit__mutmut_32,
        "xǁMultivariateVolatilityModelǁfit__mutmut_33": xǁMultivariateVolatilityModelǁfit__mutmut_33,
        "xǁMultivariateVolatilityModelǁfit__mutmut_34": xǁMultivariateVolatilityModelǁfit__mutmut_34,
        "xǁMultivariateVolatilityModelǁfit__mutmut_35": xǁMultivariateVolatilityModelǁfit__mutmut_35,
        "xǁMultivariateVolatilityModelǁfit__mutmut_36": xǁMultivariateVolatilityModelǁfit__mutmut_36,
        "xǁMultivariateVolatilityModelǁfit__mutmut_37": xǁMultivariateVolatilityModelǁfit__mutmut_37,
        "xǁMultivariateVolatilityModelǁfit__mutmut_38": xǁMultivariateVolatilityModelǁfit__mutmut_38,
        "xǁMultivariateVolatilityModelǁfit__mutmut_39": xǁMultivariateVolatilityModelǁfit__mutmut_39,
        "xǁMultivariateVolatilityModelǁfit__mutmut_40": xǁMultivariateVolatilityModelǁfit__mutmut_40,
        "xǁMultivariateVolatilityModelǁfit__mutmut_41": xǁMultivariateVolatilityModelǁfit__mutmut_41,
        "xǁMultivariateVolatilityModelǁfit__mutmut_42": xǁMultivariateVolatilityModelǁfit__mutmut_42,
        "xǁMultivariateVolatilityModelǁfit__mutmut_43": xǁMultivariateVolatilityModelǁfit__mutmut_43,
        "xǁMultivariateVolatilityModelǁfit__mutmut_44": xǁMultivariateVolatilityModelǁfit__mutmut_44,
        "xǁMultivariateVolatilityModelǁfit__mutmut_45": xǁMultivariateVolatilityModelǁfit__mutmut_45,
        "xǁMultivariateVolatilityModelǁfit__mutmut_46": xǁMultivariateVolatilityModelǁfit__mutmut_46,
        "xǁMultivariateVolatilityModelǁfit__mutmut_47": xǁMultivariateVolatilityModelǁfit__mutmut_47,
        "xǁMultivariateVolatilityModelǁfit__mutmut_48": xǁMultivariateVolatilityModelǁfit__mutmut_48,
        "xǁMultivariateVolatilityModelǁfit__mutmut_49": xǁMultivariateVolatilityModelǁfit__mutmut_49,
        "xǁMultivariateVolatilityModelǁfit__mutmut_50": xǁMultivariateVolatilityModelǁfit__mutmut_50,
        "xǁMultivariateVolatilityModelǁfit__mutmut_51": xǁMultivariateVolatilityModelǁfit__mutmut_51,
        "xǁMultivariateVolatilityModelǁfit__mutmut_52": xǁMultivariateVolatilityModelǁfit__mutmut_52,
        "xǁMultivariateVolatilityModelǁfit__mutmut_53": xǁMultivariateVolatilityModelǁfit__mutmut_53,
        "xǁMultivariateVolatilityModelǁfit__mutmut_54": xǁMultivariateVolatilityModelǁfit__mutmut_54,
        "xǁMultivariateVolatilityModelǁfit__mutmut_55": xǁMultivariateVolatilityModelǁfit__mutmut_55,
        "xǁMultivariateVolatilityModelǁfit__mutmut_56": xǁMultivariateVolatilityModelǁfit__mutmut_56,
        "xǁMultivariateVolatilityModelǁfit__mutmut_57": xǁMultivariateVolatilityModelǁfit__mutmut_57,
        "xǁMultivariateVolatilityModelǁfit__mutmut_58": xǁMultivariateVolatilityModelǁfit__mutmut_58,
        "xǁMultivariateVolatilityModelǁfit__mutmut_59": xǁMultivariateVolatilityModelǁfit__mutmut_59,
        "xǁMultivariateVolatilityModelǁfit__mutmut_60": xǁMultivariateVolatilityModelǁfit__mutmut_60,
        "xǁMultivariateVolatilityModelǁfit__mutmut_61": xǁMultivariateVolatilityModelǁfit__mutmut_61,
        "xǁMultivariateVolatilityModelǁfit__mutmut_62": xǁMultivariateVolatilityModelǁfit__mutmut_62,
        "xǁMultivariateVolatilityModelǁfit__mutmut_63": xǁMultivariateVolatilityModelǁfit__mutmut_63,
        "xǁMultivariateVolatilityModelǁfit__mutmut_64": xǁMultivariateVolatilityModelǁfit__mutmut_64,
        "xǁMultivariateVolatilityModelǁfit__mutmut_65": xǁMultivariateVolatilityModelǁfit__mutmut_65,
        "xǁMultivariateVolatilityModelǁfit__mutmut_66": xǁMultivariateVolatilityModelǁfit__mutmut_66,
        "xǁMultivariateVolatilityModelǁfit__mutmut_67": xǁMultivariateVolatilityModelǁfit__mutmut_67,
        "xǁMultivariateVolatilityModelǁfit__mutmut_68": xǁMultivariateVolatilityModelǁfit__mutmut_68,
        "xǁMultivariateVolatilityModelǁfit__mutmut_69": xǁMultivariateVolatilityModelǁfit__mutmut_69,
        "xǁMultivariateVolatilityModelǁfit__mutmut_70": xǁMultivariateVolatilityModelǁfit__mutmut_70,
        "xǁMultivariateVolatilityModelǁfit__mutmut_71": xǁMultivariateVolatilityModelǁfit__mutmut_71,
        "xǁMultivariateVolatilityModelǁfit__mutmut_72": xǁMultivariateVolatilityModelǁfit__mutmut_72,
        "xǁMultivariateVolatilityModelǁfit__mutmut_73": xǁMultivariateVolatilityModelǁfit__mutmut_73,
    }
    xǁMultivariateVolatilityModelǁfit__mutmut_orig.__name__ = "xǁMultivariateVolatilityModelǁfit"

    def _estimate_correlation(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        args = [std_resids, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_orig(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_1(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = False,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_2(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = None

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_3(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) != 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_4(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 1:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_5(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = None
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_6(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(None, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_7(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, None)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_8(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_9(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(
                params,
            )
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_10(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = None
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_11(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 1.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_12(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = None
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_13(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(None):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_14(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = None
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_15(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = None  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_16(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t - 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_17(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 2].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_18(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = None
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_19(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(None)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_20(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign < 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_21(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 1:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_22(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 10000000001.0
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_23(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = None
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_24(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(None, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_25(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, None)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_26(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_27(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(
                        r_mat,
                    )
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_28(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll = -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_29(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll -= -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_30(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 / (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_31(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += +0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_32(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -1.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_33(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) + float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_34(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet - float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_35(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(None) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_36(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(None))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_37(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 10000000001.0
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_38(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return +ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_39(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = None

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_40(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            None,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_41(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            None,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_42(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=None,
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_43(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=None,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_44(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options=None,
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_45(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_46(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_47(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_48(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_49(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_50(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="XXSLSQPXX",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_51(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="slsqp",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_52(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"XXmaxiterXX": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_53(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"MAXITER": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_54(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 501, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_55(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "XXdispXX": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_56(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "DISP": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_57(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "XXftolXX": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_58(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "FTOL": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_59(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1.00000001},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_60(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(None, dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_61(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=None)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_62(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(dtype=np.float64)

    def xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_63(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated correlation parameters.
        """
        x0 = self.start_params

        if len(x0) == 0:
            # No parameters to estimate (e.g., CCC)
            return x0

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for optimization."""
            corr_t = self._correlation_recursion(params, std_resids)
            ll = 0.0
            n_obs, _n_k = std_resids.shape
            for t in range(n_obs):
                r_mat = corr_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)
                try:
                    sign, logdet = np.linalg.slogdet(r_mat)
                    if sign <= 0:
                        return 1e10
                    r_inv = np.linalg.solve(r_mat, z)
                    ll += -0.5 * (logdet + float(z.T @ r_inv) - float(z.T @ z))
                except np.linalg.LinAlgError:
                    return 1e10
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(
            result.x,
        )

    xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_1": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_1,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_2": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_2,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_3": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_3,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_4": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_4,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_5": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_5,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_6": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_6,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_7": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_7,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_8": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_8,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_9": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_9,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_10": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_10,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_11": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_11,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_12": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_12,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_13": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_13,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_14": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_14,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_15": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_15,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_16": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_16,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_17": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_17,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_18": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_18,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_19": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_19,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_20": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_20,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_21": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_21,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_22": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_22,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_23": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_23,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_24": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_24,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_25": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_25,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_26": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_26,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_27": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_27,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_28": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_28,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_29": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_29,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_30": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_30,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_31": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_31,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_32": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_32,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_33": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_33,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_34": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_34,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_35": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_35,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_36": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_36,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_37": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_37,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_38": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_38,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_39": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_39,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_40": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_40,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_41": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_41,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_42": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_42,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_43": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_43,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_44": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_44,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_45": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_45,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_46": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_46,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_47": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_47,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_48": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_48,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_49": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_49,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_50": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_50,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_51": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_51,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_52": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_52,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_53": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_53,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_54": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_54,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_55": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_55,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_56": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_56,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_57": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_57,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_58": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_58,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_59": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_59,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_60": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_60,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_61": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_61,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_62": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_62,
        "xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_63": xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_63,
    }
    xǁMultivariateVolatilityModelǁ_estimate_correlation__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁ_estimate_correlation"
    )

    def _param_bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Default parameter bounds. Override in subclasses."""
        return [(1e-6, 0.999)] * len(self.start_params)

    def xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Default parameter bounds. Override in subclasses."""
        return [(1e-6, 0.999)] / len(self.start_params)

    def xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Default parameter bounds. Override in subclasses."""
        return [(1.000001, 0.999)] * len(self.start_params)

    def xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Default parameter bounds. Override in subclasses."""
        return [(1e-6, 1.999)] * len(self.start_params)

    xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_1": xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_1,
        "xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_2": xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_2,
        "xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_3": xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_3,
    }
    xǁMultivariateVolatilityModelǁ_param_bounds__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁ_param_bounds"
    )

    def _compute_covariance(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [corr_t, cond_vol]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_orig(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = np.zeros((n_obs, n_k, n_k))
        for t in range(n_obs):
            d_mat = np.diag(cond_vol[t])
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_1(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = None
        cov_t = np.zeros((n_obs, n_k, n_k))
        for t in range(n_obs):
            d_mat = np.diag(cond_vol[t])
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_2(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = None
        for t in range(n_obs):
            d_mat = np.diag(cond_vol[t])
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_3(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = np.zeros(None)
        for t in range(n_obs):
            d_mat = np.diag(cond_vol[t])
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_4(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = np.zeros((n_obs, n_k, n_k))
        for t in range(None):
            d_mat = np.diag(cond_vol[t])
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_5(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = np.zeros((n_obs, n_k, n_k))
        for t in range(n_obs):
            d_mat = None
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_6(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = np.zeros((n_obs, n_k, n_k))
        for t in range(n_obs):
            d_mat = np.diag(None)
            cov_t[t] = d_mat @ corr_t[t] @ d_mat
        return cov_t

    def xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_7(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        n_obs, n_k = cond_vol.shape
        cov_t = np.zeros((n_obs, n_k, n_k))
        for t in range(n_obs):
            d_mat = np.diag(cond_vol[t])
            cov_t[t] = None
        return cov_t

    xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_1": xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_1,
        "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_2": xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_2,
        "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_3": xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_3,
        "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_4": xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_4,
        "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_5": xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_5,
        "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_6": xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_6,
        "xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_7": xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_7,
    }
    xǁMultivariateVolatilityModelǁ_compute_covariance__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁ_compute_covariance"
    )

    def _loglikelihood(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        args = [corr_t, std_resids, cond_vol]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_orig(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_1(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = None
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_2(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = None
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_3(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 1.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_4(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = None

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_5(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k / np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_6(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(None)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_7(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 / np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_8(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(3.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_9(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(None):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_10(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = None
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_11(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(None)
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_12(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(None))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_13(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = None  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_14(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t - 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_15(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 2].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_16(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = None
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_17(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(None)
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_18(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign < 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_19(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 1:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_20(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return +1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_21(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -10000000001.0
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_22(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = None
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_23(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(None, z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_24(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], None)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_25(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_26(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(
                    corr_t[t],
                )
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_27(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = None
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_28(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(None)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_29(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return +1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_30(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -10000000001.0

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_31(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll = -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_32(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll -= -0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_33(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 / (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_34(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += +0.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_35(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -1.5 * (const + 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_36(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d + logdet_r - quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_37(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 * log_det_d - logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_38(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const - 2.0 * log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_39(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 2.0 / log_det_d + logdet_r + quad)

        return ll

    def xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_40(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood.
        """
        n_obs, n_k = std_resids.shape
        ll = 0.0
        const = n_k * np.log(2.0 * np.pi)

        for t in range(n_obs):
            log_det_d = np.sum(np.log(cond_vol[t]))
            z = std_resids[t : t + 1].T  # (k, 1)

            try:
                sign, logdet_r = np.linalg.slogdet(corr_t[t])
                if sign <= 0:
                    return -1e10
                r_inv_z = np.linalg.solve(corr_t[t], z)
                quad = float(z.T @ r_inv_z)
            except np.linalg.LinAlgError:
                return -1e10

            ll += -0.5 * (const + 3.0 * log_det_d + logdet_r + quad)

        return ll

    xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_1": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_1,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_2": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_2,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_3": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_3,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_4": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_4,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_5": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_5,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_6": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_6,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_7": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_7,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_8": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_8,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_9": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_9,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_10": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_10,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_11": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_11,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_12": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_12,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_13": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_13,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_14": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_14,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_15": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_15,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_16": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_16,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_17": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_17,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_18": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_18,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_19": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_19,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_20": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_20,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_21": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_21,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_22": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_22,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_23": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_23,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_24": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_24,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_25": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_25,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_26": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_26,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_27": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_27,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_28": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_28,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_29": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_29,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_30": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_30,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_31": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_31,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_32": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_32,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_33": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_33,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_34": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_34,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_35": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_35,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_36": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_36,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_37": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_37,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_38": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_38,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_39": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_39,
        "xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_40": xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_40,
    }
    xǁMultivariateVolatilityModelǁ_loglikelihood__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁ_loglikelihood"
    )

    def covariance(self, corr_t: NDArray[np.float64], t: int) -> NDArray[np.float64]:
        args = [corr_t, t]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivariateVolatilityModelǁcovariance__mutmut_orig"),
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁcovariance__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁcovariance__mutmut_orig(
        self, corr_t: NDArray[np.float64], t: int
    ) -> NDArray[np.float64]:
        """Get covariance matrix H_t at time t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        t : int
            Time index.

        Returns
        -------
        ndarray
            Covariance matrix (k, k).
        """
        assert self._conditional_volatility is not None
        d_mat = np.diag(self._conditional_volatility[t])
        return d_mat @ corr_t[t] @ d_mat

    def xǁMultivariateVolatilityModelǁcovariance__mutmut_1(
        self, corr_t: NDArray[np.float64], t: int
    ) -> NDArray[np.float64]:
        """Get covariance matrix H_t at time t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        t : int
            Time index.

        Returns
        -------
        ndarray
            Covariance matrix (k, k).
        """
        assert self._conditional_volatility is None
        d_mat = np.diag(self._conditional_volatility[t])
        return d_mat @ corr_t[t] @ d_mat

    def xǁMultivariateVolatilityModelǁcovariance__mutmut_2(
        self, corr_t: NDArray[np.float64], t: int
    ) -> NDArray[np.float64]:
        """Get covariance matrix H_t at time t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        t : int
            Time index.

        Returns
        -------
        ndarray
            Covariance matrix (k, k).
        """
        assert self._conditional_volatility is not None
        d_mat = None
        return d_mat @ corr_t[t] @ d_mat

    def xǁMultivariateVolatilityModelǁcovariance__mutmut_3(
        self, corr_t: NDArray[np.float64], t: int
    ) -> NDArray[np.float64]:
        """Get covariance matrix H_t at time t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        t : int
            Time index.

        Returns
        -------
        ndarray
            Covariance matrix (k, k).
        """
        assert self._conditional_volatility is not None
        d_mat = np.diag(None)
        return d_mat @ corr_t[t] @ d_mat

    xǁMultivariateVolatilityModelǁcovariance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁcovariance__mutmut_1": xǁMultivariateVolatilityModelǁcovariance__mutmut_1,
        "xǁMultivariateVolatilityModelǁcovariance__mutmut_2": xǁMultivariateVolatilityModelǁcovariance__mutmut_2,
        "xǁMultivariateVolatilityModelǁcovariance__mutmut_3": xǁMultivariateVolatilityModelǁcovariance__mutmut_3,
    }
    xǁMultivariateVolatilityModelǁcovariance__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁcovariance"
    )

    def correlation(self, corr_t: NDArray[np.float64], t: int) -> NDArray[np.float64]:
        """Get correlation matrix R_t at time t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        t : int
            Time index.

        Returns
        -------
        ndarray
            Correlation matrix (k, k).
        """
        return corr_t[t]

    def portfolio_variance(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [weights, cov_t]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_orig(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_1(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = None
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_2(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(None, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_3(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=None)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_4(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_5(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(
            weights,
        )
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_6(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = None
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_7(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[1]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_8(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = None
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_9(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(None)
        for t in range(n_obs):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_10(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(None):
            port_var[t] = float(w @ cov_t[t] @ w)
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_11(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = None
        return port_var

    def xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_12(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        n_obs = cov_t.shape[0]
        port_var = np.zeros(n_obs)
        for t in range(n_obs):
            port_var[t] = float(None)
        return port_var

    xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_1": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_1,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_2": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_2,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_3": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_3,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_4": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_4,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_5": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_5,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_6": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_6,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_7": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_7,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_8": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_8,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_9": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_9,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_10": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_10,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_11": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_11,
        "xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_12": xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_12,
    }
    xǁMultivariateVolatilityModelǁportfolio_variance__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁportfolio_variance"
    )

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        args = [results, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivariateVolatilityModelǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁMultivariateVolatilityModelǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateVolatilityModelǁforecast__mutmut_orig(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_1(
        self,
        results: MultivarResults,
        horizon: int = 11,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_2(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = None
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_3(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros(None)
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_4(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = None
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_5(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros(None)
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_6(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(None):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_7(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = None
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_8(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[+1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_9(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-2]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_10(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = None
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_11(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[+1]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_12(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-2]
        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_13(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"XXcovarianceXX": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_14(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"COVARIANCE": cov_forecast, "correlation": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_15(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "XXcorrelationXX": corr_forecast}

    def xǁMultivariateVolatilityModelǁforecast__mutmut_16(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., horizon.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation' (horizon, k, k).
        """
        # Default: return last observation repeated (subclasses should override)
        cov_forecast = np.zeros((horizon, self.k, self.k))
        corr_forecast = np.zeros((horizon, self.k, self.k))
        for h in range(horizon):
            cov_forecast[h] = results.dynamic_covariance[-1]
            corr_forecast[h] = results.dynamic_correlation[-1]
        return {"covariance": cov_forecast, "CORRELATION": corr_forecast}

    xǁMultivariateVolatilityModelǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateVolatilityModelǁforecast__mutmut_1": xǁMultivariateVolatilityModelǁforecast__mutmut_1,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_2": xǁMultivariateVolatilityModelǁforecast__mutmut_2,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_3": xǁMultivariateVolatilityModelǁforecast__mutmut_3,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_4": xǁMultivariateVolatilityModelǁforecast__mutmut_4,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_5": xǁMultivariateVolatilityModelǁforecast__mutmut_5,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_6": xǁMultivariateVolatilityModelǁforecast__mutmut_6,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_7": xǁMultivariateVolatilityModelǁforecast__mutmut_7,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_8": xǁMultivariateVolatilityModelǁforecast__mutmut_8,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_9": xǁMultivariateVolatilityModelǁforecast__mutmut_9,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_10": xǁMultivariateVolatilityModelǁforecast__mutmut_10,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_11": xǁMultivariateVolatilityModelǁforecast__mutmut_11,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_12": xǁMultivariateVolatilityModelǁforecast__mutmut_12,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_13": xǁMultivariateVolatilityModelǁforecast__mutmut_13,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_14": xǁMultivariateVolatilityModelǁforecast__mutmut_14,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_15": xǁMultivariateVolatilityModelǁforecast__mutmut_15,
        "xǁMultivariateVolatilityModelǁforecast__mutmut_16": xǁMultivariateVolatilityModelǁforecast__mutmut_16,
    }
    xǁMultivariateVolatilityModelǁforecast__mutmut_orig.__name__ = (
        "xǁMultivariateVolatilityModelǁforecast"
    )


class MultivarResults:
    """Container for multivariate GARCH results.

    Attributes
    ----------
    model : MultivariateVolatilityModel
        The fitted model.
    univariate_results : list
        List of ArchResults from each univariate GARCH.
    params : ndarray
        Correlation model parameters.
    dynamic_correlation : ndarray
        R_t for all t, shape (T, k, k).
    dynamic_covariance : ndarray
        H_t = D_t R_t D_t for all t, shape (T, k, k).
    conditional_volatility : ndarray
        sigma_{i,t} for each series, shape (T, k).
    std_resids : ndarray
        Standardized residuals z_t, shape (T, k).
    loglike : float
        Total log-likelihood.
    aic : float
        Akaike Information Criterion.
    bic : float
        Bayesian Information Criterion.
    n_obs : int
        Number of observations.
    n_series : int
        Number of series.
    """

    def __init__(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        args = [
            model,
            univariate_results,
            params,
            dynamic_correlation,
            dynamic_covariance,
            conditional_volatility,
            std_resids,
            loglike,
            aic,
            bic,
            n_obs,
            n_series,
        ]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivarResultsǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMultivarResultsǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivarResultsǁ__init____mutmut_orig(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_1(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = None
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_2(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = None
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_3(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = None
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_4(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = None
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_5(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = None
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_6(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = None
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_7(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = None
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_8(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = None
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_9(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = None
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_10(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = None
        self.n_obs = n_obs
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_11(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = None
        self.n_series = n_series

    def xǁMultivarResultsǁ__init____mutmut_12(  # noqa: PLR0913
        self,
        model: MultivariateVolatilityModel,
        univariate_results: list[Any],
        params: NDArray[np.float64],
        dynamic_correlation: NDArray[np.float64],
        dynamic_covariance: NDArray[np.float64],
        conditional_volatility: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        loglike: float,
        aic: float,
        bic: float,
        n_obs: int,
        n_series: int,
    ) -> None:
        """Initialize multivariate results container."""
        self.model = model
        self.univariate_results = univariate_results
        self.params = params
        self.dynamic_correlation = dynamic_correlation
        self.dynamic_covariance = dynamic_covariance
        self.conditional_volatility = conditional_volatility
        self.std_resids = std_resids
        self.loglike = loglike
        self.aic = aic
        self.bic = bic
        self.n_obs = n_obs
        self.n_series = None

    xǁMultivarResultsǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivarResultsǁ__init____mutmut_1": xǁMultivarResultsǁ__init____mutmut_1,
        "xǁMultivarResultsǁ__init____mutmut_2": xǁMultivarResultsǁ__init____mutmut_2,
        "xǁMultivarResultsǁ__init____mutmut_3": xǁMultivarResultsǁ__init____mutmut_3,
        "xǁMultivarResultsǁ__init____mutmut_4": xǁMultivarResultsǁ__init____mutmut_4,
        "xǁMultivarResultsǁ__init____mutmut_5": xǁMultivarResultsǁ__init____mutmut_5,
        "xǁMultivarResultsǁ__init____mutmut_6": xǁMultivarResultsǁ__init____mutmut_6,
        "xǁMultivarResultsǁ__init____mutmut_7": xǁMultivarResultsǁ__init____mutmut_7,
        "xǁMultivarResultsǁ__init____mutmut_8": xǁMultivarResultsǁ__init____mutmut_8,
        "xǁMultivarResultsǁ__init____mutmut_9": xǁMultivarResultsǁ__init____mutmut_9,
        "xǁMultivarResultsǁ__init____mutmut_10": xǁMultivarResultsǁ__init____mutmut_10,
        "xǁMultivarResultsǁ__init____mutmut_11": xǁMultivarResultsǁ__init____mutmut_11,
        "xǁMultivarResultsǁ__init____mutmut_12": xǁMultivarResultsǁ__init____mutmut_12,
    }
    xǁMultivarResultsǁ__init____mutmut_orig.__name__ = "xǁMultivarResultsǁ__init__"

    def summary(self) -> str:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivarResultsǁsummary__mutmut_orig"),
            object.__getattribute__(self, "xǁMultivarResultsǁsummary__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivarResultsǁsummary__mutmut_orig(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_1(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = None
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_2(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append(None)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_3(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" / 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_4(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("XX=XX" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_5(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 71)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_6(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(None)
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_7(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append(None)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_8(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" / 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_9(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("XX=XX" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_10(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 71)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_11(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(None)
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_12(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(None)
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_13(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(None)
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_14(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(None)
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_15(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(None)
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_16(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append(None)

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_17(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("XXXX")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_18(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append(None)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_19(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" / 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_20(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("XX-XX" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_21(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 71)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_22(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append(None)
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_23(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("XXUnivariate GARCH ParametersXX")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_24(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("univariate garch parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_25(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("UNIVARIATE GARCH PARAMETERS")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_26(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append(None)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_27(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" / 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_28(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("XX-XX" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_29(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 71)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_30(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(None):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_31(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(None)
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_32(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append(None)

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_33(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("XXXX")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_34(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) >= 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_35(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 1:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_36(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append(None)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_37(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" / 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_38(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("XX-XX" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_39(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 71)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_40(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append(None)
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_41(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("XXCorrelation Model ParametersXX")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_42(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("correlation model parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_43(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("CORRELATION MODEL PARAMETERS")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_44(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append(None)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_45(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" / 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_46(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("XX-XX" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_47(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 71)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_48(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(None, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_49(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, None, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_50(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=None):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_51(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_52(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_53(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(
                self.model.param_names,
                self.params,
                strict=False,
            ):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_54(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=True):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_55(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(None)
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_56(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append(None)
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_57(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("XXXX")
        lines.append("=" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_58(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append(None)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_59(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" / 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_60(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("XX=XX" * 70)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_61(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 71)

        return "\n".join(lines)

    def xǁMultivarResultsǁsummary__mutmut_62(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(None)

    def xǁMultivarResultsǁsummary__mutmut_63(self) -> str:
        """Generate summary table with univariate and multivariate parameters.

        Returns
        -------
        str
            Formatted summary string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"Multivariate GARCH Model: {self.model.model_name}")
        lines.append("=" * 70)
        lines.append(f"  Number of series:      {self.n_series}")
        lines.append(f"  Number of observations: {self.n_obs}")
        lines.append(f"  Log-likelihood:        {self.loglike:.4f}")
        lines.append(f"  AIC:                   {self.aic:.4f}")
        lines.append(f"  BIC:                   {self.bic:.4f}")
        lines.append("")

        # Univariate results
        lines.append("-" * 70)
        lines.append("Univariate GARCH Parameters")
        lines.append("-" * 70)
        for i, res in enumerate(self.univariate_results):
            lines.append(f"  Series {i}: {res.params}")
        lines.append("")

        # Correlation parameters
        if len(self.params) > 0:
            lines.append("-" * 70)
            lines.append("Correlation Model Parameters")
            lines.append("-" * 70)
            for name, val in zip(self.model.param_names, self.params, strict=False):
                lines.append(f"  {name:>12s}: {val:.6f}")
        lines.append("")
        lines.append("=" * 70)

        return "XX\nXX".join(lines)

    xǁMultivarResultsǁsummary__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivarResultsǁsummary__mutmut_1": xǁMultivarResultsǁsummary__mutmut_1,
        "xǁMultivarResultsǁsummary__mutmut_2": xǁMultivarResultsǁsummary__mutmut_2,
        "xǁMultivarResultsǁsummary__mutmut_3": xǁMultivarResultsǁsummary__mutmut_3,
        "xǁMultivarResultsǁsummary__mutmut_4": xǁMultivarResultsǁsummary__mutmut_4,
        "xǁMultivarResultsǁsummary__mutmut_5": xǁMultivarResultsǁsummary__mutmut_5,
        "xǁMultivarResultsǁsummary__mutmut_6": xǁMultivarResultsǁsummary__mutmut_6,
        "xǁMultivarResultsǁsummary__mutmut_7": xǁMultivarResultsǁsummary__mutmut_7,
        "xǁMultivarResultsǁsummary__mutmut_8": xǁMultivarResultsǁsummary__mutmut_8,
        "xǁMultivarResultsǁsummary__mutmut_9": xǁMultivarResultsǁsummary__mutmut_9,
        "xǁMultivarResultsǁsummary__mutmut_10": xǁMultivarResultsǁsummary__mutmut_10,
        "xǁMultivarResultsǁsummary__mutmut_11": xǁMultivarResultsǁsummary__mutmut_11,
        "xǁMultivarResultsǁsummary__mutmut_12": xǁMultivarResultsǁsummary__mutmut_12,
        "xǁMultivarResultsǁsummary__mutmut_13": xǁMultivarResultsǁsummary__mutmut_13,
        "xǁMultivarResultsǁsummary__mutmut_14": xǁMultivarResultsǁsummary__mutmut_14,
        "xǁMultivarResultsǁsummary__mutmut_15": xǁMultivarResultsǁsummary__mutmut_15,
        "xǁMultivarResultsǁsummary__mutmut_16": xǁMultivarResultsǁsummary__mutmut_16,
        "xǁMultivarResultsǁsummary__mutmut_17": xǁMultivarResultsǁsummary__mutmut_17,
        "xǁMultivarResultsǁsummary__mutmut_18": xǁMultivarResultsǁsummary__mutmut_18,
        "xǁMultivarResultsǁsummary__mutmut_19": xǁMultivarResultsǁsummary__mutmut_19,
        "xǁMultivarResultsǁsummary__mutmut_20": xǁMultivarResultsǁsummary__mutmut_20,
        "xǁMultivarResultsǁsummary__mutmut_21": xǁMultivarResultsǁsummary__mutmut_21,
        "xǁMultivarResultsǁsummary__mutmut_22": xǁMultivarResultsǁsummary__mutmut_22,
        "xǁMultivarResultsǁsummary__mutmut_23": xǁMultivarResultsǁsummary__mutmut_23,
        "xǁMultivarResultsǁsummary__mutmut_24": xǁMultivarResultsǁsummary__mutmut_24,
        "xǁMultivarResultsǁsummary__mutmut_25": xǁMultivarResultsǁsummary__mutmut_25,
        "xǁMultivarResultsǁsummary__mutmut_26": xǁMultivarResultsǁsummary__mutmut_26,
        "xǁMultivarResultsǁsummary__mutmut_27": xǁMultivarResultsǁsummary__mutmut_27,
        "xǁMultivarResultsǁsummary__mutmut_28": xǁMultivarResultsǁsummary__mutmut_28,
        "xǁMultivarResultsǁsummary__mutmut_29": xǁMultivarResultsǁsummary__mutmut_29,
        "xǁMultivarResultsǁsummary__mutmut_30": xǁMultivarResultsǁsummary__mutmut_30,
        "xǁMultivarResultsǁsummary__mutmut_31": xǁMultivarResultsǁsummary__mutmut_31,
        "xǁMultivarResultsǁsummary__mutmut_32": xǁMultivarResultsǁsummary__mutmut_32,
        "xǁMultivarResultsǁsummary__mutmut_33": xǁMultivarResultsǁsummary__mutmut_33,
        "xǁMultivarResultsǁsummary__mutmut_34": xǁMultivarResultsǁsummary__mutmut_34,
        "xǁMultivarResultsǁsummary__mutmut_35": xǁMultivarResultsǁsummary__mutmut_35,
        "xǁMultivarResultsǁsummary__mutmut_36": xǁMultivarResultsǁsummary__mutmut_36,
        "xǁMultivarResultsǁsummary__mutmut_37": xǁMultivarResultsǁsummary__mutmut_37,
        "xǁMultivarResultsǁsummary__mutmut_38": xǁMultivarResultsǁsummary__mutmut_38,
        "xǁMultivarResultsǁsummary__mutmut_39": xǁMultivarResultsǁsummary__mutmut_39,
        "xǁMultivarResultsǁsummary__mutmut_40": xǁMultivarResultsǁsummary__mutmut_40,
        "xǁMultivarResultsǁsummary__mutmut_41": xǁMultivarResultsǁsummary__mutmut_41,
        "xǁMultivarResultsǁsummary__mutmut_42": xǁMultivarResultsǁsummary__mutmut_42,
        "xǁMultivarResultsǁsummary__mutmut_43": xǁMultivarResultsǁsummary__mutmut_43,
        "xǁMultivarResultsǁsummary__mutmut_44": xǁMultivarResultsǁsummary__mutmut_44,
        "xǁMultivarResultsǁsummary__mutmut_45": xǁMultivarResultsǁsummary__mutmut_45,
        "xǁMultivarResultsǁsummary__mutmut_46": xǁMultivarResultsǁsummary__mutmut_46,
        "xǁMultivarResultsǁsummary__mutmut_47": xǁMultivarResultsǁsummary__mutmut_47,
        "xǁMultivarResultsǁsummary__mutmut_48": xǁMultivarResultsǁsummary__mutmut_48,
        "xǁMultivarResultsǁsummary__mutmut_49": xǁMultivarResultsǁsummary__mutmut_49,
        "xǁMultivarResultsǁsummary__mutmut_50": xǁMultivarResultsǁsummary__mutmut_50,
        "xǁMultivarResultsǁsummary__mutmut_51": xǁMultivarResultsǁsummary__mutmut_51,
        "xǁMultivarResultsǁsummary__mutmut_52": xǁMultivarResultsǁsummary__mutmut_52,
        "xǁMultivarResultsǁsummary__mutmut_53": xǁMultivarResultsǁsummary__mutmut_53,
        "xǁMultivarResultsǁsummary__mutmut_54": xǁMultivarResultsǁsummary__mutmut_54,
        "xǁMultivarResultsǁsummary__mutmut_55": xǁMultivarResultsǁsummary__mutmut_55,
        "xǁMultivarResultsǁsummary__mutmut_56": xǁMultivarResultsǁsummary__mutmut_56,
        "xǁMultivarResultsǁsummary__mutmut_57": xǁMultivarResultsǁsummary__mutmut_57,
        "xǁMultivarResultsǁsummary__mutmut_58": xǁMultivarResultsǁsummary__mutmut_58,
        "xǁMultivarResultsǁsummary__mutmut_59": xǁMultivarResultsǁsummary__mutmut_59,
        "xǁMultivarResultsǁsummary__mutmut_60": xǁMultivarResultsǁsummary__mutmut_60,
        "xǁMultivarResultsǁsummary__mutmut_61": xǁMultivarResultsǁsummary__mutmut_61,
        "xǁMultivarResultsǁsummary__mutmut_62": xǁMultivarResultsǁsummary__mutmut_62,
        "xǁMultivarResultsǁsummary__mutmut_63": xǁMultivarResultsǁsummary__mutmut_63,
    }
    xǁMultivarResultsǁsummary__mutmut_orig.__name__ = "xǁMultivarResultsǁsummary"

    def plot_correlation(self, i: int, j: int) -> None:
        args = [i, j]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivarResultsǁplot_correlation__mutmut_orig"),
            object.__getattribute__(self, "xǁMultivarResultsǁplot_correlation__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivarResultsǁplot_correlation__mutmut_orig(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_1(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = None
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_2(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = None
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_3(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=None)
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_4(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(13, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_5(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_6(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(None, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_7(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=None)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_8(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_9(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(
            rho,
        )
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_10(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=1.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_11(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(None)
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_12(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel(None)
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_13(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("XXTimeXX")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_14(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_15(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("TIME")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_16(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel(None)
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_17(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("XXCorrelationXX")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_18(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_19(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("CORRELATION")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_20(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=None, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_21(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color=None, linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_22(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle=None, linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_23(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=None)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_24(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_25(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_26(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_27(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(
            y=0,
            color="gray",
            linestyle="--",
        )
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_28(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=1, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_29(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="XXgrayXX", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_30(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="GRAY", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_31(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="XX--XX", linewidth=0.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_32(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=1.5)
        ax.set_ylim(-1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_33(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(None, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_34(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, None)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_35(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_36(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(
            -1.05,
        )
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_37(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(+1.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_38(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-2.05, 1.05)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_correlation__mutmut_39(self, i: int, j: int) -> None:
        """Plot dynamic correlation between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        rho = self.dynamic_correlation[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rho, linewidth=0.8)
        ax.set_title(f"Dynamic Correlation: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Correlation")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        ax.set_ylim(-1.05, 2.05)
        fig.tight_layout()
        plt.show()

    xǁMultivarResultsǁplot_correlation__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivarResultsǁplot_correlation__mutmut_1": xǁMultivarResultsǁplot_correlation__mutmut_1,
        "xǁMultivarResultsǁplot_correlation__mutmut_2": xǁMultivarResultsǁplot_correlation__mutmut_2,
        "xǁMultivarResultsǁplot_correlation__mutmut_3": xǁMultivarResultsǁplot_correlation__mutmut_3,
        "xǁMultivarResultsǁplot_correlation__mutmut_4": xǁMultivarResultsǁplot_correlation__mutmut_4,
        "xǁMultivarResultsǁplot_correlation__mutmut_5": xǁMultivarResultsǁplot_correlation__mutmut_5,
        "xǁMultivarResultsǁplot_correlation__mutmut_6": xǁMultivarResultsǁplot_correlation__mutmut_6,
        "xǁMultivarResultsǁplot_correlation__mutmut_7": xǁMultivarResultsǁplot_correlation__mutmut_7,
        "xǁMultivarResultsǁplot_correlation__mutmut_8": xǁMultivarResultsǁplot_correlation__mutmut_8,
        "xǁMultivarResultsǁplot_correlation__mutmut_9": xǁMultivarResultsǁplot_correlation__mutmut_9,
        "xǁMultivarResultsǁplot_correlation__mutmut_10": xǁMultivarResultsǁplot_correlation__mutmut_10,
        "xǁMultivarResultsǁplot_correlation__mutmut_11": xǁMultivarResultsǁplot_correlation__mutmut_11,
        "xǁMultivarResultsǁplot_correlation__mutmut_12": xǁMultivarResultsǁplot_correlation__mutmut_12,
        "xǁMultivarResultsǁplot_correlation__mutmut_13": xǁMultivarResultsǁplot_correlation__mutmut_13,
        "xǁMultivarResultsǁplot_correlation__mutmut_14": xǁMultivarResultsǁplot_correlation__mutmut_14,
        "xǁMultivarResultsǁplot_correlation__mutmut_15": xǁMultivarResultsǁplot_correlation__mutmut_15,
        "xǁMultivarResultsǁplot_correlation__mutmut_16": xǁMultivarResultsǁplot_correlation__mutmut_16,
        "xǁMultivarResultsǁplot_correlation__mutmut_17": xǁMultivarResultsǁplot_correlation__mutmut_17,
        "xǁMultivarResultsǁplot_correlation__mutmut_18": xǁMultivarResultsǁplot_correlation__mutmut_18,
        "xǁMultivarResultsǁplot_correlation__mutmut_19": xǁMultivarResultsǁplot_correlation__mutmut_19,
        "xǁMultivarResultsǁplot_correlation__mutmut_20": xǁMultivarResultsǁplot_correlation__mutmut_20,
        "xǁMultivarResultsǁplot_correlation__mutmut_21": xǁMultivarResultsǁplot_correlation__mutmut_21,
        "xǁMultivarResultsǁplot_correlation__mutmut_22": xǁMultivarResultsǁplot_correlation__mutmut_22,
        "xǁMultivarResultsǁplot_correlation__mutmut_23": xǁMultivarResultsǁplot_correlation__mutmut_23,
        "xǁMultivarResultsǁplot_correlation__mutmut_24": xǁMultivarResultsǁplot_correlation__mutmut_24,
        "xǁMultivarResultsǁplot_correlation__mutmut_25": xǁMultivarResultsǁplot_correlation__mutmut_25,
        "xǁMultivarResultsǁplot_correlation__mutmut_26": xǁMultivarResultsǁplot_correlation__mutmut_26,
        "xǁMultivarResultsǁplot_correlation__mutmut_27": xǁMultivarResultsǁplot_correlation__mutmut_27,
        "xǁMultivarResultsǁplot_correlation__mutmut_28": xǁMultivarResultsǁplot_correlation__mutmut_28,
        "xǁMultivarResultsǁplot_correlation__mutmut_29": xǁMultivarResultsǁplot_correlation__mutmut_29,
        "xǁMultivarResultsǁplot_correlation__mutmut_30": xǁMultivarResultsǁplot_correlation__mutmut_30,
        "xǁMultivarResultsǁplot_correlation__mutmut_31": xǁMultivarResultsǁplot_correlation__mutmut_31,
        "xǁMultivarResultsǁplot_correlation__mutmut_32": xǁMultivarResultsǁplot_correlation__mutmut_32,
        "xǁMultivarResultsǁplot_correlation__mutmut_33": xǁMultivarResultsǁplot_correlation__mutmut_33,
        "xǁMultivarResultsǁplot_correlation__mutmut_34": xǁMultivarResultsǁplot_correlation__mutmut_34,
        "xǁMultivarResultsǁplot_correlation__mutmut_35": xǁMultivarResultsǁplot_correlation__mutmut_35,
        "xǁMultivarResultsǁplot_correlation__mutmut_36": xǁMultivarResultsǁplot_correlation__mutmut_36,
        "xǁMultivarResultsǁplot_correlation__mutmut_37": xǁMultivarResultsǁplot_correlation__mutmut_37,
        "xǁMultivarResultsǁplot_correlation__mutmut_38": xǁMultivarResultsǁplot_correlation__mutmut_38,
        "xǁMultivarResultsǁplot_correlation__mutmut_39": xǁMultivarResultsǁplot_correlation__mutmut_39,
    }
    xǁMultivarResultsǁplot_correlation__mutmut_orig.__name__ = "xǁMultivarResultsǁplot_correlation"

    def plot_covariance(self, i: int, j: int) -> None:
        args = [i, j]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivarResultsǁplot_covariance__mutmut_orig"),
            object.__getattribute__(self, "xǁMultivarResultsǁplot_covariance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivarResultsǁplot_covariance__mutmut_orig(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_1(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = None
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_2(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = None
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_3(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=None)
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_4(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(13, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_5(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_6(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(None, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_7(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=None)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_8(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_9(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(
            cov,
        )
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_10(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=1.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_11(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(None)
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_12(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel(None)
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_13(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("XXTimeXX")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_14(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_15(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("TIME")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_16(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel(None)
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_17(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("XXCovarianceXX")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_18(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_19(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("COVARIANCE")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_20(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=None, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_21(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color=None, linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_22(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle=None, linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_23(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=None)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_24(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_25(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_26(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_27(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(
            y=0,
            color="gray",
            linestyle="--",
        )
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_28(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=1, color="gray", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_29(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="XXgrayXX", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_30(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="GRAY", linestyle="--", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_31(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="XX--XX", linewidth=0.5)
        fig.tight_layout()
        plt.show()

    def xǁMultivarResultsǁplot_covariance__mutmut_32(self, i: int, j: int) -> None:
        """Plot dynamic covariance between series i and j.

        Parameters
        ----------
        i : int
            First series index.
        j : int
            Second series index.
        """
        import matplotlib.pyplot as plt

        cov = self.dynamic_covariance[:, i, j]
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(cov, linewidth=0.8)
        ax.set_title(f"Dynamic Covariance: Series {i} vs Series {j}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Covariance")
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=1.5)
        fig.tight_layout()
        plt.show()

    xǁMultivarResultsǁplot_covariance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivarResultsǁplot_covariance__mutmut_1": xǁMultivarResultsǁplot_covariance__mutmut_1,
        "xǁMultivarResultsǁplot_covariance__mutmut_2": xǁMultivarResultsǁplot_covariance__mutmut_2,
        "xǁMultivarResultsǁplot_covariance__mutmut_3": xǁMultivarResultsǁplot_covariance__mutmut_3,
        "xǁMultivarResultsǁplot_covariance__mutmut_4": xǁMultivarResultsǁplot_covariance__mutmut_4,
        "xǁMultivarResultsǁplot_covariance__mutmut_5": xǁMultivarResultsǁplot_covariance__mutmut_5,
        "xǁMultivarResultsǁplot_covariance__mutmut_6": xǁMultivarResultsǁplot_covariance__mutmut_6,
        "xǁMultivarResultsǁplot_covariance__mutmut_7": xǁMultivarResultsǁplot_covariance__mutmut_7,
        "xǁMultivarResultsǁplot_covariance__mutmut_8": xǁMultivarResultsǁplot_covariance__mutmut_8,
        "xǁMultivarResultsǁplot_covariance__mutmut_9": xǁMultivarResultsǁplot_covariance__mutmut_9,
        "xǁMultivarResultsǁplot_covariance__mutmut_10": xǁMultivarResultsǁplot_covariance__mutmut_10,
        "xǁMultivarResultsǁplot_covariance__mutmut_11": xǁMultivarResultsǁplot_covariance__mutmut_11,
        "xǁMultivarResultsǁplot_covariance__mutmut_12": xǁMultivarResultsǁplot_covariance__mutmut_12,
        "xǁMultivarResultsǁplot_covariance__mutmut_13": xǁMultivarResultsǁplot_covariance__mutmut_13,
        "xǁMultivarResultsǁplot_covariance__mutmut_14": xǁMultivarResultsǁplot_covariance__mutmut_14,
        "xǁMultivarResultsǁplot_covariance__mutmut_15": xǁMultivarResultsǁplot_covariance__mutmut_15,
        "xǁMultivarResultsǁplot_covariance__mutmut_16": xǁMultivarResultsǁplot_covariance__mutmut_16,
        "xǁMultivarResultsǁplot_covariance__mutmut_17": xǁMultivarResultsǁplot_covariance__mutmut_17,
        "xǁMultivarResultsǁplot_covariance__mutmut_18": xǁMultivarResultsǁplot_covariance__mutmut_18,
        "xǁMultivarResultsǁplot_covariance__mutmut_19": xǁMultivarResultsǁplot_covariance__mutmut_19,
        "xǁMultivarResultsǁplot_covariance__mutmut_20": xǁMultivarResultsǁplot_covariance__mutmut_20,
        "xǁMultivarResultsǁplot_covariance__mutmut_21": xǁMultivarResultsǁplot_covariance__mutmut_21,
        "xǁMultivarResultsǁplot_covariance__mutmut_22": xǁMultivarResultsǁplot_covariance__mutmut_22,
        "xǁMultivarResultsǁplot_covariance__mutmut_23": xǁMultivarResultsǁplot_covariance__mutmut_23,
        "xǁMultivarResultsǁplot_covariance__mutmut_24": xǁMultivarResultsǁplot_covariance__mutmut_24,
        "xǁMultivarResultsǁplot_covariance__mutmut_25": xǁMultivarResultsǁplot_covariance__mutmut_25,
        "xǁMultivarResultsǁplot_covariance__mutmut_26": xǁMultivarResultsǁplot_covariance__mutmut_26,
        "xǁMultivarResultsǁplot_covariance__mutmut_27": xǁMultivarResultsǁplot_covariance__mutmut_27,
        "xǁMultivarResultsǁplot_covariance__mutmut_28": xǁMultivarResultsǁplot_covariance__mutmut_28,
        "xǁMultivarResultsǁplot_covariance__mutmut_29": xǁMultivarResultsǁplot_covariance__mutmut_29,
        "xǁMultivarResultsǁplot_covariance__mutmut_30": xǁMultivarResultsǁplot_covariance__mutmut_30,
        "xǁMultivarResultsǁplot_covariance__mutmut_31": xǁMultivarResultsǁplot_covariance__mutmut_31,
        "xǁMultivarResultsǁplot_covariance__mutmut_32": xǁMultivarResultsǁplot_covariance__mutmut_32,
    }
    xǁMultivarResultsǁplot_covariance__mutmut_orig.__name__ = "xǁMultivarResultsǁplot_covariance"

    def portfolio_volatility(self, weights: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [weights]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivarResultsǁportfolio_volatility__mutmut_orig"),
            object.__getattribute__(self, "xǁMultivarResultsǁportfolio_volatility__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivarResultsǁportfolio_volatility__mutmut_orig(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(np.maximum(port_var, 0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_1(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = None
        return np.sqrt(np.maximum(port_var, 0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_2(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(None, self.dynamic_covariance)
        return np.sqrt(np.maximum(port_var, 0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_3(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, None)
        return np.sqrt(np.maximum(port_var, 0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_4(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(self.dynamic_covariance)
        return np.sqrt(np.maximum(port_var, 0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_5(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(
            weights,
        )
        return np.sqrt(np.maximum(port_var, 0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_6(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(None)

    def xǁMultivarResultsǁportfolio_volatility__mutmut_7(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(np.maximum(None, 0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_8(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(np.maximum(port_var, None))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_9(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(np.maximum(0.0))

    def xǁMultivarResultsǁportfolio_volatility__mutmut_10(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(
            np.maximum(
                port_var,
            )
        )

    def xǁMultivarResultsǁportfolio_volatility__mutmut_11(
        self, weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Compute portfolio volatility series.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).

        Returns
        -------
        ndarray
            Portfolio volatility (standard deviation) series (T,).
        """
        port_var = self.model.portfolio_variance(weights, self.dynamic_covariance)
        return np.sqrt(np.maximum(port_var, 1.0))

    xǁMultivarResultsǁportfolio_volatility__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivarResultsǁportfolio_volatility__mutmut_1": xǁMultivarResultsǁportfolio_volatility__mutmut_1,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_2": xǁMultivarResultsǁportfolio_volatility__mutmut_2,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_3": xǁMultivarResultsǁportfolio_volatility__mutmut_3,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_4": xǁMultivarResultsǁportfolio_volatility__mutmut_4,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_5": xǁMultivarResultsǁportfolio_volatility__mutmut_5,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_6": xǁMultivarResultsǁportfolio_volatility__mutmut_6,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_7": xǁMultivarResultsǁportfolio_volatility__mutmut_7,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_8": xǁMultivarResultsǁportfolio_volatility__mutmut_8,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_9": xǁMultivarResultsǁportfolio_volatility__mutmut_9,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_10": xǁMultivarResultsǁportfolio_volatility__mutmut_10,
        "xǁMultivarResultsǁportfolio_volatility__mutmut_11": xǁMultivarResultsǁportfolio_volatility__mutmut_11,
    }
    xǁMultivarResultsǁportfolio_volatility__mutmut_orig.__name__ = (
        "xǁMultivarResultsǁportfolio_volatility"
    )
