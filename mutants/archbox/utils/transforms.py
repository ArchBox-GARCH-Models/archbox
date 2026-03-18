"""Parameter transformations for constrained optimization.

Transformacoes garantem que os parametros do GARCH satisfacam:
- omega > 0
- alpha_i >= 0
- beta_j >= 0
- sum(alpha_i) + sum(beta_j) < 1 (estacionariedade)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, ClassVar

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


def positive_transform(x: NDArray[np.float64]) -> NDArray[np.float64]:
    args = [x]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_positive_transform__mutmut_orig, x_positive_transform__mutmut_mutants, args, kwargs, None
    )


def x_positive_transform__mutmut_orig(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> positive via exp."""
    return np.exp(x)


def x_positive_transform__mutmut_1(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> positive via exp."""
    return np.exp(None)


x_positive_transform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_positive_transform__mutmut_1": x_positive_transform__mutmut_1
}
x_positive_transform__mutmut_orig.__name__ = "x_positive_transform"


def positive_untransform(y: NDArray[np.float64]) -> NDArray[np.float64]:
    args = [y]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_positive_untransform__mutmut_orig,
        x_positive_untransform__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_positive_untransform__mutmut_orig(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform positive -> unconstrained via log."""
    return np.log(y)


def x_positive_untransform__mutmut_1(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform positive -> unconstrained via log."""
    return np.log(None)


x_positive_untransform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_positive_untransform__mutmut_1": x_positive_untransform__mutmut_1
}
x_positive_untransform__mutmut_orig.__name__ = "x_positive_untransform"


def unit_transform(x: NDArray[np.float64]) -> NDArray[np.float64]:
    args = [x]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_unit_transform__mutmut_orig, x_unit_transform__mutmut_mutants, args, kwargs, None
    )


def x_unit_transform__mutmut_orig(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 1.0 / (1.0 + np.exp(-x))


def x_unit_transform__mutmut_1(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 1.0 * (1.0 + np.exp(-x))


def x_unit_transform__mutmut_2(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 2.0 / (1.0 + np.exp(-x))


def x_unit_transform__mutmut_3(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 1.0 / (1.0 - np.exp(-x))


def x_unit_transform__mutmut_4(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 1.0 / (2.0 + np.exp(-x))


def x_unit_transform__mutmut_5(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 1.0 / (1.0 + np.exp(None))


def x_unit_transform__mutmut_6(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 1.0 / (1.0 + np.exp(+x))


x_unit_transform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_unit_transform__mutmut_1": x_unit_transform__mutmut_1,
    "x_unit_transform__mutmut_2": x_unit_transform__mutmut_2,
    "x_unit_transform__mutmut_3": x_unit_transform__mutmut_3,
    "x_unit_transform__mutmut_4": x_unit_transform__mutmut_4,
    "x_unit_transform__mutmut_5": x_unit_transform__mutmut_5,
    "x_unit_transform__mutmut_6": x_unit_transform__mutmut_6,
}
x_unit_transform__mutmut_orig.__name__ = "x_unit_transform"


def unit_untransform(y: NDArray[np.float64]) -> NDArray[np.float64]:
    args = [y]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_unit_untransform__mutmut_orig, x_unit_untransform__mutmut_mutants, args, kwargs, None
    )


def x_unit_untransform__mutmut_orig(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform (0, 1) -> unconstrained via logit."""
    return np.log(y / (1.0 - y))


def x_unit_untransform__mutmut_1(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform (0, 1) -> unconstrained via logit."""
    return np.log(None)


def x_unit_untransform__mutmut_2(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform (0, 1) -> unconstrained via logit."""
    return np.log(y * (1.0 - y))


def x_unit_untransform__mutmut_3(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform (0, 1) -> unconstrained via logit."""
    return np.log(y / (1.0 + y))


def x_unit_untransform__mutmut_4(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform (0, 1) -> unconstrained via logit."""
    return np.log(y / (2.0 - y))


x_unit_untransform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_unit_untransform__mutmut_1": x_unit_untransform__mutmut_1,
    "x_unit_untransform__mutmut_2": x_unit_untransform__mutmut_2,
    "x_unit_untransform__mutmut_3": x_unit_untransform__mutmut_3,
    "x_unit_untransform__mutmut_4": x_unit_untransform__mutmut_4,
}
x_unit_untransform__mutmut_orig.__name__ = "x_unit_untransform"


def stationarity_transform(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    args = [alphas, betas]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_stationarity_transform__mutmut_orig,
        x_stationarity_transform__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_stationarity_transform__mutmut_orig(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_1(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = None
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_2(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate(None)
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_3(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = None
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_4(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 * (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_5(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 2.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_6(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 - np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_7(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (2.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_8(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(None))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_9(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(+raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_10(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = None
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_11(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(None)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_12(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total > 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_13(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 1.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_14(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = None
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_15(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 * total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_16(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 1.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_17(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = None
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_18(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual / scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]


def x_stationarity_transform__mutmut_19(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = None
    return individual[:n_alpha], individual[n_alpha:]


x_stationarity_transform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_stationarity_transform__mutmut_1": x_stationarity_transform__mutmut_1,
    "x_stationarity_transform__mutmut_2": x_stationarity_transform__mutmut_2,
    "x_stationarity_transform__mutmut_3": x_stationarity_transform__mutmut_3,
    "x_stationarity_transform__mutmut_4": x_stationarity_transform__mutmut_4,
    "x_stationarity_transform__mutmut_5": x_stationarity_transform__mutmut_5,
    "x_stationarity_transform__mutmut_6": x_stationarity_transform__mutmut_6,
    "x_stationarity_transform__mutmut_7": x_stationarity_transform__mutmut_7,
    "x_stationarity_transform__mutmut_8": x_stationarity_transform__mutmut_8,
    "x_stationarity_transform__mutmut_9": x_stationarity_transform__mutmut_9,
    "x_stationarity_transform__mutmut_10": x_stationarity_transform__mutmut_10,
    "x_stationarity_transform__mutmut_11": x_stationarity_transform__mutmut_11,
    "x_stationarity_transform__mutmut_12": x_stationarity_transform__mutmut_12,
    "x_stationarity_transform__mutmut_13": x_stationarity_transform__mutmut_13,
    "x_stationarity_transform__mutmut_14": x_stationarity_transform__mutmut_14,
    "x_stationarity_transform__mutmut_15": x_stationarity_transform__mutmut_15,
    "x_stationarity_transform__mutmut_16": x_stationarity_transform__mutmut_16,
    "x_stationarity_transform__mutmut_17": x_stationarity_transform__mutmut_17,
    "x_stationarity_transform__mutmut_18": x_stationarity_transform__mutmut_18,
    "x_stationarity_transform__mutmut_19": x_stationarity_transform__mutmut_19,
}
x_stationarity_transform__mutmut_orig.__name__ = "x_stationarity_transform"
