"""Multivariate GARCH model implementations.

Available models:
- CCC: Constant Conditional Correlation (Bollerslev, 1990)
- DCC: Dynamic Conditional Correlation (Engle, 2002)
- BEKK: Baba-Engle-Kraft-Kroner (Engle & Kroner, 1995)
- GOGARCH: Generalized Orthogonal GARCH (van der Weide, 2002)
- DECO: Dynamic Equicorrelation (Engle & Kelly, 2012)
"""

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults
from archbox.multivariate.bekk import BEKK
from archbox.multivariate.ccc import CCC
from archbox.multivariate.dcc import DCC
from archbox.multivariate.deco import DECO
from archbox.multivariate.gogarch import GOGARCH
from archbox.multivariate.portfolio import (
    marginal_risk_contribution,
    minimum_variance_weights,
    minimum_variance_weights_dynamic,
    portfolio_variance,
    portfolio_volatility,
    risk_contribution,
    risk_decomposition,
)

__all__ = [
    # Base
    "MultivariateVolatilityModel",
    "MultivarResults",
    # Models
    "BEKK",
    "CCC",
    "DCC",
    "DECO",
    "GOGARCH",
    # Portfolio utilities
    "marginal_risk_contribution",
    "minimum_variance_weights",
    "minimum_variance_weights_dynamic",
    "portfolio_variance",
    "portfolio_volatility",
    "risk_contribution",
    "risk_decomposition",
]
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
