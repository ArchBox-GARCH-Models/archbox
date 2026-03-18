"""VaR Backtesting: Kupiec, Christoffersen, Basel Traffic Light.

References
----------
- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk
  Measurement Models. Journal of Derivatives, 3(2), 73-84.
- Christoffersen, P.F. (1998). Evaluating Interval Forecasts.
  International Economic Review, 39(4), 841-862.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated, ClassVar

import numpy as np
from scipy import stats

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


@dataclass
class TestResult:
    """Container for a statistical test result.

    Attributes
    ----------
    statistic : float
        Test statistic value.
    pvalue : float
        p-value of the test.
    test_name : str
        Name of the test.
    df : int
        Degrees of freedom.
    """

    statistic: float
    pvalue: float
    test_name: str
    df: int = 1

    def __repr__(self) -> str:
        """Return string representation of the test result."""
        return (
            f"{self.test_name}: statistic={self.statistic:.4f}, "
            f"pvalue={self.pvalue:.4f}, df={self.df}"
        )


class VaRBacktest:
    """VaR Backtesting framework.

    Parameters
    ----------
    returns : array-like
        Realized return series.
    var_series : array-like
        VaR forecast series (must be negative for losses).
    alpha : float
        Significance level of the VaR. Default is 0.05.

    Attributes
    ----------
    returns : NDArray[np.float64]
        Realized returns.
    var : NDArray[np.float64]
        VaR forecasts.
    alpha : float
        Significance level.
    hits : NDArray[np.int64]
        Hit sequence: 1 if r_t < VaR_t, 0 otherwise.
    """

    def __init__(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        args = [returns, var_series, alpha]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVaRBacktestǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁVaRBacktestǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVaRBacktestǁ__init____mutmut_orig(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_1(
        self,
        returns: object,
        var_series: object,
        alpha: float = 1.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_2(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = None
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_3(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(None, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_4(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=None).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_5(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_6(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(
            returns,
        ).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_7(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = None

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_8(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(None, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_9(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=None).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_10(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_11(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(
            var_series,
        ).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_12(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) == len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_13(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = None
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_14(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(None)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_15(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_16(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 1 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_17(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 <= alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_18(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha <= 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_19(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 2:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_20(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = None
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_21(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(None)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_22(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = None

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_23(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = None
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_24(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) | ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_25(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_26(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(None) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_27(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_28(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(None)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_29(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = None
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_30(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = None
        self.hits = (self._returns_valid < self._var_valid).astype(np.int64)

    def xǁVaRBacktestǁ__init____mutmut_31(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = None

    def xǁVaRBacktestǁ__init____mutmut_32(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid < self._var_valid).astype(None)

    def xǁVaRBacktestǁ__init____mutmut_33(
        self,
        returns: object,
        var_series: object,
        alpha: float = 0.05,
    ) -> None:
        """Initialize VaR backtesting framework with returns and VaR series."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        self.var = np.asarray(var_series, dtype=np.float64).ravel()

        if len(self.returns) != len(self.var):
            msg = (
                f"returns and var_series must have same length, "
                f"got {len(self.returns)} and {len(self.var)}"
            )
            raise ValueError(msg)

        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.alpha = alpha

        # Filter out NaN values
        valid = ~np.isnan(self.returns) & ~np.isnan(self.var)
        self._returns_valid = self.returns[valid]
        self._var_valid = self.var[valid]
        self.hits = (self._returns_valid <= self._var_valid).astype(np.int64)

    xǁVaRBacktestǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVaRBacktestǁ__init____mutmut_1": xǁVaRBacktestǁ__init____mutmut_1,
        "xǁVaRBacktestǁ__init____mutmut_2": xǁVaRBacktestǁ__init____mutmut_2,
        "xǁVaRBacktestǁ__init____mutmut_3": xǁVaRBacktestǁ__init____mutmut_3,
        "xǁVaRBacktestǁ__init____mutmut_4": xǁVaRBacktestǁ__init____mutmut_4,
        "xǁVaRBacktestǁ__init____mutmut_5": xǁVaRBacktestǁ__init____mutmut_5,
        "xǁVaRBacktestǁ__init____mutmut_6": xǁVaRBacktestǁ__init____mutmut_6,
        "xǁVaRBacktestǁ__init____mutmut_7": xǁVaRBacktestǁ__init____mutmut_7,
        "xǁVaRBacktestǁ__init____mutmut_8": xǁVaRBacktestǁ__init____mutmut_8,
        "xǁVaRBacktestǁ__init____mutmut_9": xǁVaRBacktestǁ__init____mutmut_9,
        "xǁVaRBacktestǁ__init____mutmut_10": xǁVaRBacktestǁ__init____mutmut_10,
        "xǁVaRBacktestǁ__init____mutmut_11": xǁVaRBacktestǁ__init____mutmut_11,
        "xǁVaRBacktestǁ__init____mutmut_12": xǁVaRBacktestǁ__init____mutmut_12,
        "xǁVaRBacktestǁ__init____mutmut_13": xǁVaRBacktestǁ__init____mutmut_13,
        "xǁVaRBacktestǁ__init____mutmut_14": xǁVaRBacktestǁ__init____mutmut_14,
        "xǁVaRBacktestǁ__init____mutmut_15": xǁVaRBacktestǁ__init____mutmut_15,
        "xǁVaRBacktestǁ__init____mutmut_16": xǁVaRBacktestǁ__init____mutmut_16,
        "xǁVaRBacktestǁ__init____mutmut_17": xǁVaRBacktestǁ__init____mutmut_17,
        "xǁVaRBacktestǁ__init____mutmut_18": xǁVaRBacktestǁ__init____mutmut_18,
        "xǁVaRBacktestǁ__init____mutmut_19": xǁVaRBacktestǁ__init____mutmut_19,
        "xǁVaRBacktestǁ__init____mutmut_20": xǁVaRBacktestǁ__init____mutmut_20,
        "xǁVaRBacktestǁ__init____mutmut_21": xǁVaRBacktestǁ__init____mutmut_21,
        "xǁVaRBacktestǁ__init____mutmut_22": xǁVaRBacktestǁ__init____mutmut_22,
        "xǁVaRBacktestǁ__init____mutmut_23": xǁVaRBacktestǁ__init____mutmut_23,
        "xǁVaRBacktestǁ__init____mutmut_24": xǁVaRBacktestǁ__init____mutmut_24,
        "xǁVaRBacktestǁ__init____mutmut_25": xǁVaRBacktestǁ__init____mutmut_25,
        "xǁVaRBacktestǁ__init____mutmut_26": xǁVaRBacktestǁ__init____mutmut_26,
        "xǁVaRBacktestǁ__init____mutmut_27": xǁVaRBacktestǁ__init____mutmut_27,
        "xǁVaRBacktestǁ__init____mutmut_28": xǁVaRBacktestǁ__init____mutmut_28,
        "xǁVaRBacktestǁ__init____mutmut_29": xǁVaRBacktestǁ__init____mutmut_29,
        "xǁVaRBacktestǁ__init____mutmut_30": xǁVaRBacktestǁ__init____mutmut_30,
        "xǁVaRBacktestǁ__init____mutmut_31": xǁVaRBacktestǁ__init____mutmut_31,
        "xǁVaRBacktestǁ__init____mutmut_32": xǁVaRBacktestǁ__init____mutmut_32,
        "xǁVaRBacktestǁ__init____mutmut_33": xǁVaRBacktestǁ__init____mutmut_33,
    }
    xǁVaRBacktestǁ__init____mutmut_orig.__name__ = "xǁVaRBacktestǁ__init__"

    def kupiec_test(self) -> TestResult:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVaRBacktestǁkupiec_test__mutmut_orig"),
            object.__getattribute__(self, "xǁVaRBacktestǁkupiec_test__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_orig(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_1(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = None
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_2(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = None

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_3(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(None)

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_4(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(None))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_5(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = None

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_6(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(None, 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_7(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), None) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_8(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_9(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = (
            max(
                min(x / n, 1 - 1e-10),
            )
            if x == 0 or x == n
            else x / n
        )

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_10(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(None, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_11(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, None), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_12(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_13(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = (
            max(
                min(
                    x / n,
                ),
                1e-10,
            )
            if x == 0 or x == n
            else x / n
        )

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_14(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x * n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_15(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 + 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_16(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 2 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_17(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1.0000000001), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_18(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1.0000000001) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_19(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 and x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_20(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x != 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_21(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 1 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_22(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x != n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_23(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x * n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_24(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = None

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_25(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = None
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_26(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) - (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_27(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x / np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_28(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(None) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_29(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) / np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_30(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n + x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_31(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(None)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_32(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 + alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_33(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(2 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_34(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = None

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_35(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) - (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_36(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x / np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_37(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(None) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_38(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) / np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_39(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n + x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_40(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(None)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_41(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 + pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_42(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(2 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_43(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = None
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_44(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 / (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_45(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = +2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_46(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -3 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_47(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 + ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_48(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = None  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_49(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(None, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_50(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, None)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_51(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_52(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(
            lr_pof,
        )  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_53(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 1.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_54(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = None

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_55(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(None)

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_56(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 + stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_57(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(2 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_58(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(None, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_59(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=None))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_60(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_61(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(
            1
            - stats.chi2.cdf(
                lr_pof,
            )
        )

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_62(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=2))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_63(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=None,
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_64(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=None,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_65(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name=None,
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_66(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=None,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_67(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_68(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_69(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_70(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_71(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(None),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_72(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="XXKupiec POFXX",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_73(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="kupiec pof",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_74(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="KUPIEC POF",
            df=1,
        )

    def xǁVaRBacktestǁkupiec_test__mutmut_75(self) -> TestResult:
        """Kupiec (1995) Proportion of Failures (POF) test.

        Tests H0: violation rate = alpha.

        Returns
        -------
        TestResult
            LR_POF statistic and p-value, chi2(1).

        Notes
        -----
        LR_POF = -2 * [x*log(alpha) + (n-x)*log(1-alpha)
                        - x*log(pi_hat) - (n-x)*log(1-pi_hat)]
        LR_POF ~ chi2(1)
        """
        n = len(self.hits)
        x = int(np.sum(self.hits))

        pi_hat = max(min(x / n, 1 - 1e-10), 1e-10) if x == 0 or x == n else x / n

        alpha = self.alpha

        # Log-likelihood under H0 (rate = alpha) and H1 (rate = pi_hat)
        ll_h0 = x * np.log(alpha) + (n - x) * np.log(1 - alpha)
        ll_h1 = x * np.log(pi_hat) + (n - x) * np.log(1 - pi_hat)

        lr_pof = -2 * (ll_h0 - ll_h1)
        lr_pof = max(lr_pof, 0.0)  # numerical safety
        pvalue = float(1 - stats.chi2.cdf(lr_pof, df=1))

        return TestResult(
            statistic=float(lr_pof),
            pvalue=pvalue,
            test_name="Kupiec POF",
            df=2,
        )

    xǁVaRBacktestǁkupiec_test__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVaRBacktestǁkupiec_test__mutmut_1": xǁVaRBacktestǁkupiec_test__mutmut_1,
        "xǁVaRBacktestǁkupiec_test__mutmut_2": xǁVaRBacktestǁkupiec_test__mutmut_2,
        "xǁVaRBacktestǁkupiec_test__mutmut_3": xǁVaRBacktestǁkupiec_test__mutmut_3,
        "xǁVaRBacktestǁkupiec_test__mutmut_4": xǁVaRBacktestǁkupiec_test__mutmut_4,
        "xǁVaRBacktestǁkupiec_test__mutmut_5": xǁVaRBacktestǁkupiec_test__mutmut_5,
        "xǁVaRBacktestǁkupiec_test__mutmut_6": xǁVaRBacktestǁkupiec_test__mutmut_6,
        "xǁVaRBacktestǁkupiec_test__mutmut_7": xǁVaRBacktestǁkupiec_test__mutmut_7,
        "xǁVaRBacktestǁkupiec_test__mutmut_8": xǁVaRBacktestǁkupiec_test__mutmut_8,
        "xǁVaRBacktestǁkupiec_test__mutmut_9": xǁVaRBacktestǁkupiec_test__mutmut_9,
        "xǁVaRBacktestǁkupiec_test__mutmut_10": xǁVaRBacktestǁkupiec_test__mutmut_10,
        "xǁVaRBacktestǁkupiec_test__mutmut_11": xǁVaRBacktestǁkupiec_test__mutmut_11,
        "xǁVaRBacktestǁkupiec_test__mutmut_12": xǁVaRBacktestǁkupiec_test__mutmut_12,
        "xǁVaRBacktestǁkupiec_test__mutmut_13": xǁVaRBacktestǁkupiec_test__mutmut_13,
        "xǁVaRBacktestǁkupiec_test__mutmut_14": xǁVaRBacktestǁkupiec_test__mutmut_14,
        "xǁVaRBacktestǁkupiec_test__mutmut_15": xǁVaRBacktestǁkupiec_test__mutmut_15,
        "xǁVaRBacktestǁkupiec_test__mutmut_16": xǁVaRBacktestǁkupiec_test__mutmut_16,
        "xǁVaRBacktestǁkupiec_test__mutmut_17": xǁVaRBacktestǁkupiec_test__mutmut_17,
        "xǁVaRBacktestǁkupiec_test__mutmut_18": xǁVaRBacktestǁkupiec_test__mutmut_18,
        "xǁVaRBacktestǁkupiec_test__mutmut_19": xǁVaRBacktestǁkupiec_test__mutmut_19,
        "xǁVaRBacktestǁkupiec_test__mutmut_20": xǁVaRBacktestǁkupiec_test__mutmut_20,
        "xǁVaRBacktestǁkupiec_test__mutmut_21": xǁVaRBacktestǁkupiec_test__mutmut_21,
        "xǁVaRBacktestǁkupiec_test__mutmut_22": xǁVaRBacktestǁkupiec_test__mutmut_22,
        "xǁVaRBacktestǁkupiec_test__mutmut_23": xǁVaRBacktestǁkupiec_test__mutmut_23,
        "xǁVaRBacktestǁkupiec_test__mutmut_24": xǁVaRBacktestǁkupiec_test__mutmut_24,
        "xǁVaRBacktestǁkupiec_test__mutmut_25": xǁVaRBacktestǁkupiec_test__mutmut_25,
        "xǁVaRBacktestǁkupiec_test__mutmut_26": xǁVaRBacktestǁkupiec_test__mutmut_26,
        "xǁVaRBacktestǁkupiec_test__mutmut_27": xǁVaRBacktestǁkupiec_test__mutmut_27,
        "xǁVaRBacktestǁkupiec_test__mutmut_28": xǁVaRBacktestǁkupiec_test__mutmut_28,
        "xǁVaRBacktestǁkupiec_test__mutmut_29": xǁVaRBacktestǁkupiec_test__mutmut_29,
        "xǁVaRBacktestǁkupiec_test__mutmut_30": xǁVaRBacktestǁkupiec_test__mutmut_30,
        "xǁVaRBacktestǁkupiec_test__mutmut_31": xǁVaRBacktestǁkupiec_test__mutmut_31,
        "xǁVaRBacktestǁkupiec_test__mutmut_32": xǁVaRBacktestǁkupiec_test__mutmut_32,
        "xǁVaRBacktestǁkupiec_test__mutmut_33": xǁVaRBacktestǁkupiec_test__mutmut_33,
        "xǁVaRBacktestǁkupiec_test__mutmut_34": xǁVaRBacktestǁkupiec_test__mutmut_34,
        "xǁVaRBacktestǁkupiec_test__mutmut_35": xǁVaRBacktestǁkupiec_test__mutmut_35,
        "xǁVaRBacktestǁkupiec_test__mutmut_36": xǁVaRBacktestǁkupiec_test__mutmut_36,
        "xǁVaRBacktestǁkupiec_test__mutmut_37": xǁVaRBacktestǁkupiec_test__mutmut_37,
        "xǁVaRBacktestǁkupiec_test__mutmut_38": xǁVaRBacktestǁkupiec_test__mutmut_38,
        "xǁVaRBacktestǁkupiec_test__mutmut_39": xǁVaRBacktestǁkupiec_test__mutmut_39,
        "xǁVaRBacktestǁkupiec_test__mutmut_40": xǁVaRBacktestǁkupiec_test__mutmut_40,
        "xǁVaRBacktestǁkupiec_test__mutmut_41": xǁVaRBacktestǁkupiec_test__mutmut_41,
        "xǁVaRBacktestǁkupiec_test__mutmut_42": xǁVaRBacktestǁkupiec_test__mutmut_42,
        "xǁVaRBacktestǁkupiec_test__mutmut_43": xǁVaRBacktestǁkupiec_test__mutmut_43,
        "xǁVaRBacktestǁkupiec_test__mutmut_44": xǁVaRBacktestǁkupiec_test__mutmut_44,
        "xǁVaRBacktestǁkupiec_test__mutmut_45": xǁVaRBacktestǁkupiec_test__mutmut_45,
        "xǁVaRBacktestǁkupiec_test__mutmut_46": xǁVaRBacktestǁkupiec_test__mutmut_46,
        "xǁVaRBacktestǁkupiec_test__mutmut_47": xǁVaRBacktestǁkupiec_test__mutmut_47,
        "xǁVaRBacktestǁkupiec_test__mutmut_48": xǁVaRBacktestǁkupiec_test__mutmut_48,
        "xǁVaRBacktestǁkupiec_test__mutmut_49": xǁVaRBacktestǁkupiec_test__mutmut_49,
        "xǁVaRBacktestǁkupiec_test__mutmut_50": xǁVaRBacktestǁkupiec_test__mutmut_50,
        "xǁVaRBacktestǁkupiec_test__mutmut_51": xǁVaRBacktestǁkupiec_test__mutmut_51,
        "xǁVaRBacktestǁkupiec_test__mutmut_52": xǁVaRBacktestǁkupiec_test__mutmut_52,
        "xǁVaRBacktestǁkupiec_test__mutmut_53": xǁVaRBacktestǁkupiec_test__mutmut_53,
        "xǁVaRBacktestǁkupiec_test__mutmut_54": xǁVaRBacktestǁkupiec_test__mutmut_54,
        "xǁVaRBacktestǁkupiec_test__mutmut_55": xǁVaRBacktestǁkupiec_test__mutmut_55,
        "xǁVaRBacktestǁkupiec_test__mutmut_56": xǁVaRBacktestǁkupiec_test__mutmut_56,
        "xǁVaRBacktestǁkupiec_test__mutmut_57": xǁVaRBacktestǁkupiec_test__mutmut_57,
        "xǁVaRBacktestǁkupiec_test__mutmut_58": xǁVaRBacktestǁkupiec_test__mutmut_58,
        "xǁVaRBacktestǁkupiec_test__mutmut_59": xǁVaRBacktestǁkupiec_test__mutmut_59,
        "xǁVaRBacktestǁkupiec_test__mutmut_60": xǁVaRBacktestǁkupiec_test__mutmut_60,
        "xǁVaRBacktestǁkupiec_test__mutmut_61": xǁVaRBacktestǁkupiec_test__mutmut_61,
        "xǁVaRBacktestǁkupiec_test__mutmut_62": xǁVaRBacktestǁkupiec_test__mutmut_62,
        "xǁVaRBacktestǁkupiec_test__mutmut_63": xǁVaRBacktestǁkupiec_test__mutmut_63,
        "xǁVaRBacktestǁkupiec_test__mutmut_64": xǁVaRBacktestǁkupiec_test__mutmut_64,
        "xǁVaRBacktestǁkupiec_test__mutmut_65": xǁVaRBacktestǁkupiec_test__mutmut_65,
        "xǁVaRBacktestǁkupiec_test__mutmut_66": xǁVaRBacktestǁkupiec_test__mutmut_66,
        "xǁVaRBacktestǁkupiec_test__mutmut_67": xǁVaRBacktestǁkupiec_test__mutmut_67,
        "xǁVaRBacktestǁkupiec_test__mutmut_68": xǁVaRBacktestǁkupiec_test__mutmut_68,
        "xǁVaRBacktestǁkupiec_test__mutmut_69": xǁVaRBacktestǁkupiec_test__mutmut_69,
        "xǁVaRBacktestǁkupiec_test__mutmut_70": xǁVaRBacktestǁkupiec_test__mutmut_70,
        "xǁVaRBacktestǁkupiec_test__mutmut_71": xǁVaRBacktestǁkupiec_test__mutmut_71,
        "xǁVaRBacktestǁkupiec_test__mutmut_72": xǁVaRBacktestǁkupiec_test__mutmut_72,
        "xǁVaRBacktestǁkupiec_test__mutmut_73": xǁVaRBacktestǁkupiec_test__mutmut_73,
        "xǁVaRBacktestǁkupiec_test__mutmut_74": xǁVaRBacktestǁkupiec_test__mutmut_74,
        "xǁVaRBacktestǁkupiec_test__mutmut_75": xǁVaRBacktestǁkupiec_test__mutmut_75,
    }
    xǁVaRBacktestǁkupiec_test__mutmut_orig.__name__ = "xǁVaRBacktestǁkupiec_test"

    def christoffersen_test(self) -> TestResult:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVaRBacktestǁchristoffersen_test__mutmut_orig"),
            object.__getattribute__(self, "xǁVaRBacktestǁchristoffersen_test__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_orig(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_1(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = None

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_2(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = None
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_3(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 1, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_4(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 1, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_5(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 1, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_6(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 1
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_7(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(None, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_8(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, None):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_9(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_10(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(
            1,
        ):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_11(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(2, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_12(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 or hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_13(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t + 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_14(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 2] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_15(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] != 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_16(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 1 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_17(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] != 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_18(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 1:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_19(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 = 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_20(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 -= 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_21(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 2
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_22(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 or hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_23(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t + 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_24(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 2] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_25(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] != 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_26(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 1 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_27(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] != 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_28(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 2:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_29(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 = 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_30(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 -= 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_31(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 2
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_32(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 or hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_33(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t + 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_34(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 2] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_35(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] != 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_36(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 2 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_37(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] != 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_38(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 1:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_39(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 = 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_40(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 -= 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_41(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 2
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_42(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 = 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_43(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 -= 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_44(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 2

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_45(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = None
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_46(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 - n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_47(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = None
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_48(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 - n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_49(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = None

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_50(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 - n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_51(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 and n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_52(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total != 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_53(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 1 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_54(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 != 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_55(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 1:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_56(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=None, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_57(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=None, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_58(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name=None, df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_59(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=None)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_60(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_61(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_62(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_63(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(
                statistic=0.0,
                pvalue=1.0,
                test_name="Christoffersen CC",
            )

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_64(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=1.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_65(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=2.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_66(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="XXChristoffersen CCXX", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_67(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="christoffersen cc", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_68(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="CHRISTOFFERSEN CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_69(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=3)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_70(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = None

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_71(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) * n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_72(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 - n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_73(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = None
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_74(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 * n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_75(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 or n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_76(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 >= 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_77(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 1 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_78(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 >= 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_79(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 1 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_80(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1.0000000001
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_81(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = None

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_82(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 * n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_83(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 or n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_84(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 >= 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_85(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 1 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_86(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 >= 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_87(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 1 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_88(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1.0000000001

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_89(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = None
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_90(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(None, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_91(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, None, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_92(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, None)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_93(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_94(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_95(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(
            pi_hat,
            1e-10,
        )
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_96(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1.0000000001, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_97(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 + 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_98(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 2 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_99(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1.0000000001)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_100(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = None
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_101(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(None, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_102(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, None, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_103(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, None)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_104(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_105(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_106(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(
            pi01,
            1e-10,
        )
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_107(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1.0000000001, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_108(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 + 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_109(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 2 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_110(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1.0000000001)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_111(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = None

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_112(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(None, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_113(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, None, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_114(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, None)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_115(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_116(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_117(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(
            pi11,
            1e-10,
        )

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_118(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1.0000000001, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_119(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 + 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_120(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 2 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_121(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1.0000000001)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_122(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = None

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_123(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) - (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_124(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) / np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_125(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 - n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_126(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(None) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_127(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 + pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_128(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(2 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_129(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) / np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_130(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 - n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_131(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(None)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_132(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = None

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_133(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            - n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_134(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            - n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_135(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            - n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_136(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 / np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_137(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(None) + n01 * np.log(pi01) + n10 * np.log(1 - pi11) + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_138(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 + pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_139(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(2 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_140(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 / np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_141(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(None)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_142(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 / np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_143(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01) + n01 * np.log(pi01) + n10 * np.log(None) + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_144(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 + pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_145(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(2 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_146(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 / np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_147(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(None)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_148(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = None
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_149(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 / (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_150(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = +2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_151(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -3 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_152(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 + ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_153(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = None

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_154(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(None, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_155(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, None)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_156(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_157(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(
            lr_ind,
        )

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_158(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 1.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_159(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = None
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_160(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = None
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_161(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic - lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_162(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = None

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_163(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(None)

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_164(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 + stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_165(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(2 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_166(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(None, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_167(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=None))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_168(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_169(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(
            1
            - stats.chi2.cdf(
                lr_cc,
            )
        )

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_170(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=3))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_171(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=None,
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_172(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=None,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_173(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name=None,
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_174(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=None,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_175(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_176(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_177(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_178(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_179(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(None),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_180(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="XXChristoffersen CCXX",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_181(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="christoffersen cc",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_182(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="CHRISTOFFERSEN CC",
            df=2,
        )

    def xǁVaRBacktestǁchristoffersen_test__mutmut_183(self) -> TestResult:
        """Christoffersen (1998) Conditional Coverage test.

        Tests H0: violations are independent AND rate = alpha.

        Returns
        -------
        TestResult
            LR_CC statistic and p-value, chi2(2).

        Notes
        -----
        LR_CC = LR_POF + LR_ind ~ chi2(2)

        Where LR_ind tests independence of the hit sequence.
        """
        hits = self.hits

        # Transition counts
        n00, n01, n10, n11 = 0, 0, 0, 0
        for t in range(1, len(hits)):
            if hits[t - 1] == 0 and hits[t] == 0:
                n00 += 1
            elif hits[t - 1] == 0 and hits[t] == 1:
                n01 += 1
            elif hits[t - 1] == 1 and hits[t] == 0:
                n10 += 1
            else:
                n11 += 1

        # Avoid division by zero
        n0 = n00 + n01
        n1 = n10 + n11
        n_total = n0 + n1

        if n_total == 0 or n0 == 0:
            return TestResult(statistic=0.0, pvalue=1.0, test_name="Christoffersen CC", df=2)

        pi_hat = (n01 + n11) / n_total

        pi01 = n01 / n0 if n0 > 0 and n01 > 0 else 1e-10
        pi11 = n11 / n1 if n1 > 0 and n11 > 0 else 1e-10

        # Clamp probabilities
        pi_hat = np.clip(pi_hat, 1e-10, 1 - 1e-10)
        pi01 = np.clip(pi01, 1e-10, 1 - 1e-10)
        pi11 = np.clip(pi11, 1e-10, 1 - 1e-10)

        # Log-likelihood under H0 (independence)
        ll_h0 = (n00 + n10) * np.log(1 - pi_hat) + (n01 + n11) * np.log(pi_hat)

        # Log-likelihood under H1 (Markov)
        ll_h1 = (
            n00 * np.log(1 - pi01)
            + n01 * np.log(pi01)
            + n10 * np.log(1 - pi11)
            + n11 * np.log(pi11)
        )

        lr_ind = -2 * (ll_h0 - ll_h1)
        lr_ind = max(lr_ind, 0.0)

        # Kupiec POF
        kupiec = self.kupiec_test()
        lr_cc = kupiec.statistic + lr_ind
        pvalue = float(1 - stats.chi2.cdf(lr_cc, df=2))

        return TestResult(
            statistic=float(lr_cc),
            pvalue=pvalue,
            test_name="Christoffersen CC",
            df=3,
        )

    xǁVaRBacktestǁchristoffersen_test__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVaRBacktestǁchristoffersen_test__mutmut_1": xǁVaRBacktestǁchristoffersen_test__mutmut_1,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_2": xǁVaRBacktestǁchristoffersen_test__mutmut_2,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_3": xǁVaRBacktestǁchristoffersen_test__mutmut_3,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_4": xǁVaRBacktestǁchristoffersen_test__mutmut_4,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_5": xǁVaRBacktestǁchristoffersen_test__mutmut_5,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_6": xǁVaRBacktestǁchristoffersen_test__mutmut_6,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_7": xǁVaRBacktestǁchristoffersen_test__mutmut_7,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_8": xǁVaRBacktestǁchristoffersen_test__mutmut_8,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_9": xǁVaRBacktestǁchristoffersen_test__mutmut_9,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_10": xǁVaRBacktestǁchristoffersen_test__mutmut_10,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_11": xǁVaRBacktestǁchristoffersen_test__mutmut_11,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_12": xǁVaRBacktestǁchristoffersen_test__mutmut_12,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_13": xǁVaRBacktestǁchristoffersen_test__mutmut_13,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_14": xǁVaRBacktestǁchristoffersen_test__mutmut_14,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_15": xǁVaRBacktestǁchristoffersen_test__mutmut_15,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_16": xǁVaRBacktestǁchristoffersen_test__mutmut_16,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_17": xǁVaRBacktestǁchristoffersen_test__mutmut_17,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_18": xǁVaRBacktestǁchristoffersen_test__mutmut_18,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_19": xǁVaRBacktestǁchristoffersen_test__mutmut_19,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_20": xǁVaRBacktestǁchristoffersen_test__mutmut_20,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_21": xǁVaRBacktestǁchristoffersen_test__mutmut_21,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_22": xǁVaRBacktestǁchristoffersen_test__mutmut_22,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_23": xǁVaRBacktestǁchristoffersen_test__mutmut_23,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_24": xǁVaRBacktestǁchristoffersen_test__mutmut_24,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_25": xǁVaRBacktestǁchristoffersen_test__mutmut_25,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_26": xǁVaRBacktestǁchristoffersen_test__mutmut_26,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_27": xǁVaRBacktestǁchristoffersen_test__mutmut_27,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_28": xǁVaRBacktestǁchristoffersen_test__mutmut_28,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_29": xǁVaRBacktestǁchristoffersen_test__mutmut_29,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_30": xǁVaRBacktestǁchristoffersen_test__mutmut_30,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_31": xǁVaRBacktestǁchristoffersen_test__mutmut_31,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_32": xǁVaRBacktestǁchristoffersen_test__mutmut_32,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_33": xǁVaRBacktestǁchristoffersen_test__mutmut_33,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_34": xǁVaRBacktestǁchristoffersen_test__mutmut_34,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_35": xǁVaRBacktestǁchristoffersen_test__mutmut_35,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_36": xǁVaRBacktestǁchristoffersen_test__mutmut_36,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_37": xǁVaRBacktestǁchristoffersen_test__mutmut_37,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_38": xǁVaRBacktestǁchristoffersen_test__mutmut_38,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_39": xǁVaRBacktestǁchristoffersen_test__mutmut_39,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_40": xǁVaRBacktestǁchristoffersen_test__mutmut_40,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_41": xǁVaRBacktestǁchristoffersen_test__mutmut_41,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_42": xǁVaRBacktestǁchristoffersen_test__mutmut_42,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_43": xǁVaRBacktestǁchristoffersen_test__mutmut_43,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_44": xǁVaRBacktestǁchristoffersen_test__mutmut_44,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_45": xǁVaRBacktestǁchristoffersen_test__mutmut_45,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_46": xǁVaRBacktestǁchristoffersen_test__mutmut_46,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_47": xǁVaRBacktestǁchristoffersen_test__mutmut_47,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_48": xǁVaRBacktestǁchristoffersen_test__mutmut_48,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_49": xǁVaRBacktestǁchristoffersen_test__mutmut_49,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_50": xǁVaRBacktestǁchristoffersen_test__mutmut_50,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_51": xǁVaRBacktestǁchristoffersen_test__mutmut_51,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_52": xǁVaRBacktestǁchristoffersen_test__mutmut_52,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_53": xǁVaRBacktestǁchristoffersen_test__mutmut_53,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_54": xǁVaRBacktestǁchristoffersen_test__mutmut_54,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_55": xǁVaRBacktestǁchristoffersen_test__mutmut_55,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_56": xǁVaRBacktestǁchristoffersen_test__mutmut_56,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_57": xǁVaRBacktestǁchristoffersen_test__mutmut_57,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_58": xǁVaRBacktestǁchristoffersen_test__mutmut_58,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_59": xǁVaRBacktestǁchristoffersen_test__mutmut_59,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_60": xǁVaRBacktestǁchristoffersen_test__mutmut_60,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_61": xǁVaRBacktestǁchristoffersen_test__mutmut_61,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_62": xǁVaRBacktestǁchristoffersen_test__mutmut_62,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_63": xǁVaRBacktestǁchristoffersen_test__mutmut_63,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_64": xǁVaRBacktestǁchristoffersen_test__mutmut_64,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_65": xǁVaRBacktestǁchristoffersen_test__mutmut_65,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_66": xǁVaRBacktestǁchristoffersen_test__mutmut_66,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_67": xǁVaRBacktestǁchristoffersen_test__mutmut_67,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_68": xǁVaRBacktestǁchristoffersen_test__mutmut_68,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_69": xǁVaRBacktestǁchristoffersen_test__mutmut_69,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_70": xǁVaRBacktestǁchristoffersen_test__mutmut_70,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_71": xǁVaRBacktestǁchristoffersen_test__mutmut_71,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_72": xǁVaRBacktestǁchristoffersen_test__mutmut_72,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_73": xǁVaRBacktestǁchristoffersen_test__mutmut_73,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_74": xǁVaRBacktestǁchristoffersen_test__mutmut_74,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_75": xǁVaRBacktestǁchristoffersen_test__mutmut_75,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_76": xǁVaRBacktestǁchristoffersen_test__mutmut_76,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_77": xǁVaRBacktestǁchristoffersen_test__mutmut_77,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_78": xǁVaRBacktestǁchristoffersen_test__mutmut_78,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_79": xǁVaRBacktestǁchristoffersen_test__mutmut_79,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_80": xǁVaRBacktestǁchristoffersen_test__mutmut_80,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_81": xǁVaRBacktestǁchristoffersen_test__mutmut_81,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_82": xǁVaRBacktestǁchristoffersen_test__mutmut_82,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_83": xǁVaRBacktestǁchristoffersen_test__mutmut_83,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_84": xǁVaRBacktestǁchristoffersen_test__mutmut_84,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_85": xǁVaRBacktestǁchristoffersen_test__mutmut_85,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_86": xǁVaRBacktestǁchristoffersen_test__mutmut_86,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_87": xǁVaRBacktestǁchristoffersen_test__mutmut_87,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_88": xǁVaRBacktestǁchristoffersen_test__mutmut_88,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_89": xǁVaRBacktestǁchristoffersen_test__mutmut_89,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_90": xǁVaRBacktestǁchristoffersen_test__mutmut_90,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_91": xǁVaRBacktestǁchristoffersen_test__mutmut_91,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_92": xǁVaRBacktestǁchristoffersen_test__mutmut_92,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_93": xǁVaRBacktestǁchristoffersen_test__mutmut_93,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_94": xǁVaRBacktestǁchristoffersen_test__mutmut_94,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_95": xǁVaRBacktestǁchristoffersen_test__mutmut_95,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_96": xǁVaRBacktestǁchristoffersen_test__mutmut_96,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_97": xǁVaRBacktestǁchristoffersen_test__mutmut_97,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_98": xǁVaRBacktestǁchristoffersen_test__mutmut_98,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_99": xǁVaRBacktestǁchristoffersen_test__mutmut_99,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_100": xǁVaRBacktestǁchristoffersen_test__mutmut_100,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_101": xǁVaRBacktestǁchristoffersen_test__mutmut_101,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_102": xǁVaRBacktestǁchristoffersen_test__mutmut_102,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_103": xǁVaRBacktestǁchristoffersen_test__mutmut_103,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_104": xǁVaRBacktestǁchristoffersen_test__mutmut_104,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_105": xǁVaRBacktestǁchristoffersen_test__mutmut_105,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_106": xǁVaRBacktestǁchristoffersen_test__mutmut_106,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_107": xǁVaRBacktestǁchristoffersen_test__mutmut_107,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_108": xǁVaRBacktestǁchristoffersen_test__mutmut_108,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_109": xǁVaRBacktestǁchristoffersen_test__mutmut_109,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_110": xǁVaRBacktestǁchristoffersen_test__mutmut_110,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_111": xǁVaRBacktestǁchristoffersen_test__mutmut_111,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_112": xǁVaRBacktestǁchristoffersen_test__mutmut_112,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_113": xǁVaRBacktestǁchristoffersen_test__mutmut_113,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_114": xǁVaRBacktestǁchristoffersen_test__mutmut_114,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_115": xǁVaRBacktestǁchristoffersen_test__mutmut_115,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_116": xǁVaRBacktestǁchristoffersen_test__mutmut_116,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_117": xǁVaRBacktestǁchristoffersen_test__mutmut_117,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_118": xǁVaRBacktestǁchristoffersen_test__mutmut_118,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_119": xǁVaRBacktestǁchristoffersen_test__mutmut_119,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_120": xǁVaRBacktestǁchristoffersen_test__mutmut_120,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_121": xǁVaRBacktestǁchristoffersen_test__mutmut_121,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_122": xǁVaRBacktestǁchristoffersen_test__mutmut_122,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_123": xǁVaRBacktestǁchristoffersen_test__mutmut_123,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_124": xǁVaRBacktestǁchristoffersen_test__mutmut_124,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_125": xǁVaRBacktestǁchristoffersen_test__mutmut_125,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_126": xǁVaRBacktestǁchristoffersen_test__mutmut_126,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_127": xǁVaRBacktestǁchristoffersen_test__mutmut_127,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_128": xǁVaRBacktestǁchristoffersen_test__mutmut_128,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_129": xǁVaRBacktestǁchristoffersen_test__mutmut_129,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_130": xǁVaRBacktestǁchristoffersen_test__mutmut_130,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_131": xǁVaRBacktestǁchristoffersen_test__mutmut_131,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_132": xǁVaRBacktestǁchristoffersen_test__mutmut_132,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_133": xǁVaRBacktestǁchristoffersen_test__mutmut_133,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_134": xǁVaRBacktestǁchristoffersen_test__mutmut_134,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_135": xǁVaRBacktestǁchristoffersen_test__mutmut_135,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_136": xǁVaRBacktestǁchristoffersen_test__mutmut_136,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_137": xǁVaRBacktestǁchristoffersen_test__mutmut_137,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_138": xǁVaRBacktestǁchristoffersen_test__mutmut_138,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_139": xǁVaRBacktestǁchristoffersen_test__mutmut_139,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_140": xǁVaRBacktestǁchristoffersen_test__mutmut_140,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_141": xǁVaRBacktestǁchristoffersen_test__mutmut_141,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_142": xǁVaRBacktestǁchristoffersen_test__mutmut_142,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_143": xǁVaRBacktestǁchristoffersen_test__mutmut_143,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_144": xǁVaRBacktestǁchristoffersen_test__mutmut_144,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_145": xǁVaRBacktestǁchristoffersen_test__mutmut_145,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_146": xǁVaRBacktestǁchristoffersen_test__mutmut_146,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_147": xǁVaRBacktestǁchristoffersen_test__mutmut_147,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_148": xǁVaRBacktestǁchristoffersen_test__mutmut_148,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_149": xǁVaRBacktestǁchristoffersen_test__mutmut_149,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_150": xǁVaRBacktestǁchristoffersen_test__mutmut_150,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_151": xǁVaRBacktestǁchristoffersen_test__mutmut_151,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_152": xǁVaRBacktestǁchristoffersen_test__mutmut_152,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_153": xǁVaRBacktestǁchristoffersen_test__mutmut_153,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_154": xǁVaRBacktestǁchristoffersen_test__mutmut_154,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_155": xǁVaRBacktestǁchristoffersen_test__mutmut_155,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_156": xǁVaRBacktestǁchristoffersen_test__mutmut_156,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_157": xǁVaRBacktestǁchristoffersen_test__mutmut_157,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_158": xǁVaRBacktestǁchristoffersen_test__mutmut_158,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_159": xǁVaRBacktestǁchristoffersen_test__mutmut_159,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_160": xǁVaRBacktestǁchristoffersen_test__mutmut_160,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_161": xǁVaRBacktestǁchristoffersen_test__mutmut_161,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_162": xǁVaRBacktestǁchristoffersen_test__mutmut_162,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_163": xǁVaRBacktestǁchristoffersen_test__mutmut_163,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_164": xǁVaRBacktestǁchristoffersen_test__mutmut_164,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_165": xǁVaRBacktestǁchristoffersen_test__mutmut_165,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_166": xǁVaRBacktestǁchristoffersen_test__mutmut_166,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_167": xǁVaRBacktestǁchristoffersen_test__mutmut_167,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_168": xǁVaRBacktestǁchristoffersen_test__mutmut_168,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_169": xǁVaRBacktestǁchristoffersen_test__mutmut_169,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_170": xǁVaRBacktestǁchristoffersen_test__mutmut_170,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_171": xǁVaRBacktestǁchristoffersen_test__mutmut_171,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_172": xǁVaRBacktestǁchristoffersen_test__mutmut_172,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_173": xǁVaRBacktestǁchristoffersen_test__mutmut_173,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_174": xǁVaRBacktestǁchristoffersen_test__mutmut_174,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_175": xǁVaRBacktestǁchristoffersen_test__mutmut_175,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_176": xǁVaRBacktestǁchristoffersen_test__mutmut_176,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_177": xǁVaRBacktestǁchristoffersen_test__mutmut_177,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_178": xǁVaRBacktestǁchristoffersen_test__mutmut_178,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_179": xǁVaRBacktestǁchristoffersen_test__mutmut_179,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_180": xǁVaRBacktestǁchristoffersen_test__mutmut_180,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_181": xǁVaRBacktestǁchristoffersen_test__mutmut_181,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_182": xǁVaRBacktestǁchristoffersen_test__mutmut_182,
        "xǁVaRBacktestǁchristoffersen_test__mutmut_183": xǁVaRBacktestǁchristoffersen_test__mutmut_183,
    }
    xǁVaRBacktestǁchristoffersen_test__mutmut_orig.__name__ = "xǁVaRBacktestǁchristoffersen_test"

    def basel_traffic_light(self, window: int = 250) -> str:
        args = [window]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVaRBacktestǁbasel_traffic_light__mutmut_orig"),
            object.__getattribute__(self, "xǁVaRBacktestǁbasel_traffic_light__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_orig(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_1(self, window: int = 251) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_2(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = None
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_3(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[+window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_4(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) > window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_5(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = None

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_6(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(None)

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_7(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(None))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_8(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations < 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_9(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 5:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_10(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "XXgreenXX"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_11(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "GREEN"
        if n_violations <= 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_12(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations < 9:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_13(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 10:
            return "yellow"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_14(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "XXyellowXX"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_15(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "YELLOW"
        return "red"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_16(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "XXredXX"

    def xǁVaRBacktestǁbasel_traffic_light__mutmut_17(self, window: int = 250) -> str:
        """Basel traffic light system.

        Parameters
        ----------
        window : int
            Backtesting window in days. Default is 250.

        Returns
        -------
        str
            'green', 'yellow', or 'red'.

        Notes
        -----
        For 250 days at alpha=1%:
            - Green: 0-4 violations
            - Yellow: 5-9 violations
            - Red: 10+ violations
        """
        # Use last `window` observations
        hits_window = self.hits[-window:] if len(self.hits) >= window else self.hits
        n_violations = int(np.sum(hits_window))

        if n_violations <= 4:
            return "green"
        if n_violations <= 9:
            return "yellow"
        return "RED"

    xǁVaRBacktestǁbasel_traffic_light__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_1": xǁVaRBacktestǁbasel_traffic_light__mutmut_1,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_2": xǁVaRBacktestǁbasel_traffic_light__mutmut_2,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_3": xǁVaRBacktestǁbasel_traffic_light__mutmut_3,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_4": xǁVaRBacktestǁbasel_traffic_light__mutmut_4,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_5": xǁVaRBacktestǁbasel_traffic_light__mutmut_5,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_6": xǁVaRBacktestǁbasel_traffic_light__mutmut_6,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_7": xǁVaRBacktestǁbasel_traffic_light__mutmut_7,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_8": xǁVaRBacktestǁbasel_traffic_light__mutmut_8,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_9": xǁVaRBacktestǁbasel_traffic_light__mutmut_9,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_10": xǁVaRBacktestǁbasel_traffic_light__mutmut_10,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_11": xǁVaRBacktestǁbasel_traffic_light__mutmut_11,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_12": xǁVaRBacktestǁbasel_traffic_light__mutmut_12,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_13": xǁVaRBacktestǁbasel_traffic_light__mutmut_13,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_14": xǁVaRBacktestǁbasel_traffic_light__mutmut_14,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_15": xǁVaRBacktestǁbasel_traffic_light__mutmut_15,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_16": xǁVaRBacktestǁbasel_traffic_light__mutmut_16,
        "xǁVaRBacktestǁbasel_traffic_light__mutmut_17": xǁVaRBacktestǁbasel_traffic_light__mutmut_17,
    }
    xǁVaRBacktestǁbasel_traffic_light__mutmut_orig.__name__ = "xǁVaRBacktestǁbasel_traffic_light"

    def violation_ratio(self) -> float:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVaRBacktestǁviolation_ratio__mutmut_orig"),
            object.__getattribute__(self, "xǁVaRBacktestǁviolation_ratio__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVaRBacktestǁviolation_ratio__mutmut_orig(self) -> float:
        """Compute the violation ratio.

        Returns
        -------
        float
            Observed violation rate / expected violation rate (alpha).
            A ratio of 1.0 indicates perfect calibration.
        """
        observed_rate = self.hits.mean()
        return float(observed_rate / self.alpha)

    def xǁVaRBacktestǁviolation_ratio__mutmut_1(self) -> float:
        """Compute the violation ratio.

        Returns
        -------
        float
            Observed violation rate / expected violation rate (alpha).
            A ratio of 1.0 indicates perfect calibration.
        """
        observed_rate = None
        return float(observed_rate / self.alpha)

    def xǁVaRBacktestǁviolation_ratio__mutmut_2(self) -> float:
        """Compute the violation ratio.

        Returns
        -------
        float
            Observed violation rate / expected violation rate (alpha).
            A ratio of 1.0 indicates perfect calibration.
        """
        observed_rate = self.hits.mean()
        return float(None)

    def xǁVaRBacktestǁviolation_ratio__mutmut_3(self) -> float:
        """Compute the violation ratio.

        Returns
        -------
        float
            Observed violation rate / expected violation rate (alpha).
            A ratio of 1.0 indicates perfect calibration.
        """
        observed_rate = self.hits.mean()
        return float(observed_rate * self.alpha)

    xǁVaRBacktestǁviolation_ratio__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVaRBacktestǁviolation_ratio__mutmut_1": xǁVaRBacktestǁviolation_ratio__mutmut_1,
        "xǁVaRBacktestǁviolation_ratio__mutmut_2": xǁVaRBacktestǁviolation_ratio__mutmut_2,
        "xǁVaRBacktestǁviolation_ratio__mutmut_3": xǁVaRBacktestǁviolation_ratio__mutmut_3,
    }
    xǁVaRBacktestǁviolation_ratio__mutmut_orig.__name__ = "xǁVaRBacktestǁviolation_ratio"

    def summary(self) -> str:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁVaRBacktestǁsummary__mutmut_orig"),
            object.__getattribute__(self, "xǁVaRBacktestǁsummary__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁVaRBacktestǁsummary__mutmut_orig(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_1(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = None
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_2(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = None
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_3(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = None
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_4(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = None

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_5(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = None
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_6(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = None
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_7(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(None)
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_8(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(None))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_9(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = None

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_10(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = None

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_11(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" / 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_12(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "XX=XX" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_13(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 61,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_14(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "XXVaR Backtest SummaryXX",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_15(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "var backtest summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_16(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VAR BACKTEST SUMMARY",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_17(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" / 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_18(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "XX=XX" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_19(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 61,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_20(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "XXXX",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_21(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" / 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_22(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "XX-XX" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_23(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 61,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_24(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "XXStatistical TestsXX",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_25(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "statistical tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_26(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "STATISTICAL TESTS",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_27(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" / 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_28(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "XX-XX" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_29(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 61,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_30(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "XXXX",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_31(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" / 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_32(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "XX-XX" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_33(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 61,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_34(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.lower()}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_35(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" / 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_36(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "XX=XX" * 60,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_37(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 61,
        ]

        return "\n".join(lines)

    def xǁVaRBacktestǁsummary__mutmut_38(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "\n".join(None)

    def xǁVaRBacktestǁsummary__mutmut_39(self) -> str:
        """Generate a full backtest report.

        Returns
        -------
        str
            Formatted report with all test results.
        """
        kupiec = self.kupiec_test()
        christoffersen = self.christoffersen_test()
        traffic = self.basel_traffic_light()
        vr = self.violation_ratio()

        n = len(self.hits)
        x = int(np.sum(self.hits))
        rate = self.hits.mean()

        lines = [
            "=" * 60,
            "VaR Backtest Summary",
            "=" * 60,
            f"  Observations:      {n}",
            f"  VaR level (alpha): {self.alpha:.4f}",
            f"  Violations:        {x}",
            f"  Violation rate:    {rate:.4f}",
            f"  Violation ratio:   {vr:.4f}",
            "",
            "-" * 60,
            "Statistical Tests",
            "-" * 60,
            f"  {kupiec}",
            f"  {christoffersen}",
            "",
            "-" * 60,
            f"  Basel Traffic Light: {traffic.upper()}",
            "=" * 60,
        ]

        return "XX\nXX".join(lines)

    xǁVaRBacktestǁsummary__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁVaRBacktestǁsummary__mutmut_1": xǁVaRBacktestǁsummary__mutmut_1,
        "xǁVaRBacktestǁsummary__mutmut_2": xǁVaRBacktestǁsummary__mutmut_2,
        "xǁVaRBacktestǁsummary__mutmut_3": xǁVaRBacktestǁsummary__mutmut_3,
        "xǁVaRBacktestǁsummary__mutmut_4": xǁVaRBacktestǁsummary__mutmut_4,
        "xǁVaRBacktestǁsummary__mutmut_5": xǁVaRBacktestǁsummary__mutmut_5,
        "xǁVaRBacktestǁsummary__mutmut_6": xǁVaRBacktestǁsummary__mutmut_6,
        "xǁVaRBacktestǁsummary__mutmut_7": xǁVaRBacktestǁsummary__mutmut_7,
        "xǁVaRBacktestǁsummary__mutmut_8": xǁVaRBacktestǁsummary__mutmut_8,
        "xǁVaRBacktestǁsummary__mutmut_9": xǁVaRBacktestǁsummary__mutmut_9,
        "xǁVaRBacktestǁsummary__mutmut_10": xǁVaRBacktestǁsummary__mutmut_10,
        "xǁVaRBacktestǁsummary__mutmut_11": xǁVaRBacktestǁsummary__mutmut_11,
        "xǁVaRBacktestǁsummary__mutmut_12": xǁVaRBacktestǁsummary__mutmut_12,
        "xǁVaRBacktestǁsummary__mutmut_13": xǁVaRBacktestǁsummary__mutmut_13,
        "xǁVaRBacktestǁsummary__mutmut_14": xǁVaRBacktestǁsummary__mutmut_14,
        "xǁVaRBacktestǁsummary__mutmut_15": xǁVaRBacktestǁsummary__mutmut_15,
        "xǁVaRBacktestǁsummary__mutmut_16": xǁVaRBacktestǁsummary__mutmut_16,
        "xǁVaRBacktestǁsummary__mutmut_17": xǁVaRBacktestǁsummary__mutmut_17,
        "xǁVaRBacktestǁsummary__mutmut_18": xǁVaRBacktestǁsummary__mutmut_18,
        "xǁVaRBacktestǁsummary__mutmut_19": xǁVaRBacktestǁsummary__mutmut_19,
        "xǁVaRBacktestǁsummary__mutmut_20": xǁVaRBacktestǁsummary__mutmut_20,
        "xǁVaRBacktestǁsummary__mutmut_21": xǁVaRBacktestǁsummary__mutmut_21,
        "xǁVaRBacktestǁsummary__mutmut_22": xǁVaRBacktestǁsummary__mutmut_22,
        "xǁVaRBacktestǁsummary__mutmut_23": xǁVaRBacktestǁsummary__mutmut_23,
        "xǁVaRBacktestǁsummary__mutmut_24": xǁVaRBacktestǁsummary__mutmut_24,
        "xǁVaRBacktestǁsummary__mutmut_25": xǁVaRBacktestǁsummary__mutmut_25,
        "xǁVaRBacktestǁsummary__mutmut_26": xǁVaRBacktestǁsummary__mutmut_26,
        "xǁVaRBacktestǁsummary__mutmut_27": xǁVaRBacktestǁsummary__mutmut_27,
        "xǁVaRBacktestǁsummary__mutmut_28": xǁVaRBacktestǁsummary__mutmut_28,
        "xǁVaRBacktestǁsummary__mutmut_29": xǁVaRBacktestǁsummary__mutmut_29,
        "xǁVaRBacktestǁsummary__mutmut_30": xǁVaRBacktestǁsummary__mutmut_30,
        "xǁVaRBacktestǁsummary__mutmut_31": xǁVaRBacktestǁsummary__mutmut_31,
        "xǁVaRBacktestǁsummary__mutmut_32": xǁVaRBacktestǁsummary__mutmut_32,
        "xǁVaRBacktestǁsummary__mutmut_33": xǁVaRBacktestǁsummary__mutmut_33,
        "xǁVaRBacktestǁsummary__mutmut_34": xǁVaRBacktestǁsummary__mutmut_34,
        "xǁVaRBacktestǁsummary__mutmut_35": xǁVaRBacktestǁsummary__mutmut_35,
        "xǁVaRBacktestǁsummary__mutmut_36": xǁVaRBacktestǁsummary__mutmut_36,
        "xǁVaRBacktestǁsummary__mutmut_37": xǁVaRBacktestǁsummary__mutmut_37,
        "xǁVaRBacktestǁsummary__mutmut_38": xǁVaRBacktestǁsummary__mutmut_38,
        "xǁVaRBacktestǁsummary__mutmut_39": xǁVaRBacktestǁsummary__mutmut_39,
    }
    xǁVaRBacktestǁsummary__mutmut_orig.__name__ = "xǁVaRBacktestǁsummary"
