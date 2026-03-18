"""Value at Risk (VaR) implementations.

Methods:
    - Parametric (Normal, Student-t)
    - Historical Simulation
    - Filtered Historical Simulation (Barone-Adesi et al., 1999)
    - Monte Carlo

References
----------
- Barone-Adesi, G., Giannopoulos, K. & Vosper, L. (1999).
  VaR Without Correlations for Portfolios of Derivative Securities.
  Journal of Futures Markets, 19(5), 583-602.
- McNeil, A.J., Frey, R. & Embrechts, P. (2015).
  Quantitative Risk Management. 2nd ed. Princeton University Press.
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


class ValueAtRisk:
    """Value at Risk calculator.

    Parameters
    ----------
    results : ArchResults
        Fitted model results from archbox.
    alpha : float
        Significance level (e.g., 0.05 for 5% VaR). Default is 0.05.

    Attributes
    ----------
    results : ArchResults
        The fitted model results.
    alpha : float
        Significance level.
    returns : NDArray[np.float64]
        The return series from the fitted model.
    conditional_volatility : NDArray[np.float64]
        Conditional volatility series sigma_t.
    """

    def __init__(self, results: object, alpha: float = 0.05) -> None:
        args = [results, alpha]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁValueAtRiskǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁValueAtRiskǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁValueAtRiskǁ__init____mutmut_orig(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_1(self, results: object, alpha: float = 1.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_2(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_3(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 1 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_4(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 <= alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_5(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha <= 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_6(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 2:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_7(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = None
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_8(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(None)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_9(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = None
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_10(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = None

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_11(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_12(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_13(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_14(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_15(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_16(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_17(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_18(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_19(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_20(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_21(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_22(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_23(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_24(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_25(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_26(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_27(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_28(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_29(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_30(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_31(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_32(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_33(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_34(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_35(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_36(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_37(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_38(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_39(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_40(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_41(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_42(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
        raw = getattr(results, "resids", None)
        if raw is None:
            raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "endog", None)
        self.returns: NDArray[np.float64] = np.asarray(raw, dtype=np.float64)
        self.conditional_volatility: NDArray[np.float64] = None
        self.mu: float = float(getattr(results, "mu", 0.0))

    def xǁValueAtRiskǁ__init____mutmut_43(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_44(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_45(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_46(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_47(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_48(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_49(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_50(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_51(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_52(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_53(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_54(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_55(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_56(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_57(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_58(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_59(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_60(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_61(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_62(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_63(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    def xǁValueAtRiskǁ__init____mutmut_64(self, results: object, alpha: float = 0.05) -> None:
        """Initialize Value-at-Risk calculator from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = alpha

        # Extract data from results
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

    xǁValueAtRiskǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁValueAtRiskǁ__init____mutmut_1": xǁValueAtRiskǁ__init____mutmut_1,
        "xǁValueAtRiskǁ__init____mutmut_2": xǁValueAtRiskǁ__init____mutmut_2,
        "xǁValueAtRiskǁ__init____mutmut_3": xǁValueAtRiskǁ__init____mutmut_3,
        "xǁValueAtRiskǁ__init____mutmut_4": xǁValueAtRiskǁ__init____mutmut_4,
        "xǁValueAtRiskǁ__init____mutmut_5": xǁValueAtRiskǁ__init____mutmut_5,
        "xǁValueAtRiskǁ__init____mutmut_6": xǁValueAtRiskǁ__init____mutmut_6,
        "xǁValueAtRiskǁ__init____mutmut_7": xǁValueAtRiskǁ__init____mutmut_7,
        "xǁValueAtRiskǁ__init____mutmut_8": xǁValueAtRiskǁ__init____mutmut_8,
        "xǁValueAtRiskǁ__init____mutmut_9": xǁValueAtRiskǁ__init____mutmut_9,
        "xǁValueAtRiskǁ__init____mutmut_10": xǁValueAtRiskǁ__init____mutmut_10,
        "xǁValueAtRiskǁ__init____mutmut_11": xǁValueAtRiskǁ__init____mutmut_11,
        "xǁValueAtRiskǁ__init____mutmut_12": xǁValueAtRiskǁ__init____mutmut_12,
        "xǁValueAtRiskǁ__init____mutmut_13": xǁValueAtRiskǁ__init____mutmut_13,
        "xǁValueAtRiskǁ__init____mutmut_14": xǁValueAtRiskǁ__init____mutmut_14,
        "xǁValueAtRiskǁ__init____mutmut_15": xǁValueAtRiskǁ__init____mutmut_15,
        "xǁValueAtRiskǁ__init____mutmut_16": xǁValueAtRiskǁ__init____mutmut_16,
        "xǁValueAtRiskǁ__init____mutmut_17": xǁValueAtRiskǁ__init____mutmut_17,
        "xǁValueAtRiskǁ__init____mutmut_18": xǁValueAtRiskǁ__init____mutmut_18,
        "xǁValueAtRiskǁ__init____mutmut_19": xǁValueAtRiskǁ__init____mutmut_19,
        "xǁValueAtRiskǁ__init____mutmut_20": xǁValueAtRiskǁ__init____mutmut_20,
        "xǁValueAtRiskǁ__init____mutmut_21": xǁValueAtRiskǁ__init____mutmut_21,
        "xǁValueAtRiskǁ__init____mutmut_22": xǁValueAtRiskǁ__init____mutmut_22,
        "xǁValueAtRiskǁ__init____mutmut_23": xǁValueAtRiskǁ__init____mutmut_23,
        "xǁValueAtRiskǁ__init____mutmut_24": xǁValueAtRiskǁ__init____mutmut_24,
        "xǁValueAtRiskǁ__init____mutmut_25": xǁValueAtRiskǁ__init____mutmut_25,
        "xǁValueAtRiskǁ__init____mutmut_26": xǁValueAtRiskǁ__init____mutmut_26,
        "xǁValueAtRiskǁ__init____mutmut_27": xǁValueAtRiskǁ__init____mutmut_27,
        "xǁValueAtRiskǁ__init____mutmut_28": xǁValueAtRiskǁ__init____mutmut_28,
        "xǁValueAtRiskǁ__init____mutmut_29": xǁValueAtRiskǁ__init____mutmut_29,
        "xǁValueAtRiskǁ__init____mutmut_30": xǁValueAtRiskǁ__init____mutmut_30,
        "xǁValueAtRiskǁ__init____mutmut_31": xǁValueAtRiskǁ__init____mutmut_31,
        "xǁValueAtRiskǁ__init____mutmut_32": xǁValueAtRiskǁ__init____mutmut_32,
        "xǁValueAtRiskǁ__init____mutmut_33": xǁValueAtRiskǁ__init____mutmut_33,
        "xǁValueAtRiskǁ__init____mutmut_34": xǁValueAtRiskǁ__init____mutmut_34,
        "xǁValueAtRiskǁ__init____mutmut_35": xǁValueAtRiskǁ__init____mutmut_35,
        "xǁValueAtRiskǁ__init____mutmut_36": xǁValueAtRiskǁ__init____mutmut_36,
        "xǁValueAtRiskǁ__init____mutmut_37": xǁValueAtRiskǁ__init____mutmut_37,
        "xǁValueAtRiskǁ__init____mutmut_38": xǁValueAtRiskǁ__init____mutmut_38,
        "xǁValueAtRiskǁ__init____mutmut_39": xǁValueAtRiskǁ__init____mutmut_39,
        "xǁValueAtRiskǁ__init____mutmut_40": xǁValueAtRiskǁ__init____mutmut_40,
        "xǁValueAtRiskǁ__init____mutmut_41": xǁValueAtRiskǁ__init____mutmut_41,
        "xǁValueAtRiskǁ__init____mutmut_42": xǁValueAtRiskǁ__init____mutmut_42,
        "xǁValueAtRiskǁ__init____mutmut_43": xǁValueAtRiskǁ__init____mutmut_43,
        "xǁValueAtRiskǁ__init____mutmut_44": xǁValueAtRiskǁ__init____mutmut_44,
        "xǁValueAtRiskǁ__init____mutmut_45": xǁValueAtRiskǁ__init____mutmut_45,
        "xǁValueAtRiskǁ__init____mutmut_46": xǁValueAtRiskǁ__init____mutmut_46,
        "xǁValueAtRiskǁ__init____mutmut_47": xǁValueAtRiskǁ__init____mutmut_47,
        "xǁValueAtRiskǁ__init____mutmut_48": xǁValueAtRiskǁ__init____mutmut_48,
        "xǁValueAtRiskǁ__init____mutmut_49": xǁValueAtRiskǁ__init____mutmut_49,
        "xǁValueAtRiskǁ__init____mutmut_50": xǁValueAtRiskǁ__init____mutmut_50,
        "xǁValueAtRiskǁ__init____mutmut_51": xǁValueAtRiskǁ__init____mutmut_51,
        "xǁValueAtRiskǁ__init____mutmut_52": xǁValueAtRiskǁ__init____mutmut_52,
        "xǁValueAtRiskǁ__init____mutmut_53": xǁValueAtRiskǁ__init____mutmut_53,
        "xǁValueAtRiskǁ__init____mutmut_54": xǁValueAtRiskǁ__init____mutmut_54,
        "xǁValueAtRiskǁ__init____mutmut_55": xǁValueAtRiskǁ__init____mutmut_55,
        "xǁValueAtRiskǁ__init____mutmut_56": xǁValueAtRiskǁ__init____mutmut_56,
        "xǁValueAtRiskǁ__init____mutmut_57": xǁValueAtRiskǁ__init____mutmut_57,
        "xǁValueAtRiskǁ__init____mutmut_58": xǁValueAtRiskǁ__init____mutmut_58,
        "xǁValueAtRiskǁ__init____mutmut_59": xǁValueAtRiskǁ__init____mutmut_59,
        "xǁValueAtRiskǁ__init____mutmut_60": xǁValueAtRiskǁ__init____mutmut_60,
        "xǁValueAtRiskǁ__init____mutmut_61": xǁValueAtRiskǁ__init____mutmut_61,
        "xǁValueAtRiskǁ__init____mutmut_62": xǁValueAtRiskǁ__init____mutmut_62,
        "xǁValueAtRiskǁ__init____mutmut_63": xǁValueAtRiskǁ__init____mutmut_63,
        "xǁValueAtRiskǁ__init____mutmut_64": xǁValueAtRiskǁ__init____mutmut_64,
    }
    xǁValueAtRiskǁ__init____mutmut_orig.__name__ = "xǁValueAtRiskǁ__init__"

    def parametric(self, dist: str = "normal", nu: float = 8.0) -> NDArray[np.float64]:
        args = [dist, nu]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁValueAtRiskǁparametric__mutmut_orig"),
            object.__getattribute__(self, "xǁValueAtRiskǁparametric__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁValueAtRiskǁparametric__mutmut_orig(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_1(
        self, dist: str = "XXnormalXX", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_2(
        self, dist: str = "NORMAL", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_3(
        self, dist: str = "normal", nu: float = 9.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_4(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = None

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_5(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist != "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_6(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "XXnormalXX":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_7(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "NORMAL":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_8(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = None
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_9(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(None)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_10(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu - sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_11(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma / z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_12(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist != "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_13(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "XXstudenttXX":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_14(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "STUDENTT":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_15(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu < 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_16(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 3:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_17(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = None
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_18(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(None)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_19(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = None
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_20(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(None, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_21(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=None)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_22(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_23(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(
                self.alpha,
            )
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_24(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = None
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_25(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt(None)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_26(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) * nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_27(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu + 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_28(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 3) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_29(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu - sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_30(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha / scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_31(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma / t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_32(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = None
        raise ValueError(msg)

    def xǁValueAtRiskǁparametric__mutmut_33(
        self, dist: str = "normal", nu: float = 8.0
    ) -> NDArray[np.float64]:
        """Compute parametric VaR.

        Parameters
        ----------
        dist : str
            Distribution: 'normal' or 'studentt'. Default is 'normal'.
        nu : float
            Degrees of freedom for Student-t. Default is 8.0.

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). Negative values indicate losses.

        Notes
        -----
        Normal:
            VaR_alpha = mu + sigma_t * Phi^{-1}(alpha)

        Student-t:
            VaR_alpha = mu + sigma_t * t^{-1}_nu(alpha) * sqrt((nu-2)/nu)
        """
        sigma = self.conditional_volatility

        if dist == "normal":
            z_alpha = stats.norm.ppf(self.alpha)
            return self.mu + sigma * z_alpha

        if dist == "studentt":
            if nu <= 2:
                msg = f"Degrees of freedom must be > 2, got {nu}"
                raise ValueError(msg)
            t_alpha = stats.t.ppf(self.alpha, df=nu)
            scale = np.sqrt((nu - 2) / nu)
            return self.mu + sigma * t_alpha * scale

        msg = f"Unknown distribution: {dist}. Use 'normal' or 'studentt'."
        raise ValueError(None)

    xǁValueAtRiskǁparametric__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁValueAtRiskǁparametric__mutmut_1": xǁValueAtRiskǁparametric__mutmut_1,
        "xǁValueAtRiskǁparametric__mutmut_2": xǁValueAtRiskǁparametric__mutmut_2,
        "xǁValueAtRiskǁparametric__mutmut_3": xǁValueAtRiskǁparametric__mutmut_3,
        "xǁValueAtRiskǁparametric__mutmut_4": xǁValueAtRiskǁparametric__mutmut_4,
        "xǁValueAtRiskǁparametric__mutmut_5": xǁValueAtRiskǁparametric__mutmut_5,
        "xǁValueAtRiskǁparametric__mutmut_6": xǁValueAtRiskǁparametric__mutmut_6,
        "xǁValueAtRiskǁparametric__mutmut_7": xǁValueAtRiskǁparametric__mutmut_7,
        "xǁValueAtRiskǁparametric__mutmut_8": xǁValueAtRiskǁparametric__mutmut_8,
        "xǁValueAtRiskǁparametric__mutmut_9": xǁValueAtRiskǁparametric__mutmut_9,
        "xǁValueAtRiskǁparametric__mutmut_10": xǁValueAtRiskǁparametric__mutmut_10,
        "xǁValueAtRiskǁparametric__mutmut_11": xǁValueAtRiskǁparametric__mutmut_11,
        "xǁValueAtRiskǁparametric__mutmut_12": xǁValueAtRiskǁparametric__mutmut_12,
        "xǁValueAtRiskǁparametric__mutmut_13": xǁValueAtRiskǁparametric__mutmut_13,
        "xǁValueAtRiskǁparametric__mutmut_14": xǁValueAtRiskǁparametric__mutmut_14,
        "xǁValueAtRiskǁparametric__mutmut_15": xǁValueAtRiskǁparametric__mutmut_15,
        "xǁValueAtRiskǁparametric__mutmut_16": xǁValueAtRiskǁparametric__mutmut_16,
        "xǁValueAtRiskǁparametric__mutmut_17": xǁValueAtRiskǁparametric__mutmut_17,
        "xǁValueAtRiskǁparametric__mutmut_18": xǁValueAtRiskǁparametric__mutmut_18,
        "xǁValueAtRiskǁparametric__mutmut_19": xǁValueAtRiskǁparametric__mutmut_19,
        "xǁValueAtRiskǁparametric__mutmut_20": xǁValueAtRiskǁparametric__mutmut_20,
        "xǁValueAtRiskǁparametric__mutmut_21": xǁValueAtRiskǁparametric__mutmut_21,
        "xǁValueAtRiskǁparametric__mutmut_22": xǁValueAtRiskǁparametric__mutmut_22,
        "xǁValueAtRiskǁparametric__mutmut_23": xǁValueAtRiskǁparametric__mutmut_23,
        "xǁValueAtRiskǁparametric__mutmut_24": xǁValueAtRiskǁparametric__mutmut_24,
        "xǁValueAtRiskǁparametric__mutmut_25": xǁValueAtRiskǁparametric__mutmut_25,
        "xǁValueAtRiskǁparametric__mutmut_26": xǁValueAtRiskǁparametric__mutmut_26,
        "xǁValueAtRiskǁparametric__mutmut_27": xǁValueAtRiskǁparametric__mutmut_27,
        "xǁValueAtRiskǁparametric__mutmut_28": xǁValueAtRiskǁparametric__mutmut_28,
        "xǁValueAtRiskǁparametric__mutmut_29": xǁValueAtRiskǁparametric__mutmut_29,
        "xǁValueAtRiskǁparametric__mutmut_30": xǁValueAtRiskǁparametric__mutmut_30,
        "xǁValueAtRiskǁparametric__mutmut_31": xǁValueAtRiskǁparametric__mutmut_31,
        "xǁValueAtRiskǁparametric__mutmut_32": xǁValueAtRiskǁparametric__mutmut_32,
        "xǁValueAtRiskǁparametric__mutmut_33": xǁValueAtRiskǁparametric__mutmut_33,
    }
    xǁValueAtRiskǁparametric__mutmut_orig.__name__ = "xǁValueAtRiskǁparametric"

    def historical(self, window: int = 250) -> NDArray[np.float64]:
        args = [window]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁValueAtRiskǁhistorical__mutmut_orig"),
            object.__getattribute__(self, "xǁValueAtRiskǁhistorical__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁValueAtRiskǁhistorical__mutmut_orig(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_1(self, window: int = 251) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_2(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = None
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_3(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = None

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_4(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(None, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_5(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, None)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_6(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_7(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(
            n_obs,
        )

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_8(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(None, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_9(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, None):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_10(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_11(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(
            window,
        ):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_12(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = None
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_13(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t + window : t]
            var_series[t] = np.quantile(rolling_window, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_14(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = None

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_15(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(None, self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_16(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(rolling_window, None)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_17(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(self.alpha)

        return var_series

    def xǁValueAtRiskǁhistorical__mutmut_18(self, window: int = 250) -> NDArray[np.float64]:
        """Compute VaR by Historical Simulation.

        Parameters
        ----------
        window : int
            Rolling window size. Default is 250 (approx. 1 year).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,). First `window` values are NaN.

        Notes
        -----
        VaR_alpha = quantile(r_{t-W+1}, ..., r_t ; alpha)
        """
        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        for t in range(window, n_obs):
            rolling_window = self.returns[t - window : t]
            var_series[t] = np.quantile(
                rolling_window,
            )

        return var_series

    xǁValueAtRiskǁhistorical__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁValueAtRiskǁhistorical__mutmut_1": xǁValueAtRiskǁhistorical__mutmut_1,
        "xǁValueAtRiskǁhistorical__mutmut_2": xǁValueAtRiskǁhistorical__mutmut_2,
        "xǁValueAtRiskǁhistorical__mutmut_3": xǁValueAtRiskǁhistorical__mutmut_3,
        "xǁValueAtRiskǁhistorical__mutmut_4": xǁValueAtRiskǁhistorical__mutmut_4,
        "xǁValueAtRiskǁhistorical__mutmut_5": xǁValueAtRiskǁhistorical__mutmut_5,
        "xǁValueAtRiskǁhistorical__mutmut_6": xǁValueAtRiskǁhistorical__mutmut_6,
        "xǁValueAtRiskǁhistorical__mutmut_7": xǁValueAtRiskǁhistorical__mutmut_7,
        "xǁValueAtRiskǁhistorical__mutmut_8": xǁValueAtRiskǁhistorical__mutmut_8,
        "xǁValueAtRiskǁhistorical__mutmut_9": xǁValueAtRiskǁhistorical__mutmut_9,
        "xǁValueAtRiskǁhistorical__mutmut_10": xǁValueAtRiskǁhistorical__mutmut_10,
        "xǁValueAtRiskǁhistorical__mutmut_11": xǁValueAtRiskǁhistorical__mutmut_11,
        "xǁValueAtRiskǁhistorical__mutmut_12": xǁValueAtRiskǁhistorical__mutmut_12,
        "xǁValueAtRiskǁhistorical__mutmut_13": xǁValueAtRiskǁhistorical__mutmut_13,
        "xǁValueAtRiskǁhistorical__mutmut_14": xǁValueAtRiskǁhistorical__mutmut_14,
        "xǁValueAtRiskǁhistorical__mutmut_15": xǁValueAtRiskǁhistorical__mutmut_15,
        "xǁValueAtRiskǁhistorical__mutmut_16": xǁValueAtRiskǁhistorical__mutmut_16,
        "xǁValueAtRiskǁhistorical__mutmut_17": xǁValueAtRiskǁhistorical__mutmut_17,
        "xǁValueAtRiskǁhistorical__mutmut_18": xǁValueAtRiskǁhistorical__mutmut_18,
    }
    xǁValueAtRiskǁhistorical__mutmut_orig.__name__ = "xǁValueAtRiskǁhistorical"

    def filtered_historical(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁValueAtRiskǁfiltered_historical__mutmut_orig"),
            object.__getattribute__(self, "xǁValueAtRiskǁfiltered_historical__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁValueAtRiskǁfiltered_historical__mutmut_orig(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_1(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = None
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_2(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns + self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_3(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = None
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_4(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = None
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_5(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(None, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_6(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, None)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_7(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_8(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(
            sigma,
        )
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_9(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1.000000000001)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_10(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = None

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_11(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids * sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_12(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = None
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_13(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = None

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_14(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(None, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_15(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, None)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_16(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_17(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(
            n_obs,
        )

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_18(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = None
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_19(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 51
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_20(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(None, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_21(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, None):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_22(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_23(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(
            min_obs,
        ):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_24(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = None
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_25(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(None, self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_26(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], None)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_27(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(self.alpha)
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_28(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(
                std_resids[:t],
            )
            var_series[t] = self.mu + sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_29(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = None

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_30(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu - sigma[t] * z_quantile

        return var_series

    def xǁValueAtRiskǁfiltered_historical__mutmut_31(self) -> NDArray[np.float64]:
        """Compute VaR by Filtered Historical Simulation (FHS).

        Returns
        -------
        NDArray[np.float64]
            VaR series, shape (T,).

        Notes
        -----
        Barone-Adesi et al. (1999):
            1. z_t = (r_t - mu) / sigma_t  (standardized residuals)
            2. VaR_t = mu + sigma_t * quantile(z_1, ..., z_{t-1} ; alpha)

        The FHS method combines the GARCH volatility dynamics with the
        empirical distribution of standardized residuals.
        """
        resids = self.returns - self.mu
        sigma = self.conditional_volatility
        # Avoid division by zero
        sigma_safe = np.maximum(sigma, 1e-12)
        std_resids = resids / sigma_safe

        n_obs = len(self.returns)
        var_series = np.full(n_obs, np.nan)

        # Need at least some observations for quantile
        min_obs = 50
        for t in range(min_obs, n_obs):
            z_quantile = np.quantile(std_resids[:t], self.alpha)
            var_series[t] = self.mu + sigma[t] / z_quantile

        return var_series

    xǁValueAtRiskǁfiltered_historical__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁValueAtRiskǁfiltered_historical__mutmut_1": xǁValueAtRiskǁfiltered_historical__mutmut_1,
        "xǁValueAtRiskǁfiltered_historical__mutmut_2": xǁValueAtRiskǁfiltered_historical__mutmut_2,
        "xǁValueAtRiskǁfiltered_historical__mutmut_3": xǁValueAtRiskǁfiltered_historical__mutmut_3,
        "xǁValueAtRiskǁfiltered_historical__mutmut_4": xǁValueAtRiskǁfiltered_historical__mutmut_4,
        "xǁValueAtRiskǁfiltered_historical__mutmut_5": xǁValueAtRiskǁfiltered_historical__mutmut_5,
        "xǁValueAtRiskǁfiltered_historical__mutmut_6": xǁValueAtRiskǁfiltered_historical__mutmut_6,
        "xǁValueAtRiskǁfiltered_historical__mutmut_7": xǁValueAtRiskǁfiltered_historical__mutmut_7,
        "xǁValueAtRiskǁfiltered_historical__mutmut_8": xǁValueAtRiskǁfiltered_historical__mutmut_8,
        "xǁValueAtRiskǁfiltered_historical__mutmut_9": xǁValueAtRiskǁfiltered_historical__mutmut_9,
        "xǁValueAtRiskǁfiltered_historical__mutmut_10": xǁValueAtRiskǁfiltered_historical__mutmut_10,
        "xǁValueAtRiskǁfiltered_historical__mutmut_11": xǁValueAtRiskǁfiltered_historical__mutmut_11,
        "xǁValueAtRiskǁfiltered_historical__mutmut_12": xǁValueAtRiskǁfiltered_historical__mutmut_12,
        "xǁValueAtRiskǁfiltered_historical__mutmut_13": xǁValueAtRiskǁfiltered_historical__mutmut_13,
        "xǁValueAtRiskǁfiltered_historical__mutmut_14": xǁValueAtRiskǁfiltered_historical__mutmut_14,
        "xǁValueAtRiskǁfiltered_historical__mutmut_15": xǁValueAtRiskǁfiltered_historical__mutmut_15,
        "xǁValueAtRiskǁfiltered_historical__mutmut_16": xǁValueAtRiskǁfiltered_historical__mutmut_16,
        "xǁValueAtRiskǁfiltered_historical__mutmut_17": xǁValueAtRiskǁfiltered_historical__mutmut_17,
        "xǁValueAtRiskǁfiltered_historical__mutmut_18": xǁValueAtRiskǁfiltered_historical__mutmut_18,
        "xǁValueAtRiskǁfiltered_historical__mutmut_19": xǁValueAtRiskǁfiltered_historical__mutmut_19,
        "xǁValueAtRiskǁfiltered_historical__mutmut_20": xǁValueAtRiskǁfiltered_historical__mutmut_20,
        "xǁValueAtRiskǁfiltered_historical__mutmut_21": xǁValueAtRiskǁfiltered_historical__mutmut_21,
        "xǁValueAtRiskǁfiltered_historical__mutmut_22": xǁValueAtRiskǁfiltered_historical__mutmut_22,
        "xǁValueAtRiskǁfiltered_historical__mutmut_23": xǁValueAtRiskǁfiltered_historical__mutmut_23,
        "xǁValueAtRiskǁfiltered_historical__mutmut_24": xǁValueAtRiskǁfiltered_historical__mutmut_24,
        "xǁValueAtRiskǁfiltered_historical__mutmut_25": xǁValueAtRiskǁfiltered_historical__mutmut_25,
        "xǁValueAtRiskǁfiltered_historical__mutmut_26": xǁValueAtRiskǁfiltered_historical__mutmut_26,
        "xǁValueAtRiskǁfiltered_historical__mutmut_27": xǁValueAtRiskǁfiltered_historical__mutmut_27,
        "xǁValueAtRiskǁfiltered_historical__mutmut_28": xǁValueAtRiskǁfiltered_historical__mutmut_28,
        "xǁValueAtRiskǁfiltered_historical__mutmut_29": xǁValueAtRiskǁfiltered_historical__mutmut_29,
        "xǁValueAtRiskǁfiltered_historical__mutmut_30": xǁValueAtRiskǁfiltered_historical__mutmut_30,
        "xǁValueAtRiskǁfiltered_historical__mutmut_31": xǁValueAtRiskǁfiltered_historical__mutmut_31,
    }
    xǁValueAtRiskǁfiltered_historical__mutmut_orig.__name__ = "xǁValueAtRiskǁfiltered_historical"

    def monte_carlo(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        args = [n_sims, horizon, seed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁValueAtRiskǁmonte_carlo__mutmut_orig"),
            object.__getattribute__(self, "xǁValueAtRiskǁmonte_carlo__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁValueAtRiskǁmonte_carlo__mutmut_orig(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_1(
        self,
        n_sims: int = 10001,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_2(
        self,
        n_sims: int = 10000,
        horizon: int = 2,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_3(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = None

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_4(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(None)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_5(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = None
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_6(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(None, dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_7(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=None)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_8(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_9(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(
            getattr(self.results, "params", None),
        )
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_10(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(None, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_11(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, None, None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_12(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr("params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_13(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_14(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(self.results.params, dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_15(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "XXparamsXX", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_16(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "PARAMS", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_17(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = None
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_18(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] * 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_19(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[+1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_20(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-2] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_21(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 3
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_22(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = None

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_23(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] + self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_24(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[+1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_25(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-2] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_26(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = None
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_27(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[1]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_28(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = None
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_29(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(None)
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_30(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(None, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_31(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, None, 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_32(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", None))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_33(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr("p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_34(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_35(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(self.results.p)
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_36(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "XXpXX", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_37(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "P", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_38(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 2))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_39(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = None
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_40(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(None)
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_41(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(None, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_42(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, None, 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_43(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", None))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_44(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr("q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_45(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_46(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(self.results.q)
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_47(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "XXqXX", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_48(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "Q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_49(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 2))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_50(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = None
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_51(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[2 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_52(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 - q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_53(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 2 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_54(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = None

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_55(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 - q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_56(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[2 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_57(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q - p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_58(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 - q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_59(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 2 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_60(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = None

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_61(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(None)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_62(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(None):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_63(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = None

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_64(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(None)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_65(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(None):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_66(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = None
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_67(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 - betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_68(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega - alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_69(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] / last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_70(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[1] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_71(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid * 2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_72(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**3 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_73(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] / sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_74(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[1] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_75(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h >= 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_76(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 1:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_77(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = None
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_78(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) - np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_79(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(None) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_80(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(None)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_81(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = None
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_82(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega * (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_83(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 + persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_84(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (2 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_85(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence <= 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_86(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 2 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_87(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = None

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_88(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var - persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_89(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h / (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_90(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence * h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_91(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last + uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_92(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = None
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_93(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(None, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_94(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, None)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_95(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_96(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(
                    sigma2,
                )
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_97(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1.000000000001)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_98(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = None
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_99(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = None

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_100(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu - np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_101(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) / z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_102(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(None) * z

            var_series[h] = np.quantile(sim_returns, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_103(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = None

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_104(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(None, self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_105(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(sim_returns, None)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_106(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(self.alpha)

        return var_series

    def xǁValueAtRiskǁmonte_carlo__mutmut_107(
        self,
        n_sims: int = 10000,
        horizon: int = 1,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Compute VaR by Monte Carlo simulation.

        Parameters
        ----------
        n_sims : int
            Number of simulation paths. Default is 10000.
        horizon : int
            Forecast horizon in periods. Default is 1.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        NDArray[np.float64]
            VaR estimate(s). If horizon=1, returns scalar-like array.
            If horizon>1, returns array of shape (horizon,).

        Notes
        -----
        1. Use the last conditional variance as starting point.
        2. Simulate N paths of sigma^2_{T+h} and r_{T+h}.
        3. VaR_alpha = quantile(simulated returns ; alpha).
        """
        rng = np.random.default_rng(seed)

        # Extract GARCH parameters from results
        params = np.asarray(getattr(self.results, "params", None), dtype=np.float64)
        sigma2_last = self.conditional_volatility[-1] ** 2
        last_resid = self.returns[-1] - self.mu

        # Parse GARCH(p,q) parameters: [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        omega = params[0]
        # Determine p, q from model if available
        p = int(getattr(self.results, "p", 1))
        q = int(getattr(self.results, "q", 1))
        alphas = params[1 : 1 + q]
        betas = params[1 + q : 1 + q + p]

        var_series = np.empty(horizon)

        for h in range(horizon):
            # Simulate n_sims paths for this horizon step
            sim_returns = np.empty(n_sims)

            for i in range(n_sims):
                sigma2 = omega + alphas[0] * last_resid**2 + betas[0] * sigma2_last
                if h > 0:
                    # For multi-step, use unconditional expectation approximation
                    persistence = np.sum(alphas) + np.sum(betas)
                    uncond_var = omega / (1 - persistence) if persistence < 1 else sigma2_last
                    sigma2 = uncond_var + persistence**h * (sigma2_last - uncond_var)

                sigma2 = max(sigma2, 1e-12)
                z = rng.standard_normal()
                sim_returns[i] = self.mu + np.sqrt(sigma2) * z

            var_series[h] = np.quantile(
                sim_returns,
            )

        return var_series

    xǁValueAtRiskǁmonte_carlo__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁValueAtRiskǁmonte_carlo__mutmut_1": xǁValueAtRiskǁmonte_carlo__mutmut_1,
        "xǁValueAtRiskǁmonte_carlo__mutmut_2": xǁValueAtRiskǁmonte_carlo__mutmut_2,
        "xǁValueAtRiskǁmonte_carlo__mutmut_3": xǁValueAtRiskǁmonte_carlo__mutmut_3,
        "xǁValueAtRiskǁmonte_carlo__mutmut_4": xǁValueAtRiskǁmonte_carlo__mutmut_4,
        "xǁValueAtRiskǁmonte_carlo__mutmut_5": xǁValueAtRiskǁmonte_carlo__mutmut_5,
        "xǁValueAtRiskǁmonte_carlo__mutmut_6": xǁValueAtRiskǁmonte_carlo__mutmut_6,
        "xǁValueAtRiskǁmonte_carlo__mutmut_7": xǁValueAtRiskǁmonte_carlo__mutmut_7,
        "xǁValueAtRiskǁmonte_carlo__mutmut_8": xǁValueAtRiskǁmonte_carlo__mutmut_8,
        "xǁValueAtRiskǁmonte_carlo__mutmut_9": xǁValueAtRiskǁmonte_carlo__mutmut_9,
        "xǁValueAtRiskǁmonte_carlo__mutmut_10": xǁValueAtRiskǁmonte_carlo__mutmut_10,
        "xǁValueAtRiskǁmonte_carlo__mutmut_11": xǁValueAtRiskǁmonte_carlo__mutmut_11,
        "xǁValueAtRiskǁmonte_carlo__mutmut_12": xǁValueAtRiskǁmonte_carlo__mutmut_12,
        "xǁValueAtRiskǁmonte_carlo__mutmut_13": xǁValueAtRiskǁmonte_carlo__mutmut_13,
        "xǁValueAtRiskǁmonte_carlo__mutmut_14": xǁValueAtRiskǁmonte_carlo__mutmut_14,
        "xǁValueAtRiskǁmonte_carlo__mutmut_15": xǁValueAtRiskǁmonte_carlo__mutmut_15,
        "xǁValueAtRiskǁmonte_carlo__mutmut_16": xǁValueAtRiskǁmonte_carlo__mutmut_16,
        "xǁValueAtRiskǁmonte_carlo__mutmut_17": xǁValueAtRiskǁmonte_carlo__mutmut_17,
        "xǁValueAtRiskǁmonte_carlo__mutmut_18": xǁValueAtRiskǁmonte_carlo__mutmut_18,
        "xǁValueAtRiskǁmonte_carlo__mutmut_19": xǁValueAtRiskǁmonte_carlo__mutmut_19,
        "xǁValueAtRiskǁmonte_carlo__mutmut_20": xǁValueAtRiskǁmonte_carlo__mutmut_20,
        "xǁValueAtRiskǁmonte_carlo__mutmut_21": xǁValueAtRiskǁmonte_carlo__mutmut_21,
        "xǁValueAtRiskǁmonte_carlo__mutmut_22": xǁValueAtRiskǁmonte_carlo__mutmut_22,
        "xǁValueAtRiskǁmonte_carlo__mutmut_23": xǁValueAtRiskǁmonte_carlo__mutmut_23,
        "xǁValueAtRiskǁmonte_carlo__mutmut_24": xǁValueAtRiskǁmonte_carlo__mutmut_24,
        "xǁValueAtRiskǁmonte_carlo__mutmut_25": xǁValueAtRiskǁmonte_carlo__mutmut_25,
        "xǁValueAtRiskǁmonte_carlo__mutmut_26": xǁValueAtRiskǁmonte_carlo__mutmut_26,
        "xǁValueAtRiskǁmonte_carlo__mutmut_27": xǁValueAtRiskǁmonte_carlo__mutmut_27,
        "xǁValueAtRiskǁmonte_carlo__mutmut_28": xǁValueAtRiskǁmonte_carlo__mutmut_28,
        "xǁValueAtRiskǁmonte_carlo__mutmut_29": xǁValueAtRiskǁmonte_carlo__mutmut_29,
        "xǁValueAtRiskǁmonte_carlo__mutmut_30": xǁValueAtRiskǁmonte_carlo__mutmut_30,
        "xǁValueAtRiskǁmonte_carlo__mutmut_31": xǁValueAtRiskǁmonte_carlo__mutmut_31,
        "xǁValueAtRiskǁmonte_carlo__mutmut_32": xǁValueAtRiskǁmonte_carlo__mutmut_32,
        "xǁValueAtRiskǁmonte_carlo__mutmut_33": xǁValueAtRiskǁmonte_carlo__mutmut_33,
        "xǁValueAtRiskǁmonte_carlo__mutmut_34": xǁValueAtRiskǁmonte_carlo__mutmut_34,
        "xǁValueAtRiskǁmonte_carlo__mutmut_35": xǁValueAtRiskǁmonte_carlo__mutmut_35,
        "xǁValueAtRiskǁmonte_carlo__mutmut_36": xǁValueAtRiskǁmonte_carlo__mutmut_36,
        "xǁValueAtRiskǁmonte_carlo__mutmut_37": xǁValueAtRiskǁmonte_carlo__mutmut_37,
        "xǁValueAtRiskǁmonte_carlo__mutmut_38": xǁValueAtRiskǁmonte_carlo__mutmut_38,
        "xǁValueAtRiskǁmonte_carlo__mutmut_39": xǁValueAtRiskǁmonte_carlo__mutmut_39,
        "xǁValueAtRiskǁmonte_carlo__mutmut_40": xǁValueAtRiskǁmonte_carlo__mutmut_40,
        "xǁValueAtRiskǁmonte_carlo__mutmut_41": xǁValueAtRiskǁmonte_carlo__mutmut_41,
        "xǁValueAtRiskǁmonte_carlo__mutmut_42": xǁValueAtRiskǁmonte_carlo__mutmut_42,
        "xǁValueAtRiskǁmonte_carlo__mutmut_43": xǁValueAtRiskǁmonte_carlo__mutmut_43,
        "xǁValueAtRiskǁmonte_carlo__mutmut_44": xǁValueAtRiskǁmonte_carlo__mutmut_44,
        "xǁValueAtRiskǁmonte_carlo__mutmut_45": xǁValueAtRiskǁmonte_carlo__mutmut_45,
        "xǁValueAtRiskǁmonte_carlo__mutmut_46": xǁValueAtRiskǁmonte_carlo__mutmut_46,
        "xǁValueAtRiskǁmonte_carlo__mutmut_47": xǁValueAtRiskǁmonte_carlo__mutmut_47,
        "xǁValueAtRiskǁmonte_carlo__mutmut_48": xǁValueAtRiskǁmonte_carlo__mutmut_48,
        "xǁValueAtRiskǁmonte_carlo__mutmut_49": xǁValueAtRiskǁmonte_carlo__mutmut_49,
        "xǁValueAtRiskǁmonte_carlo__mutmut_50": xǁValueAtRiskǁmonte_carlo__mutmut_50,
        "xǁValueAtRiskǁmonte_carlo__mutmut_51": xǁValueAtRiskǁmonte_carlo__mutmut_51,
        "xǁValueAtRiskǁmonte_carlo__mutmut_52": xǁValueAtRiskǁmonte_carlo__mutmut_52,
        "xǁValueAtRiskǁmonte_carlo__mutmut_53": xǁValueAtRiskǁmonte_carlo__mutmut_53,
        "xǁValueAtRiskǁmonte_carlo__mutmut_54": xǁValueAtRiskǁmonte_carlo__mutmut_54,
        "xǁValueAtRiskǁmonte_carlo__mutmut_55": xǁValueAtRiskǁmonte_carlo__mutmut_55,
        "xǁValueAtRiskǁmonte_carlo__mutmut_56": xǁValueAtRiskǁmonte_carlo__mutmut_56,
        "xǁValueAtRiskǁmonte_carlo__mutmut_57": xǁValueAtRiskǁmonte_carlo__mutmut_57,
        "xǁValueAtRiskǁmonte_carlo__mutmut_58": xǁValueAtRiskǁmonte_carlo__mutmut_58,
        "xǁValueAtRiskǁmonte_carlo__mutmut_59": xǁValueAtRiskǁmonte_carlo__mutmut_59,
        "xǁValueAtRiskǁmonte_carlo__mutmut_60": xǁValueAtRiskǁmonte_carlo__mutmut_60,
        "xǁValueAtRiskǁmonte_carlo__mutmut_61": xǁValueAtRiskǁmonte_carlo__mutmut_61,
        "xǁValueAtRiskǁmonte_carlo__mutmut_62": xǁValueAtRiskǁmonte_carlo__mutmut_62,
        "xǁValueAtRiskǁmonte_carlo__mutmut_63": xǁValueAtRiskǁmonte_carlo__mutmut_63,
        "xǁValueAtRiskǁmonte_carlo__mutmut_64": xǁValueAtRiskǁmonte_carlo__mutmut_64,
        "xǁValueAtRiskǁmonte_carlo__mutmut_65": xǁValueAtRiskǁmonte_carlo__mutmut_65,
        "xǁValueAtRiskǁmonte_carlo__mutmut_66": xǁValueAtRiskǁmonte_carlo__mutmut_66,
        "xǁValueAtRiskǁmonte_carlo__mutmut_67": xǁValueAtRiskǁmonte_carlo__mutmut_67,
        "xǁValueAtRiskǁmonte_carlo__mutmut_68": xǁValueAtRiskǁmonte_carlo__mutmut_68,
        "xǁValueAtRiskǁmonte_carlo__mutmut_69": xǁValueAtRiskǁmonte_carlo__mutmut_69,
        "xǁValueAtRiskǁmonte_carlo__mutmut_70": xǁValueAtRiskǁmonte_carlo__mutmut_70,
        "xǁValueAtRiskǁmonte_carlo__mutmut_71": xǁValueAtRiskǁmonte_carlo__mutmut_71,
        "xǁValueAtRiskǁmonte_carlo__mutmut_72": xǁValueAtRiskǁmonte_carlo__mutmut_72,
        "xǁValueAtRiskǁmonte_carlo__mutmut_73": xǁValueAtRiskǁmonte_carlo__mutmut_73,
        "xǁValueAtRiskǁmonte_carlo__mutmut_74": xǁValueAtRiskǁmonte_carlo__mutmut_74,
        "xǁValueAtRiskǁmonte_carlo__mutmut_75": xǁValueAtRiskǁmonte_carlo__mutmut_75,
        "xǁValueAtRiskǁmonte_carlo__mutmut_76": xǁValueAtRiskǁmonte_carlo__mutmut_76,
        "xǁValueAtRiskǁmonte_carlo__mutmut_77": xǁValueAtRiskǁmonte_carlo__mutmut_77,
        "xǁValueAtRiskǁmonte_carlo__mutmut_78": xǁValueAtRiskǁmonte_carlo__mutmut_78,
        "xǁValueAtRiskǁmonte_carlo__mutmut_79": xǁValueAtRiskǁmonte_carlo__mutmut_79,
        "xǁValueAtRiskǁmonte_carlo__mutmut_80": xǁValueAtRiskǁmonte_carlo__mutmut_80,
        "xǁValueAtRiskǁmonte_carlo__mutmut_81": xǁValueAtRiskǁmonte_carlo__mutmut_81,
        "xǁValueAtRiskǁmonte_carlo__mutmut_82": xǁValueAtRiskǁmonte_carlo__mutmut_82,
        "xǁValueAtRiskǁmonte_carlo__mutmut_83": xǁValueAtRiskǁmonte_carlo__mutmut_83,
        "xǁValueAtRiskǁmonte_carlo__mutmut_84": xǁValueAtRiskǁmonte_carlo__mutmut_84,
        "xǁValueAtRiskǁmonte_carlo__mutmut_85": xǁValueAtRiskǁmonte_carlo__mutmut_85,
        "xǁValueAtRiskǁmonte_carlo__mutmut_86": xǁValueAtRiskǁmonte_carlo__mutmut_86,
        "xǁValueAtRiskǁmonte_carlo__mutmut_87": xǁValueAtRiskǁmonte_carlo__mutmut_87,
        "xǁValueAtRiskǁmonte_carlo__mutmut_88": xǁValueAtRiskǁmonte_carlo__mutmut_88,
        "xǁValueAtRiskǁmonte_carlo__mutmut_89": xǁValueAtRiskǁmonte_carlo__mutmut_89,
        "xǁValueAtRiskǁmonte_carlo__mutmut_90": xǁValueAtRiskǁmonte_carlo__mutmut_90,
        "xǁValueAtRiskǁmonte_carlo__mutmut_91": xǁValueAtRiskǁmonte_carlo__mutmut_91,
        "xǁValueAtRiskǁmonte_carlo__mutmut_92": xǁValueAtRiskǁmonte_carlo__mutmut_92,
        "xǁValueAtRiskǁmonte_carlo__mutmut_93": xǁValueAtRiskǁmonte_carlo__mutmut_93,
        "xǁValueAtRiskǁmonte_carlo__mutmut_94": xǁValueAtRiskǁmonte_carlo__mutmut_94,
        "xǁValueAtRiskǁmonte_carlo__mutmut_95": xǁValueAtRiskǁmonte_carlo__mutmut_95,
        "xǁValueAtRiskǁmonte_carlo__mutmut_96": xǁValueAtRiskǁmonte_carlo__mutmut_96,
        "xǁValueAtRiskǁmonte_carlo__mutmut_97": xǁValueAtRiskǁmonte_carlo__mutmut_97,
        "xǁValueAtRiskǁmonte_carlo__mutmut_98": xǁValueAtRiskǁmonte_carlo__mutmut_98,
        "xǁValueAtRiskǁmonte_carlo__mutmut_99": xǁValueAtRiskǁmonte_carlo__mutmut_99,
        "xǁValueAtRiskǁmonte_carlo__mutmut_100": xǁValueAtRiskǁmonte_carlo__mutmut_100,
        "xǁValueAtRiskǁmonte_carlo__mutmut_101": xǁValueAtRiskǁmonte_carlo__mutmut_101,
        "xǁValueAtRiskǁmonte_carlo__mutmut_102": xǁValueAtRiskǁmonte_carlo__mutmut_102,
        "xǁValueAtRiskǁmonte_carlo__mutmut_103": xǁValueAtRiskǁmonte_carlo__mutmut_103,
        "xǁValueAtRiskǁmonte_carlo__mutmut_104": xǁValueAtRiskǁmonte_carlo__mutmut_104,
        "xǁValueAtRiskǁmonte_carlo__mutmut_105": xǁValueAtRiskǁmonte_carlo__mutmut_105,
        "xǁValueAtRiskǁmonte_carlo__mutmut_106": xǁValueAtRiskǁmonte_carlo__mutmut_106,
        "xǁValueAtRiskǁmonte_carlo__mutmut_107": xǁValueAtRiskǁmonte_carlo__mutmut_107,
    }
    xǁValueAtRiskǁmonte_carlo__mutmut_orig.__name__ = "xǁValueAtRiskǁmonte_carlo"
