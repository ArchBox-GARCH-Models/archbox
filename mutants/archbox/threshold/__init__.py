"""Threshold and Smooth Transition Autoregressive models.

Models:
- TAR: Threshold Autoregressive (Tong, 1978)
- SETAR: Self-Exciting TAR (Tong & Lim, 1980)
- LSTAR: Logistic Smooth Transition AR (Terasvirta, 1994)
- ESTAR: Exponential Smooth Transition AR (Terasvirta, 1994)

Linearity Tests:
- Luukkonen-Saikkonen-Terasvirta (1988) LM test
- Terasvirta (1994) transition type test
- Tsay (1989) test for TAR
- Hansen (1996) bootstrap threshold test
"""

from archbox.threshold.base import ThresholdModel
from archbox.threshold.estar import ESTAR
from archbox.threshold.lstar import LSTAR
from archbox.threshold.results import TestResult, ThresholdResults
from archbox.threshold.setar import SETAR
from archbox.threshold.tar import TAR
from archbox.threshold.tests_linearity import (
    hansen_threshold_test,
    linearity_test,
    transition_type_test,
    tsay_test,
)
from archbox.threshold.transition import (
    exponential_transition,
    logistic_transition,
    logistic_transition_order2,
    plot_transition,
)

__all__ = [
    "ThresholdModel",
    "ThresholdResults",
    "TestResult",
    "TAR",
    "SETAR",
    "LSTAR",
    "ESTAR",
    "logistic_transition",
    "exponential_transition",
    "logistic_transition_order2",
    "plot_transition",
    "linearity_test",
    "transition_type_test",
    "tsay_test",
    "hansen_threshold_test",
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
