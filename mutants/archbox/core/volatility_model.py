"""Base class for volatility models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

from archbox.utils.validation import validate_returns

if TYPE_CHECKING:
    from archbox.distributions.base import Distribution
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


class VolatilityModel(ABC):
    """Abstract base class for volatility models.

    All volatility models (GARCH, EGARCH, GJR-GARCH, etc.) inherit from this class.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' (demean) or 'zero'.
    dist : str
        Conditional distribution: 'normal', 'studentt', 'skewt'.

    Attributes
    ----------
    endog : NDArray[np.float64]
        Returns (demeaned if mean='constant').
    nobs : int
        Number of observations.
    dist : Distribution
        Conditional distribution instance.
    volatility_process : str
        Name of the volatility process.
    mu : float
        Estimated mean (0 if mean='zero').
    """

    volatility_process: str = "Unknown"

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        args = [endog, mean, dist]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVolatilityModelǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁVolatilityModelǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVolatilityModelǁ__init____mutmut_orig(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_1(
        self,
        endog: Any,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_2(
        self,
        endog: Any,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_3(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_4(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_5(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = None

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_6(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(None)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_7(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = None
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_8(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean != "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_9(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "XXconstantXX":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_10(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "CONSTANT":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_11(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = None
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_12(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(None)
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_13(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(None))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_14(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = None
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_15(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw + self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_16(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean != "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_17(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "XXzeroXX":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_18(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "ZERO":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_19(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = None
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_20(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 1.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_21(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = None
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_22(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = None
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_23(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(None)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_24(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = None
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_25(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = None
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_26(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = None
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_27(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(None)
        self._is_fitted = False

    def xǁVolatilityModelǁ__init____mutmut_28(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = None

    def xǁVolatilityModelǁ__init____mutmut_29(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = True

    xǁVolatilityModelǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVolatilityModelǁ__init____mutmut_1": xǁVolatilityModelǁ__init____mutmut_1,
        "xǁVolatilityModelǁ__init____mutmut_2": xǁVolatilityModelǁ__init____mutmut_2,
        "xǁVolatilityModelǁ__init____mutmut_3": xǁVolatilityModelǁ__init____mutmut_3,
        "xǁVolatilityModelǁ__init____mutmut_4": xǁVolatilityModelǁ__init____mutmut_4,
        "xǁVolatilityModelǁ__init____mutmut_5": xǁVolatilityModelǁ__init____mutmut_5,
        "xǁVolatilityModelǁ__init____mutmut_6": xǁVolatilityModelǁ__init____mutmut_6,
        "xǁVolatilityModelǁ__init____mutmut_7": xǁVolatilityModelǁ__init____mutmut_7,
        "xǁVolatilityModelǁ__init____mutmut_8": xǁVolatilityModelǁ__init____mutmut_8,
        "xǁVolatilityModelǁ__init____mutmut_9": xǁVolatilityModelǁ__init____mutmut_9,
        "xǁVolatilityModelǁ__init____mutmut_10": xǁVolatilityModelǁ__init____mutmut_10,
        "xǁVolatilityModelǁ__init____mutmut_11": xǁVolatilityModelǁ__init____mutmut_11,
        "xǁVolatilityModelǁ__init____mutmut_12": xǁVolatilityModelǁ__init____mutmut_12,
        "xǁVolatilityModelǁ__init____mutmut_13": xǁVolatilityModelǁ__init____mutmut_13,
        "xǁVolatilityModelǁ__init____mutmut_14": xǁVolatilityModelǁ__init____mutmut_14,
        "xǁVolatilityModelǁ__init____mutmut_15": xǁVolatilityModelǁ__init____mutmut_15,
        "xǁVolatilityModelǁ__init____mutmut_16": xǁVolatilityModelǁ__init____mutmut_16,
        "xǁVolatilityModelǁ__init____mutmut_17": xǁVolatilityModelǁ__init____mutmut_17,
        "xǁVolatilityModelǁ__init____mutmut_18": xǁVolatilityModelǁ__init____mutmut_18,
        "xǁVolatilityModelǁ__init____mutmut_19": xǁVolatilityModelǁ__init____mutmut_19,
        "xǁVolatilityModelǁ__init____mutmut_20": xǁVolatilityModelǁ__init____mutmut_20,
        "xǁVolatilityModelǁ__init____mutmut_21": xǁVolatilityModelǁ__init____mutmut_21,
        "xǁVolatilityModelǁ__init____mutmut_22": xǁVolatilityModelǁ__init____mutmut_22,
        "xǁVolatilityModelǁ__init____mutmut_23": xǁVolatilityModelǁ__init____mutmut_23,
        "xǁVolatilityModelǁ__init____mutmut_24": xǁVolatilityModelǁ__init____mutmut_24,
        "xǁVolatilityModelǁ__init____mutmut_25": xǁVolatilityModelǁ__init____mutmut_25,
        "xǁVolatilityModelǁ__init____mutmut_26": xǁVolatilityModelǁ__init____mutmut_26,
        "xǁVolatilityModelǁ__init____mutmut_27": xǁVolatilityModelǁ__init____mutmut_27,
        "xǁVolatilityModelǁ__init____mutmut_28": xǁVolatilityModelǁ__init____mutmut_28,
        "xǁVolatilityModelǁ__init____mutmut_29": xǁVolatilityModelǁ__init____mutmut_29,
    }
    xǁVolatilityModelǁ__init____mutmut_orig.__name__ = "xǁVolatilityModelǁ__init__"

    @staticmethod
    def _build_distribution(dist: str) -> Distribution:
        """Build a distribution instance from name."""
        from archbox.distributions.normal import Normal

        if dist == "normal":
            return Normal()
        msg = f"Unknown distribution: {dist}. Available: 'normal'."
        raise ValueError(msg)

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series.

        Parameters
        ----------
        params : ndarray
            Model parameters (omega, alpha, beta, ...).
        resids : ndarray
            Residuals (eps_t = r_t - mu).
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t, shape (T,).
        """

    @property
    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names."""

    @abstractmethod
    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained parameters to constrained space."""

    @abstractmethod
    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained parameters to unconstrained space."""

    @abstractmethod
    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer [(lower, upper), ...]."""

    @property
    @abstractmethod
    def num_params(self) -> int:
        """Number of model parameters."""

    # --- Concrete methods ---

    def fit(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        args = [method, starting_values, variance_targeting, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVolatilityModelǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁVolatilityModelǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_orig(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_1(
        self,
        method: str = "XXmleXX",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_2(
        self,
        method: str = "MLE",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_3(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = True,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_4(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = False,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_5(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """

        estimator = None
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_6(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = None
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_7(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=None,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_8(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=None,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_9(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=None,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_10(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=None,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_11(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_12(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_13(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            disp=disp,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_14(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
        )
        self._is_fitted = True
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_15(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = None
        return results

    # --- Concrete methods ---

    def xǁVolatilityModelǁfit__mutmut_16(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = False
        return results

    xǁVolatilityModelǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVolatilityModelǁfit__mutmut_1": xǁVolatilityModelǁfit__mutmut_1,
        "xǁVolatilityModelǁfit__mutmut_2": xǁVolatilityModelǁfit__mutmut_2,
        "xǁVolatilityModelǁfit__mutmut_3": xǁVolatilityModelǁfit__mutmut_3,
        "xǁVolatilityModelǁfit__mutmut_4": xǁVolatilityModelǁfit__mutmut_4,
        "xǁVolatilityModelǁfit__mutmut_5": xǁVolatilityModelǁfit__mutmut_5,
        "xǁVolatilityModelǁfit__mutmut_6": xǁVolatilityModelǁfit__mutmut_6,
        "xǁVolatilityModelǁfit__mutmut_7": xǁVolatilityModelǁfit__mutmut_7,
        "xǁVolatilityModelǁfit__mutmut_8": xǁVolatilityModelǁfit__mutmut_8,
        "xǁVolatilityModelǁfit__mutmut_9": xǁVolatilityModelǁfit__mutmut_9,
        "xǁVolatilityModelǁfit__mutmut_10": xǁVolatilityModelǁfit__mutmut_10,
        "xǁVolatilityModelǁfit__mutmut_11": xǁVolatilityModelǁfit__mutmut_11,
        "xǁVolatilityModelǁfit__mutmut_12": xǁVolatilityModelǁfit__mutmut_12,
        "xǁVolatilityModelǁfit__mutmut_13": xǁVolatilityModelǁfit__mutmut_13,
        "xǁVolatilityModelǁfit__mutmut_14": xǁVolatilityModelǁfit__mutmut_14,
        "xǁVolatilityModelǁfit__mutmut_15": xǁVolatilityModelǁfit__mutmut_15,
        "xǁVolatilityModelǁfit__mutmut_16": xǁVolatilityModelǁfit__mutmut_16,
    }
    xǁVolatilityModelǁfit__mutmut_orig.__name__ = "xǁVolatilityModelǁfit"

    def loglike(self, params: NDArray[np.float64], backcast: float | None = None) -> float:
        args = [params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVolatilityModelǁloglike__mutmut_orig"),
            object.__getattribute__(self, "xǁVolatilityModelǁloglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVolatilityModelǁloglike__mutmut_orig(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_1(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is not None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_2(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = None
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_3(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(None)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_4(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = None
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_5(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(None, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_6(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, None, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_7(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, None)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_8(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_9(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_10(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(
            params,
            self.endog,
        )
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_11(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = None
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_12(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(None, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_13(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, None)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_14(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_15(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(
            sigma2,
        )
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_16(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1.000000000001)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_17(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = None
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_18(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(None, sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_19(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, None)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_20(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(sigma2)
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_21(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(
            self.endog,
        )
        return float(np.sum(ll_per_obs))

    def xǁVolatilityModelǁloglike__mutmut_22(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(None)

    def xǁVolatilityModelǁloglike__mutmut_23(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2)
        return float(np.sum(None))

    xǁVolatilityModelǁloglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVolatilityModelǁloglike__mutmut_1": xǁVolatilityModelǁloglike__mutmut_1,
        "xǁVolatilityModelǁloglike__mutmut_2": xǁVolatilityModelǁloglike__mutmut_2,
        "xǁVolatilityModelǁloglike__mutmut_3": xǁVolatilityModelǁloglike__mutmut_3,
        "xǁVolatilityModelǁloglike__mutmut_4": xǁVolatilityModelǁloglike__mutmut_4,
        "xǁVolatilityModelǁloglike__mutmut_5": xǁVolatilityModelǁloglike__mutmut_5,
        "xǁVolatilityModelǁloglike__mutmut_6": xǁVolatilityModelǁloglike__mutmut_6,
        "xǁVolatilityModelǁloglike__mutmut_7": xǁVolatilityModelǁloglike__mutmut_7,
        "xǁVolatilityModelǁloglike__mutmut_8": xǁVolatilityModelǁloglike__mutmut_8,
        "xǁVolatilityModelǁloglike__mutmut_9": xǁVolatilityModelǁloglike__mutmut_9,
        "xǁVolatilityModelǁloglike__mutmut_10": xǁVolatilityModelǁloglike__mutmut_10,
        "xǁVolatilityModelǁloglike__mutmut_11": xǁVolatilityModelǁloglike__mutmut_11,
        "xǁVolatilityModelǁloglike__mutmut_12": xǁVolatilityModelǁloglike__mutmut_12,
        "xǁVolatilityModelǁloglike__mutmut_13": xǁVolatilityModelǁloglike__mutmut_13,
        "xǁVolatilityModelǁloglike__mutmut_14": xǁVolatilityModelǁloglike__mutmut_14,
        "xǁVolatilityModelǁloglike__mutmut_15": xǁVolatilityModelǁloglike__mutmut_15,
        "xǁVolatilityModelǁloglike__mutmut_16": xǁVolatilityModelǁloglike__mutmut_16,
        "xǁVolatilityModelǁloglike__mutmut_17": xǁVolatilityModelǁloglike__mutmut_17,
        "xǁVolatilityModelǁloglike__mutmut_18": xǁVolatilityModelǁloglike__mutmut_18,
        "xǁVolatilityModelǁloglike__mutmut_19": xǁVolatilityModelǁloglike__mutmut_19,
        "xǁVolatilityModelǁloglike__mutmut_20": xǁVolatilityModelǁloglike__mutmut_20,
        "xǁVolatilityModelǁloglike__mutmut_21": xǁVolatilityModelǁloglike__mutmut_21,
        "xǁVolatilityModelǁloglike__mutmut_22": xǁVolatilityModelǁloglike__mutmut_22,
        "xǁVolatilityModelǁloglike__mutmut_23": xǁVolatilityModelǁloglike__mutmut_23,
    }
    xǁVolatilityModelǁloglike__mutmut_orig.__name__ = "xǁVolatilityModelǁloglike"

    def loglike_per_obs(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        args = [params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVolatilityModelǁloglike_per_obs__mutmut_orig"),
            object.__getattribute__(self, "xǁVolatilityModelǁloglike_per_obs__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVolatilityModelǁloglike_per_obs__mutmut_orig(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_1(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is not None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_2(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = None
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_3(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(None)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_4(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = None
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_5(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(None, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_6(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, None, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_7(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, None)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_8(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_9(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_10(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(
            params,
            self.endog,
        )
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_11(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = None
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_12(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(None, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_13(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, None)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_14(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(1e-12)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_15(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(
            sigma2,
        )
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_16(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1.000000000001)
        return self.dist.loglikelihood(self.endog, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_17(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(None, sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_18(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, None)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_19(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(sigma2)

    def xǁVolatilityModelǁloglike_per_obs__mutmut_20(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        sigma2 = self._variance_recursion(params, self.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(
            self.endog,
        )

    xǁVolatilityModelǁloglike_per_obs__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVolatilityModelǁloglike_per_obs__mutmut_1": xǁVolatilityModelǁloglike_per_obs__mutmut_1,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_2": xǁVolatilityModelǁloglike_per_obs__mutmut_2,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_3": xǁVolatilityModelǁloglike_per_obs__mutmut_3,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_4": xǁVolatilityModelǁloglike_per_obs__mutmut_4,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_5": xǁVolatilityModelǁloglike_per_obs__mutmut_5,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_6": xǁVolatilityModelǁloglike_per_obs__mutmut_6,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_7": xǁVolatilityModelǁloglike_per_obs__mutmut_7,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_8": xǁVolatilityModelǁloglike_per_obs__mutmut_8,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_9": xǁVolatilityModelǁloglike_per_obs__mutmut_9,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_10": xǁVolatilityModelǁloglike_per_obs__mutmut_10,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_11": xǁVolatilityModelǁloglike_per_obs__mutmut_11,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_12": xǁVolatilityModelǁloglike_per_obs__mutmut_12,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_13": xǁVolatilityModelǁloglike_per_obs__mutmut_13,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_14": xǁVolatilityModelǁloglike_per_obs__mutmut_14,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_15": xǁVolatilityModelǁloglike_per_obs__mutmut_15,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_16": xǁVolatilityModelǁloglike_per_obs__mutmut_16,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_17": xǁVolatilityModelǁloglike_per_obs__mutmut_17,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_18": xǁVolatilityModelǁloglike_per_obs__mutmut_18,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_19": xǁVolatilityModelǁloglike_per_obs__mutmut_19,
        "xǁVolatilityModelǁloglike_per_obs__mutmut_20": xǁVolatilityModelǁloglike_per_obs__mutmut_20,
    }
    xǁVolatilityModelǁloglike_per_obs__mutmut_orig.__name__ = "xǁVolatilityModelǁloglike_per_obs"

    def simulate(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        args = [n, params, seed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVolatilityModelǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁVolatilityModelǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVolatilityModelǁsimulate__mutmut_orig(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_1(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = None
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_2(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(None)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_3(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = None

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_4(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(None, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_5(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, None)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_6(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_7(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(
            n,
        )

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_8(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = None  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_9(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] * (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_10(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[1] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_11(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 + np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_12(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (2.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_13(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(None))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_14(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[2:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_15(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) and backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_16(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_17(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(None) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_18(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast < 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_19(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 1:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_20(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = None

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_21(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(None) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_22(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) >= 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_23(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 1 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_24(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 2.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_25(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = None
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_26(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(None)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_27(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = None

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_28(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(None)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_29(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = None
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_30(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[1] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_31(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = None

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_32(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[1] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_33(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) / z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_34(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(None) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_35(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[1]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_36(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[1]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_37(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(None, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_38(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, None):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_39(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_40(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(
            1,
        ):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_41(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(2, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_42(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = None
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_43(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t - 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_44(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 2] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_45(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(None, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_46(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, None, float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_47(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], None)[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_48(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_49(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_50(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(
                params,
                returns[:t],
            )[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_51(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(None))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_52(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[+1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_53(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-2:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_54(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = None

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_55(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) / z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_56(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(None) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_57(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(None, 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_58(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], None)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_59(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_60(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = (
                np.sqrt(
                    max(
                        sigma2[t],
                    )
                )
                * z[t]
            )

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_61(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1.000000000001)) * z[t]

        return returns, np.sqrt(sigma2)

    def xǁVolatilityModelǁsimulate__mutmut_62(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        z = self.dist.simulate(n, rng)

        backcast = params[0] / (1.0 - np.sum(params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(params, returns[:t], float(backcast))[-1:]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(None)

    xǁVolatilityModelǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVolatilityModelǁsimulate__mutmut_1": xǁVolatilityModelǁsimulate__mutmut_1,
        "xǁVolatilityModelǁsimulate__mutmut_2": xǁVolatilityModelǁsimulate__mutmut_2,
        "xǁVolatilityModelǁsimulate__mutmut_3": xǁVolatilityModelǁsimulate__mutmut_3,
        "xǁVolatilityModelǁsimulate__mutmut_4": xǁVolatilityModelǁsimulate__mutmut_4,
        "xǁVolatilityModelǁsimulate__mutmut_5": xǁVolatilityModelǁsimulate__mutmut_5,
        "xǁVolatilityModelǁsimulate__mutmut_6": xǁVolatilityModelǁsimulate__mutmut_6,
        "xǁVolatilityModelǁsimulate__mutmut_7": xǁVolatilityModelǁsimulate__mutmut_7,
        "xǁVolatilityModelǁsimulate__mutmut_8": xǁVolatilityModelǁsimulate__mutmut_8,
        "xǁVolatilityModelǁsimulate__mutmut_9": xǁVolatilityModelǁsimulate__mutmut_9,
        "xǁVolatilityModelǁsimulate__mutmut_10": xǁVolatilityModelǁsimulate__mutmut_10,
        "xǁVolatilityModelǁsimulate__mutmut_11": xǁVolatilityModelǁsimulate__mutmut_11,
        "xǁVolatilityModelǁsimulate__mutmut_12": xǁVolatilityModelǁsimulate__mutmut_12,
        "xǁVolatilityModelǁsimulate__mutmut_13": xǁVolatilityModelǁsimulate__mutmut_13,
        "xǁVolatilityModelǁsimulate__mutmut_14": xǁVolatilityModelǁsimulate__mutmut_14,
        "xǁVolatilityModelǁsimulate__mutmut_15": xǁVolatilityModelǁsimulate__mutmut_15,
        "xǁVolatilityModelǁsimulate__mutmut_16": xǁVolatilityModelǁsimulate__mutmut_16,
        "xǁVolatilityModelǁsimulate__mutmut_17": xǁVolatilityModelǁsimulate__mutmut_17,
        "xǁVolatilityModelǁsimulate__mutmut_18": xǁVolatilityModelǁsimulate__mutmut_18,
        "xǁVolatilityModelǁsimulate__mutmut_19": xǁVolatilityModelǁsimulate__mutmut_19,
        "xǁVolatilityModelǁsimulate__mutmut_20": xǁVolatilityModelǁsimulate__mutmut_20,
        "xǁVolatilityModelǁsimulate__mutmut_21": xǁVolatilityModelǁsimulate__mutmut_21,
        "xǁVolatilityModelǁsimulate__mutmut_22": xǁVolatilityModelǁsimulate__mutmut_22,
        "xǁVolatilityModelǁsimulate__mutmut_23": xǁVolatilityModelǁsimulate__mutmut_23,
        "xǁVolatilityModelǁsimulate__mutmut_24": xǁVolatilityModelǁsimulate__mutmut_24,
        "xǁVolatilityModelǁsimulate__mutmut_25": xǁVolatilityModelǁsimulate__mutmut_25,
        "xǁVolatilityModelǁsimulate__mutmut_26": xǁVolatilityModelǁsimulate__mutmut_26,
        "xǁVolatilityModelǁsimulate__mutmut_27": xǁVolatilityModelǁsimulate__mutmut_27,
        "xǁVolatilityModelǁsimulate__mutmut_28": xǁVolatilityModelǁsimulate__mutmut_28,
        "xǁVolatilityModelǁsimulate__mutmut_29": xǁVolatilityModelǁsimulate__mutmut_29,
        "xǁVolatilityModelǁsimulate__mutmut_30": xǁVolatilityModelǁsimulate__mutmut_30,
        "xǁVolatilityModelǁsimulate__mutmut_31": xǁVolatilityModelǁsimulate__mutmut_31,
        "xǁVolatilityModelǁsimulate__mutmut_32": xǁVolatilityModelǁsimulate__mutmut_32,
        "xǁVolatilityModelǁsimulate__mutmut_33": xǁVolatilityModelǁsimulate__mutmut_33,
        "xǁVolatilityModelǁsimulate__mutmut_34": xǁVolatilityModelǁsimulate__mutmut_34,
        "xǁVolatilityModelǁsimulate__mutmut_35": xǁVolatilityModelǁsimulate__mutmut_35,
        "xǁVolatilityModelǁsimulate__mutmut_36": xǁVolatilityModelǁsimulate__mutmut_36,
        "xǁVolatilityModelǁsimulate__mutmut_37": xǁVolatilityModelǁsimulate__mutmut_37,
        "xǁVolatilityModelǁsimulate__mutmut_38": xǁVolatilityModelǁsimulate__mutmut_38,
        "xǁVolatilityModelǁsimulate__mutmut_39": xǁVolatilityModelǁsimulate__mutmut_39,
        "xǁVolatilityModelǁsimulate__mutmut_40": xǁVolatilityModelǁsimulate__mutmut_40,
        "xǁVolatilityModelǁsimulate__mutmut_41": xǁVolatilityModelǁsimulate__mutmut_41,
        "xǁVolatilityModelǁsimulate__mutmut_42": xǁVolatilityModelǁsimulate__mutmut_42,
        "xǁVolatilityModelǁsimulate__mutmut_43": xǁVolatilityModelǁsimulate__mutmut_43,
        "xǁVolatilityModelǁsimulate__mutmut_44": xǁVolatilityModelǁsimulate__mutmut_44,
        "xǁVolatilityModelǁsimulate__mutmut_45": xǁVolatilityModelǁsimulate__mutmut_45,
        "xǁVolatilityModelǁsimulate__mutmut_46": xǁVolatilityModelǁsimulate__mutmut_46,
        "xǁVolatilityModelǁsimulate__mutmut_47": xǁVolatilityModelǁsimulate__mutmut_47,
        "xǁVolatilityModelǁsimulate__mutmut_48": xǁVolatilityModelǁsimulate__mutmut_48,
        "xǁVolatilityModelǁsimulate__mutmut_49": xǁVolatilityModelǁsimulate__mutmut_49,
        "xǁVolatilityModelǁsimulate__mutmut_50": xǁVolatilityModelǁsimulate__mutmut_50,
        "xǁVolatilityModelǁsimulate__mutmut_51": xǁVolatilityModelǁsimulate__mutmut_51,
        "xǁVolatilityModelǁsimulate__mutmut_52": xǁVolatilityModelǁsimulate__mutmut_52,
        "xǁVolatilityModelǁsimulate__mutmut_53": xǁVolatilityModelǁsimulate__mutmut_53,
        "xǁVolatilityModelǁsimulate__mutmut_54": xǁVolatilityModelǁsimulate__mutmut_54,
        "xǁVolatilityModelǁsimulate__mutmut_55": xǁVolatilityModelǁsimulate__mutmut_55,
        "xǁVolatilityModelǁsimulate__mutmut_56": xǁVolatilityModelǁsimulate__mutmut_56,
        "xǁVolatilityModelǁsimulate__mutmut_57": xǁVolatilityModelǁsimulate__mutmut_57,
        "xǁVolatilityModelǁsimulate__mutmut_58": xǁVolatilityModelǁsimulate__mutmut_58,
        "xǁVolatilityModelǁsimulate__mutmut_59": xǁVolatilityModelǁsimulate__mutmut_59,
        "xǁVolatilityModelǁsimulate__mutmut_60": xǁVolatilityModelǁsimulate__mutmut_60,
        "xǁVolatilityModelǁsimulate__mutmut_61": xǁVolatilityModelǁsimulate__mutmut_61,
        "xǁVolatilityModelǁsimulate__mutmut_62": xǁVolatilityModelǁsimulate__mutmut_62,
    }
    xǁVolatilityModelǁsimulate__mutmut_orig.__name__ = "xǁVolatilityModelǁsimulate"

    def _backcast(self, resids: NDArray[np.float64]) -> float:
        args = [resids]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVolatilityModelǁ_backcast__mutmut_orig"),
            object.__getattribute__(self, "xǁVolatilityModelǁ_backcast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVolatilityModelǁ_backcast__mutmut_orig(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_1(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = None
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_2(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = None
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_3(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(None, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_4(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, None)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_5(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_6(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(
            75,
        )
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_7(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(76, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_8(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = None
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_9(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 * (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_10(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 3.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_11(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span - 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_12(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 2.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_13(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = None
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_14(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids * 2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_15(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**3
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_16(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = None
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_17(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) * np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_18(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 + alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_19(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (2 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_20(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(None, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_21(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, None, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_22(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, None)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_23(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(-1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_24(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_25(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(
            t - 1,
            -1,
        )
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_26(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t + 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_27(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 2, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_28(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, +1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_29(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -2, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_30(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, +1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_31(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -2)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_32(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = None
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_33(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(None)
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_34(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) * np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_35(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(None) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_36(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights / resids2) / np.sum(weights))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_37(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(None))
        return max(backcast, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_38(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(None, 1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_39(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, None)

    def xǁVolatilityModelǁ_backcast__mutmut_40(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(1e-12)

    def xǁVolatilityModelǁ_backcast__mutmut_41(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(
            backcast,
        )

    def xǁVolatilityModelǁ_backcast__mutmut_42(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1.000000000001)

    xǁVolatilityModelǁ_backcast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVolatilityModelǁ_backcast__mutmut_1": xǁVolatilityModelǁ_backcast__mutmut_1,
        "xǁVolatilityModelǁ_backcast__mutmut_2": xǁVolatilityModelǁ_backcast__mutmut_2,
        "xǁVolatilityModelǁ_backcast__mutmut_3": xǁVolatilityModelǁ_backcast__mutmut_3,
        "xǁVolatilityModelǁ_backcast__mutmut_4": xǁVolatilityModelǁ_backcast__mutmut_4,
        "xǁVolatilityModelǁ_backcast__mutmut_5": xǁVolatilityModelǁ_backcast__mutmut_5,
        "xǁVolatilityModelǁ_backcast__mutmut_6": xǁVolatilityModelǁ_backcast__mutmut_6,
        "xǁVolatilityModelǁ_backcast__mutmut_7": xǁVolatilityModelǁ_backcast__mutmut_7,
        "xǁVolatilityModelǁ_backcast__mutmut_8": xǁVolatilityModelǁ_backcast__mutmut_8,
        "xǁVolatilityModelǁ_backcast__mutmut_9": xǁVolatilityModelǁ_backcast__mutmut_9,
        "xǁVolatilityModelǁ_backcast__mutmut_10": xǁVolatilityModelǁ_backcast__mutmut_10,
        "xǁVolatilityModelǁ_backcast__mutmut_11": xǁVolatilityModelǁ_backcast__mutmut_11,
        "xǁVolatilityModelǁ_backcast__mutmut_12": xǁVolatilityModelǁ_backcast__mutmut_12,
        "xǁVolatilityModelǁ_backcast__mutmut_13": xǁVolatilityModelǁ_backcast__mutmut_13,
        "xǁVolatilityModelǁ_backcast__mutmut_14": xǁVolatilityModelǁ_backcast__mutmut_14,
        "xǁVolatilityModelǁ_backcast__mutmut_15": xǁVolatilityModelǁ_backcast__mutmut_15,
        "xǁVolatilityModelǁ_backcast__mutmut_16": xǁVolatilityModelǁ_backcast__mutmut_16,
        "xǁVolatilityModelǁ_backcast__mutmut_17": xǁVolatilityModelǁ_backcast__mutmut_17,
        "xǁVolatilityModelǁ_backcast__mutmut_18": xǁVolatilityModelǁ_backcast__mutmut_18,
        "xǁVolatilityModelǁ_backcast__mutmut_19": xǁVolatilityModelǁ_backcast__mutmut_19,
        "xǁVolatilityModelǁ_backcast__mutmut_20": xǁVolatilityModelǁ_backcast__mutmut_20,
        "xǁVolatilityModelǁ_backcast__mutmut_21": xǁVolatilityModelǁ_backcast__mutmut_21,
        "xǁVolatilityModelǁ_backcast__mutmut_22": xǁVolatilityModelǁ_backcast__mutmut_22,
        "xǁVolatilityModelǁ_backcast__mutmut_23": xǁVolatilityModelǁ_backcast__mutmut_23,
        "xǁVolatilityModelǁ_backcast__mutmut_24": xǁVolatilityModelǁ_backcast__mutmut_24,
        "xǁVolatilityModelǁ_backcast__mutmut_25": xǁVolatilityModelǁ_backcast__mutmut_25,
        "xǁVolatilityModelǁ_backcast__mutmut_26": xǁVolatilityModelǁ_backcast__mutmut_26,
        "xǁVolatilityModelǁ_backcast__mutmut_27": xǁVolatilityModelǁ_backcast__mutmut_27,
        "xǁVolatilityModelǁ_backcast__mutmut_28": xǁVolatilityModelǁ_backcast__mutmut_28,
        "xǁVolatilityModelǁ_backcast__mutmut_29": xǁVolatilityModelǁ_backcast__mutmut_29,
        "xǁVolatilityModelǁ_backcast__mutmut_30": xǁVolatilityModelǁ_backcast__mutmut_30,
        "xǁVolatilityModelǁ_backcast__mutmut_31": xǁVolatilityModelǁ_backcast__mutmut_31,
        "xǁVolatilityModelǁ_backcast__mutmut_32": xǁVolatilityModelǁ_backcast__mutmut_32,
        "xǁVolatilityModelǁ_backcast__mutmut_33": xǁVolatilityModelǁ_backcast__mutmut_33,
        "xǁVolatilityModelǁ_backcast__mutmut_34": xǁVolatilityModelǁ_backcast__mutmut_34,
        "xǁVolatilityModelǁ_backcast__mutmut_35": xǁVolatilityModelǁ_backcast__mutmut_35,
        "xǁVolatilityModelǁ_backcast__mutmut_36": xǁVolatilityModelǁ_backcast__mutmut_36,
        "xǁVolatilityModelǁ_backcast__mutmut_37": xǁVolatilityModelǁ_backcast__mutmut_37,
        "xǁVolatilityModelǁ_backcast__mutmut_38": xǁVolatilityModelǁ_backcast__mutmut_38,
        "xǁVolatilityModelǁ_backcast__mutmut_39": xǁVolatilityModelǁ_backcast__mutmut_39,
        "xǁVolatilityModelǁ_backcast__mutmut_40": xǁVolatilityModelǁ_backcast__mutmut_40,
        "xǁVolatilityModelǁ_backcast__mutmut_41": xǁVolatilityModelǁ_backcast__mutmut_41,
        "xǁVolatilityModelǁ_backcast__mutmut_42": xǁVolatilityModelǁ_backcast__mutmut_42,
    }
    xǁVolatilityModelǁ_backcast__mutmut_orig.__name__ = "xǁVolatilityModelǁ_backcast"
