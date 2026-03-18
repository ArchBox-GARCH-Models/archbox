"""Diagnostic tests for GARCH models."""

from archbox.diagnostics.arch_lm import arch_lm_test
from archbox.diagnostics.diagnostics import DiagnosticReport, full_diagnostics
from archbox.diagnostics.engle_sheppard import engle_sheppard_test
from archbox.diagnostics.hong_spillover import hong_spillover_test
from archbox.diagnostics.ljung_box import ljung_box_squared
from archbox.diagnostics.nyblom import nyblom_test
from archbox.diagnostics.sign_bias import sign_bias_test

__all__ = [
    "arch_lm_test",
    "sign_bias_test",
    "ljung_box_squared",
    "nyblom_test",
    "engle_sheppard_test",
    "hong_spillover_test",
    "full_diagnostics",
    "DiagnosticReport",
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
