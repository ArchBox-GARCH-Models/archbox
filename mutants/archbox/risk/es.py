"""Expected Shortfall (ES / CVaR) implementations.

The Expected Shortfall at level alpha is the expected loss given that
the loss exceeds the VaR at the same level.

Methods:
    - Parametric (Normal, Student-t)
    - Historical
    - Filtered Historical Simulation

References
----------
- Artzner, P., Delbaen, F., Eber, J.-M. & Heath, D. (1999).
  Coherent Measures of Risk. Mathematical Finance, 9(3), 203-228.
- McNeil, A.J., Frey, R. & Embrechts, P. (2015).
  Quantitative Risk Management. 2nd ed. Princeton University Press. Cap. 2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from scipy import stats

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


class ExpectedShortfall:
    """Expected Shortfall (CVaR) calculator.

    Parameters
    ----------
    results : ArchResults
        Fitted model results from archbox.
    alpha : float
        Significance level (e.g., 0.05 for 5% ES). Default is 0.05.

    Attributes
    ----------
    results : ArchResults
        The fitted model results.
    alpha : float
        Significance level.
    returns : NDArray[np.float64]
        The return series.
    conditional_volatility : NDArray[np.float64]
        Conditional volatility series sigma_t.
    """

    def __init__(self, results: object, alpha: float = 0.05) -> None:
        args = [results, alpha]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁExpectedShortfallǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁExpectedShortfallǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁExpectedShortfallǁ__init____mutmut_orig(
        self, results: object, alpha: float = 0.05
    ) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_1(self, results: object, alpha: float = 1.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_2(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_3(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 1 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_4(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 <= alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_5(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha <= 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_6(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 2:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_7(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = None
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_8(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(None)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_9(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = None
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_10(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = None

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_11(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = None
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_12(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(None, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_13(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, None, None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_14(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr("resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_15(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_16(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = results.resids
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_17(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "XXresidsXX", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_18(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "RESIDS", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_19(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is not None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_20(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = None
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_21(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(None, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_22(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, None, None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_23(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr("resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_24(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_25(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = results.resid
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_26(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "XXresidXX", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_27(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "RESID", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_28(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is not None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_29(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = None
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_30(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(None, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_31(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, None, None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_32(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr("endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_33(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_34(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = results.endog
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_35(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "XXendogXX", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_36(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "ENDOG", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_37(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = None
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_38(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(None, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_39(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=None)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_40(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_41(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(
            raw,
        )
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_42(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = None
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_43(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            None,
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_44(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=None,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_45(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_46(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_47(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(None, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_48(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, None, None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_49(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr("conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_50(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_51(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            results.conditional_volatility,
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_52(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "XXconditional_volatilityXX", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_53(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "CONDITIONAL_VOLATILITY", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_54(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = None

    def xǁExpectedShortfallǁ__init____mutmut_55(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(None)

    def xǁExpectedShortfallǁ__init____mutmut_56(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(None, "mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_57(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, None, 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_58(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", None))

    def xǁExpectedShortfallǁ__init____mutmut_59(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr("mu", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_60(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_61(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(results.mu)

    def xǁExpectedShortfallǁ__init____mutmut_62(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "XXmuXX", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_63(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "MU", 0.0))

    def xǁExpectedShortfallǁ__init____mutmut_64(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Expected Shortfall calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = np.asarray(
            getattr(results, "conditional_volatility", None),
            dtype=np.float64,
        )
        self.mu: float = float(getattr(results, "mu", 1.0))

    xǁExpectedShortfallǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁExpectedShortfallǁ__init____mutmut_1": xǁExpectedShortfallǁ__init____mutmut_1,
        "xǁExpectedShortfallǁ__init____mutmut_2": xǁExpectedShortfallǁ__init____mutmut_2,
        "xǁExpectedShortfallǁ__init____mutmut_3": xǁExpectedShortfallǁ__init____mutmut_3,
        "xǁExpectedShortfallǁ__init____mutmut_4": xǁExpectedShortfallǁ__init____mutmut_4,
        "xǁExpectedShortfallǁ__init____mutmut_5": xǁExpectedShortfallǁ__init____mutmut_5,
        "xǁExpectedShortfallǁ__init____mutmut_6": xǁExpectedShortfallǁ__init____mutmut_6,
        "xǁExpectedShortfallǁ__init____mutmut_7": xǁExpectedShortfallǁ__init____mutmut_7,
        "xǁExpectedShortfallǁ__init____mutmut_8": xǁExpectedShortfallǁ__init____mutmut_8,
        "xǁExpectedShortfallǁ__init____mutmut_9": xǁExpectedShortfallǁ__init____mutmut_9,
        "xǁExpectedShortfallǁ__init____mutmut_10": xǁExpectedShortfallǁ__init____mutmut_10,
        "xǁExpectedShortfallǁ__init____mutmut_11": xǁExpectedShortfallǁ__init____mutmut_11,
        "xǁExpectedShortfallǁ__init____mutmut_12": xǁExpectedShortfallǁ__init____mutmut_12,
        "xǁExpectedShortfallǁ__init____mutmut_13": xǁExpectedShortfallǁ__init____mutmut_13,
        "xǁExpectedShortfallǁ__init____mutmut_14": xǁExpectedShortfallǁ__init____mutmut_14,
        "xǁExpectedShortfallǁ__init____mutmut_15": xǁExpectedShortfallǁ__init____mutmut_15,
        "xǁExpectedShortfallǁ__init____mutmut_16": xǁExpectedShortfallǁ__init____mutmut_16,
        "xǁExpectedShortfallǁ__init____mutmut_17": xǁExpectedShortfallǁ__init____mutmut_17,
        "xǁExpectedShortfallǁ__init____mutmut_18": xǁExpectedShortfallǁ__init____mutmut_18,
        "xǁExpectedShortfallǁ__init____mutmut_19": xǁExpectedShortfallǁ__init____mutmut_19,
        "xǁExpectedShortfallǁ__init____mutmut_20": xǁExpectedShortfallǁ__init____mutmut_20,
        "xǁExpectedShortfallǁ__init____mutmut_21": xǁExpectedShortfallǁ__init____mutmut_21,
        "xǁExpectedShortfallǁ__init____mutmut_22": xǁExpectedShortfallǁ__init____mutmut_22,
        "xǁExpectedShortfallǁ__init____mutmut_23": xǁExpectedShortfallǁ__init____mutmut_23,
        "xǁExpectedShortfallǁ__init____mutmut_24": xǁExpectedShortfallǁ__init____mutmut_24,
        "xǁExpectedShortfallǁ__init____mutmut_25": xǁExpectedShortfallǁ__init____mutmut_25,
        "xǁExpectedShortfallǁ__init____mutmut_26": xǁExpectedShortfallǁ__init____mutmut_26,
        "xǁExpectedShortfallǁ__init____mutmut_27": xǁExpectedShortfallǁ__init____mutmut_27,
        "xǁExpectedShortfallǁ__init____mutmut_28": xǁExpectedShortfallǁ__init____mutmut_28,
        "xǁExpectedShortfallǁ__init____mutmut_29": xǁExpectedShortfallǁ__init____mutmut_29,
        "xǁExpectedShortfallǁ__init____mutmut_30": xǁExpectedShortfallǁ__init____mutmut_30,
        "xǁExpectedShortfallǁ__init____mutmut_31": xǁExpectedShortfallǁ__init____mutmut_31,
        "xǁExpectedShortfallǁ__init____mutmut_32": xǁExpectedShortfallǁ__init____mutmut_32,
        "xǁExpectedShortfallǁ__init____mutmut_33": xǁExpectedShortfallǁ__init____mutmut_33,
        "xǁExpectedShortfallǁ__init____mutmut_34": xǁExpectedShortfallǁ__init____mutmut_34,
        "xǁExpectedShortfallǁ__init____mutmut_35": xǁExpectedShortfallǁ__init____mutmut_35,
        "xǁExpectedShortfallǁ__init____mutmut_36": xǁExpectedShortfallǁ__init____mutmut_36,
        "xǁExpectedShortfallǁ__init____mutmut_37": xǁExpectedShortfallǁ__init____mutmut_37,
        "xǁExpectedShortfallǁ__init____mutmut_38": xǁExpectedShortfallǁ__init____mutmut_38,
        "xǁExpectedShortfallǁ__init____mutmut_39": xǁExpectedShortfallǁ__init____mutmut_39,
        "xǁExpectedShortfallǁ__init____mutmut_40": xǁExpectedShortfallǁ__init____mutmut_40,
        "xǁExpectedShortfallǁ__init____mutmut_41": xǁExpectedShortfallǁ__init____mutmut_41,
        "xǁExpectedShortfallǁ__init____mutmut_42": xǁExpectedShortfallǁ__init____mutmut_42,
        "xǁExpectedShortfallǁ__init____mutmut_43": xǁExpectedShortfallǁ__init____mutmut_43,
        "xǁExpectedShortfallǁ__init____mutmut_44": xǁExpectedShortfallǁ__init____mutmut_44,
        "xǁExpectedShortfallǁ__init____mutmut_45": xǁExpectedShortfallǁ__init____mutmut_45,
        "xǁExpectedShortfallǁ__init____mutmut_46": xǁExpectedShortfallǁ__init____mutmut_46,
        "xǁExpectedShortfallǁ__init____mutmut_47": xǁExpectedShortfallǁ__init____mutmut_47,
        "xǁExpectedShortfallǁ__init____mutmut_48": xǁExpectedShortfallǁ__init____mutmut_48,
        "xǁExpectedShortfallǁ__init____mutmut_49": xǁExpectedShortfallǁ__init____mutmut_49,
        "xǁExpectedShortfallǁ__init____mutmut_50": xǁExpectedShortfallǁ__init____mutmut_50,
        "xǁExpectedShortfallǁ__init____mutmut_51": xǁExpectedShortfallǁ__init____mutmut_51,
        "xǁExpectedShortfallǁ__init____mutmut_52": xǁExpectedShortfallǁ__init____mutmut_52,
        "xǁExpectedShortfallǁ__init____mutmut_53": xǁExpectedShortfallǁ__init____mutmut_53,
        "xǁExpectedShortfallǁ__init____mutmut_54": xǁExpectedShortfallǁ__init____mutmut_54,
        "xǁExpectedShortfallǁ__init____mutmut_55": xǁExpectedShortfallǁ__init____mutmut_55,
        "xǁExpectedShortfallǁ__init____mutmut_56": xǁExpectedShortfallǁ__init____mutmut_56,
        "xǁExpectedShortfallǁ__init____mutmut_57": xǁExpectedShortfallǁ__init____mutmut_57,
        "xǁExpectedShortfallǁ__init____mutmut_58": xǁExpectedShortfallǁ__init____mutmut_58,
        "xǁExpectedShortfallǁ__init____mutmut_59": xǁExpectedShortfallǁ__init____mutmut_59,
        "xǁExpectedShortfallǁ__init____mutmut_60": xǁExpectedShortfallǁ__init____mutmut_60,
        "xǁExpectedShortfallǁ__init____mutmut_61": xǁExpectedShortfallǁ__init____mutmut_61,
        "xǁExpectedShortfallǁ__init____mutmut_62": xǁExpectedShortfallǁ__init____mutmut_62,
        "xǁExpectedShortfallǁ__init____mutmut_63": xǁExpectedShortfallǁ__init____mutmut_63,
        "xǁExpectedShortfallǁ__init____mutmut_64": xǁExpectedShortfallǁ__init____mutmut_64,
    }
    xǁExpectedShortfallǁ__init____mutmut_orig.__name__ = "xǁExpectedShortfallǁ__init__"

    def parametric(self, dist: str = "normal", nu: float = 8.0) -> NDArray[np.float64]:
        args = [dist, nu]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁExpectedShortfallǁparametric__mutmut_orig"),
            object.__getattribute__(self, "xǁExpectedShortfallǁparametric__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁExpectedShortfallǁparametric__mutmut_orig(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_1(
        self, dist: str = "XXnormalXX", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_2(
        self, dist: str = "NORMAL", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_3(
        self, dist: str = "normal", nu: float = 9.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_4(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = None

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_5(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist != "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_6(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "XXnormalXX":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_7(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "NORMAL":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_8(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = None
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_9(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(None)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_10(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = None
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_11(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(None)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_12(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu + sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_13(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z * self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_14(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma / phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_15(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist != "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_16(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "XXstudenttXX":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_17(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "STUDENTT":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_18(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu < 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_19(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 3:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_20(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = None
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_21(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(None)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_22(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = None
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_23(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(None, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_24(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=None)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_25(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_26(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(
                self.alpha,
            )
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_27(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = None
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_28(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(None, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_29(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=None)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_30(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_31(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(
                t_alpha,
            )
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_32(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = None
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_33(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt(None)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_34(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) * nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_35(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu + 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_36(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 3) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_37(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = None
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_38(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) / ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_39(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu * self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_40(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) * (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_41(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu - t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_42(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha * 2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_43(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**3) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_44(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu + 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_45(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 2))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_46(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu + sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_47(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor / scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_48(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma / es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_49(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = None
        raise ValueError(msg)

    def xǁExpectedShortfallǁparametric__mutmut_50(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric Expected Shortfall.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). Negative values indicate expected losses.

        Notes
        -----
        Normal:
            ES_alpha = mu - sigma * phi(z_alpha) / alpha

        Student-t:
            ES_alpha = mu - sigma * (f_nu(t_alpha) / alpha) *
                       ((nu + t_alpha^2) / (nu - 1)) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            phi_z = stats.norm.pdf(z_alpha)
            return self.mu - sigma * phi_z / self.alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            f_nu = stats.t.pdf(t_alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            es_factor = (f_nu / self.alpha) * ((nu + t_alpha**2) / (nu - 1))
            return self.mu - sigma * es_factor * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(None)

    xǁExpectedShortfallǁparametric__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁExpectedShortfallǁparametric__mutmut_1": xǁExpectedShortfallǁparametric__mutmut_1,
        "xǁExpectedShortfallǁparametric__mutmut_2": xǁExpectedShortfallǁparametric__mutmut_2,
        "xǁExpectedShortfallǁparametric__mutmut_3": xǁExpectedShortfallǁparametric__mutmut_3,
        "xǁExpectedShortfallǁparametric__mutmut_4": xǁExpectedShortfallǁparametric__mutmut_4,
        "xǁExpectedShortfallǁparametric__mutmut_5": xǁExpectedShortfallǁparametric__mutmut_5,
        "xǁExpectedShortfallǁparametric__mutmut_6": xǁExpectedShortfallǁparametric__mutmut_6,
        "xǁExpectedShortfallǁparametric__mutmut_7": xǁExpectedShortfallǁparametric__mutmut_7,
        "xǁExpectedShortfallǁparametric__mutmut_8": xǁExpectedShortfallǁparametric__mutmut_8,
        "xǁExpectedShortfallǁparametric__mutmut_9": xǁExpectedShortfallǁparametric__mutmut_9,
        "xǁExpectedShortfallǁparametric__mutmut_10": xǁExpectedShortfallǁparametric__mutmut_10,
        "xǁExpectedShortfallǁparametric__mutmut_11": xǁExpectedShortfallǁparametric__mutmut_11,
        "xǁExpectedShortfallǁparametric__mutmut_12": xǁExpectedShortfallǁparametric__mutmut_12,
        "xǁExpectedShortfallǁparametric__mutmut_13": xǁExpectedShortfallǁparametric__mutmut_13,
        "xǁExpectedShortfallǁparametric__mutmut_14": xǁExpectedShortfallǁparametric__mutmut_14,
        "xǁExpectedShortfallǁparametric__mutmut_15": xǁExpectedShortfallǁparametric__mutmut_15,
        "xǁExpectedShortfallǁparametric__mutmut_16": xǁExpectedShortfallǁparametric__mutmut_16,
        "xǁExpectedShortfallǁparametric__mutmut_17": xǁExpectedShortfallǁparametric__mutmut_17,
        "xǁExpectedShortfallǁparametric__mutmut_18": xǁExpectedShortfallǁparametric__mutmut_18,
        "xǁExpectedShortfallǁparametric__mutmut_19": xǁExpectedShortfallǁparametric__mutmut_19,
        "xǁExpectedShortfallǁparametric__mutmut_20": xǁExpectedShortfallǁparametric__mutmut_20,
        "xǁExpectedShortfallǁparametric__mutmut_21": xǁExpectedShortfallǁparametric__mutmut_21,
        "xǁExpectedShortfallǁparametric__mutmut_22": xǁExpectedShortfallǁparametric__mutmut_22,
        "xǁExpectedShortfallǁparametric__mutmut_23": xǁExpectedShortfallǁparametric__mutmut_23,
        "xǁExpectedShortfallǁparametric__mutmut_24": xǁExpectedShortfallǁparametric__mutmut_24,
        "xǁExpectedShortfallǁparametric__mutmut_25": xǁExpectedShortfallǁparametric__mutmut_25,
        "xǁExpectedShortfallǁparametric__mutmut_26": xǁExpectedShortfallǁparametric__mutmut_26,
        "xǁExpectedShortfallǁparametric__mutmut_27": xǁExpectedShortfallǁparametric__mutmut_27,
        "xǁExpectedShortfallǁparametric__mutmut_28": xǁExpectedShortfallǁparametric__mutmut_28,
        "xǁExpectedShortfallǁparametric__mutmut_29": xǁExpectedShortfallǁparametric__mutmut_29,
        "xǁExpectedShortfallǁparametric__mutmut_30": xǁExpectedShortfallǁparametric__mutmut_30,
        "xǁExpectedShortfallǁparametric__mutmut_31": xǁExpectedShortfallǁparametric__mutmut_31,
        "xǁExpectedShortfallǁparametric__mutmut_32": xǁExpectedShortfallǁparametric__mutmut_32,
        "xǁExpectedShortfallǁparametric__mutmut_33": xǁExpectedShortfallǁparametric__mutmut_33,
        "xǁExpectedShortfallǁparametric__mutmut_34": xǁExpectedShortfallǁparametric__mutmut_34,
        "xǁExpectedShortfallǁparametric__mutmut_35": xǁExpectedShortfallǁparametric__mutmut_35,
        "xǁExpectedShortfallǁparametric__mutmut_36": xǁExpectedShortfallǁparametric__mutmut_36,
        "xǁExpectedShortfallǁparametric__mutmut_37": xǁExpectedShortfallǁparametric__mutmut_37,
        "xǁExpectedShortfallǁparametric__mutmut_38": xǁExpectedShortfallǁparametric__mutmut_38,
        "xǁExpectedShortfallǁparametric__mutmut_39": xǁExpectedShortfallǁparametric__mutmut_39,
        "xǁExpectedShortfallǁparametric__mutmut_40": xǁExpectedShortfallǁparametric__mutmut_40,
        "xǁExpectedShortfallǁparametric__mutmut_41": xǁExpectedShortfallǁparametric__mutmut_41,
        "xǁExpectedShortfallǁparametric__mutmut_42": xǁExpectedShortfallǁparametric__mutmut_42,
        "xǁExpectedShortfallǁparametric__mutmut_43": xǁExpectedShortfallǁparametric__mutmut_43,
        "xǁExpectedShortfallǁparametric__mutmut_44": xǁExpectedShortfallǁparametric__mutmut_44,
        "xǁExpectedShortfallǁparametric__mutmut_45": xǁExpectedShortfallǁparametric__mutmut_45,
        "xǁExpectedShortfallǁparametric__mutmut_46": xǁExpectedShortfallǁparametric__mutmut_46,
        "xǁExpectedShortfallǁparametric__mutmut_47": xǁExpectedShortfallǁparametric__mutmut_47,
        "xǁExpectedShortfallǁparametric__mutmut_48": xǁExpectedShortfallǁparametric__mutmut_48,
        "xǁExpectedShortfallǁparametric__mutmut_49": xǁExpectedShortfallǁparametric__mutmut_49,
        "xǁExpectedShortfallǁparametric__mutmut_50": xǁExpectedShortfallǁparametric__mutmut_50,
    }
    xǁExpectedShortfallǁparametric__mutmut_orig.__name__ = "xǁExpectedShortfallǁparametric"

    def historical(self, window: int = 250) -> NDArray[np.float64]:
        args = [window]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁExpectedShortfallǁhistorical__mutmut_orig"),
            object.__getattribute__(self, "xǁExpectedShortfallǁhistorical__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁExpectedShortfallǁhistorical__mutmut_orig(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_1(self, window: int = 251) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_2(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = None
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_3(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = None

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_4(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(None, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_5(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, None)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_6(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_7(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(
            n_obs,
        )

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_8(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(None, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_9(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, None):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_10(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_11(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(
            window,
        ):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_12(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = None
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_13(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t + window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_14(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = None
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_15(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(None, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_16(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, None)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_17(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_18(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(
                rolling_window,
            )
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_19(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = None
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_20(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window < var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_21(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = None

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_22(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(None) if len(tail) > 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_23(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) >= 0 else var_alpha

        return es_series

    def xǁExpectedShortfallǁhistorical__mutmut_24(self, window: int = 250) -> NDArray[np.float64]:
        """Compute ES by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,). First `window` values are NaN.

        Notes
        -----
        ES_alpha = mean(r_t | r_t < VaR_alpha) in rolling window.
        """
        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_alpha = np.quantile(rolling_window, self.alpha)
            tail = rolling_window[rolling_window <= var_alpha]
            es_series[t] = np.mean(tail) if len(tail) > 1 else var_alpha

        return es_series

    xǁExpectedShortfallǁhistorical__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁExpectedShortfallǁhistorical__mutmut_1": xǁExpectedShortfallǁhistorical__mutmut_1,
        "xǁExpectedShortfallǁhistorical__mutmut_2": xǁExpectedShortfallǁhistorical__mutmut_2,
        "xǁExpectedShortfallǁhistorical__mutmut_3": xǁExpectedShortfallǁhistorical__mutmut_3,
        "xǁExpectedShortfallǁhistorical__mutmut_4": xǁExpectedShortfallǁhistorical__mutmut_4,
        "xǁExpectedShortfallǁhistorical__mutmut_5": xǁExpectedShortfallǁhistorical__mutmut_5,
        "xǁExpectedShortfallǁhistorical__mutmut_6": xǁExpectedShortfallǁhistorical__mutmut_6,
        "xǁExpectedShortfallǁhistorical__mutmut_7": xǁExpectedShortfallǁhistorical__mutmut_7,
        "xǁExpectedShortfallǁhistorical__mutmut_8": xǁExpectedShortfallǁhistorical__mutmut_8,
        "xǁExpectedShortfallǁhistorical__mutmut_9": xǁExpectedShortfallǁhistorical__mutmut_9,
        "xǁExpectedShortfallǁhistorical__mutmut_10": xǁExpectedShortfallǁhistorical__mutmut_10,
        "xǁExpectedShortfallǁhistorical__mutmut_11": xǁExpectedShortfallǁhistorical__mutmut_11,
        "xǁExpectedShortfallǁhistorical__mutmut_12": xǁExpectedShortfallǁhistorical__mutmut_12,
        "xǁExpectedShortfallǁhistorical__mutmut_13": xǁExpectedShortfallǁhistorical__mutmut_13,
        "xǁExpectedShortfallǁhistorical__mutmut_14": xǁExpectedShortfallǁhistorical__mutmut_14,
        "xǁExpectedShortfallǁhistorical__mutmut_15": xǁExpectedShortfallǁhistorical__mutmut_15,
        "xǁExpectedShortfallǁhistorical__mutmut_16": xǁExpectedShortfallǁhistorical__mutmut_16,
        "xǁExpectedShortfallǁhistorical__mutmut_17": xǁExpectedShortfallǁhistorical__mutmut_17,
        "xǁExpectedShortfallǁhistorical__mutmut_18": xǁExpectedShortfallǁhistorical__mutmut_18,
        "xǁExpectedShortfallǁhistorical__mutmut_19": xǁExpectedShortfallǁhistorical__mutmut_19,
        "xǁExpectedShortfallǁhistorical__mutmut_20": xǁExpectedShortfallǁhistorical__mutmut_20,
        "xǁExpectedShortfallǁhistorical__mutmut_21": xǁExpectedShortfallǁhistorical__mutmut_21,
        "xǁExpectedShortfallǁhistorical__mutmut_22": xǁExpectedShortfallǁhistorical__mutmut_22,
        "xǁExpectedShortfallǁhistorical__mutmut_23": xǁExpectedShortfallǁhistorical__mutmut_23,
        "xǁExpectedShortfallǁhistorical__mutmut_24": xǁExpectedShortfallǁhistorical__mutmut_24,
    }
    xǁExpectedShortfallǁhistorical__mutmut_orig.__name__ = "xǁExpectedShortfallǁhistorical"

    def filtered_historical(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁExpectedShortfallǁfiltered_historical__mutmut_orig"),
            object.__getattribute__(
                self, "xǁExpectedShortfallǁfiltered_historical__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁExpectedShortfallǁfiltered_historical__mutmut_orig(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_1(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = None
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_2(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns + self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_3(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = None
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_4(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = None
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_5(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(None, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_6(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, None)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_7(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_8(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(
            sigma,
        )
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_9(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1.000000000001)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_10(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = None

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_11(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids * sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_12(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = None
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_13(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = None

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_14(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(None, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_15(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, None)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_16(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_17(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(
            n_obs,
        )

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_18(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = None
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_19(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 51
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_20(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(None, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_21(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, None):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_22(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_23(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(
            min_obs,
        ):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_24(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = None
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_25(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = None
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_26(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(None, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_27(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, None)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_28(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_29(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(
                z_window,
            )
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_30(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = None
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_31(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window < z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_32(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = None
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_33(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(None) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_34(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) >= 0 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_35(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 1 else z_quantile
            es_series[t] = self.mu + sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_36(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = None

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_37(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu - sigma[t] * es_z

        return es_series

    def xǁExpectedShortfallǁfiltered_historical__mutmut_38(self) -> NDArray[np.float64]:
        """Compute ES by Filtered Historical Simulation.

        Returns
        -------
        NDArray[np.float64]
            ES series, shape (T,).

        Notes
        -----
        1. z_t = (r_t - mu) / sigma_t
        2. ES_t = mu + sigma_t * mean(z_s | z_s < quantile(z; alpha))
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        es_series = np.full(n_obs, np.nan)

        min_obs = 50
        for t in range(min_obs, n_obs):
            z_window = std_resids[:t]
            z_quantile = np.quantile(z_window, self.alpha)
            tail = z_window[z_window <= z_quantile]
            es_z = np.mean(tail) if len(tail) > 0 else z_quantile
            es_series[t] = self.mu + sigma[t] / es_z

        return es_series

    xǁExpectedShortfallǁfiltered_historical__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁExpectedShortfallǁfiltered_historical__mutmut_1": xǁExpectedShortfallǁfiltered_historical__mutmut_1,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_2": xǁExpectedShortfallǁfiltered_historical__mutmut_2,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_3": xǁExpectedShortfallǁfiltered_historical__mutmut_3,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_4": xǁExpectedShortfallǁfiltered_historical__mutmut_4,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_5": xǁExpectedShortfallǁfiltered_historical__mutmut_5,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_6": xǁExpectedShortfallǁfiltered_historical__mutmut_6,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_7": xǁExpectedShortfallǁfiltered_historical__mutmut_7,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_8": xǁExpectedShortfallǁfiltered_historical__mutmut_8,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_9": xǁExpectedShortfallǁfiltered_historical__mutmut_9,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_10": xǁExpectedShortfallǁfiltered_historical__mutmut_10,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_11": xǁExpectedShortfallǁfiltered_historical__mutmut_11,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_12": xǁExpectedShortfallǁfiltered_historical__mutmut_12,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_13": xǁExpectedShortfallǁfiltered_historical__mutmut_13,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_14": xǁExpectedShortfallǁfiltered_historical__mutmut_14,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_15": xǁExpectedShortfallǁfiltered_historical__mutmut_15,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_16": xǁExpectedShortfallǁfiltered_historical__mutmut_16,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_17": xǁExpectedShortfallǁfiltered_historical__mutmut_17,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_18": xǁExpectedShortfallǁfiltered_historical__mutmut_18,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_19": xǁExpectedShortfallǁfiltered_historical__mutmut_19,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_20": xǁExpectedShortfallǁfiltered_historical__mutmut_20,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_21": xǁExpectedShortfallǁfiltered_historical__mutmut_21,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_22": xǁExpectedShortfallǁfiltered_historical__mutmut_22,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_23": xǁExpectedShortfallǁfiltered_historical__mutmut_23,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_24": xǁExpectedShortfallǁfiltered_historical__mutmut_24,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_25": xǁExpectedShortfallǁfiltered_historical__mutmut_25,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_26": xǁExpectedShortfallǁfiltered_historical__mutmut_26,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_27": xǁExpectedShortfallǁfiltered_historical__mutmut_27,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_28": xǁExpectedShortfallǁfiltered_historical__mutmut_28,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_29": xǁExpectedShortfallǁfiltered_historical__mutmut_29,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_30": xǁExpectedShortfallǁfiltered_historical__mutmut_30,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_31": xǁExpectedShortfallǁfiltered_historical__mutmut_31,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_32": xǁExpectedShortfallǁfiltered_historical__mutmut_32,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_33": xǁExpectedShortfallǁfiltered_historical__mutmut_33,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_34": xǁExpectedShortfallǁfiltered_historical__mutmut_34,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_35": xǁExpectedShortfallǁfiltered_historical__mutmut_35,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_36": xǁExpectedShortfallǁfiltered_historical__mutmut_36,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_37": xǁExpectedShortfallǁfiltered_historical__mutmut_37,
        "xǁExpectedShortfallǁfiltered_historical__mutmut_38": xǁExpectedShortfallǁfiltered_historical__mutmut_38,
    }
    xǁExpectedShortfallǁfiltered_historical__mutmut_orig.__name__ = (
        "xǁExpectedShortfallǁfiltered_historical"
    )
