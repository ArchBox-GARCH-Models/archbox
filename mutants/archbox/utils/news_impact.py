"""News Impact Curve for asymmetric volatility models.

The news impact curve shows how past shocks eps_{t-1} affect the current
conditional variance sigma^2_t, holding all else constant.

References
----------
- Engle, R.F. & Ng, V.K. (1993). Measuring and Testing the Impact of News on Volatility.
  Journal of Finance, 48(5), 1749-1778.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

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


def news_impact_curve(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    args = [model, results, n_points, sigma_range]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_news_impact_curve__mutmut_orig, x_news_impact_curve__mutmut_mutants, args, kwargs, None
    )


def x_news_impact_curve__mutmut_orig(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_1(
    model: Any,
    results: Any,
    n_points: int = 101,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_2(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 4.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_3(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = None
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_4(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) * 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_5(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(None) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_6(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 3
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_7(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = None

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_8(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(None)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_9(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = None

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_10(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        None,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_11(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        None,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_12(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        None,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_13(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_14(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_15(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_16(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range / sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_17(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        +sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_18(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range / sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_19(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = None
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_20(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = None

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_21(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(None)

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_22(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(None, sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_23(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), None, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_24(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(eps), sigma2_ref, None) for eps in eps_range]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_25(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array([model._one_step_variance(sigma2_ref, params) for eps in eps_range])

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_26(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array([model._one_step_variance(float(eps), params) for eps in eps_range])

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_27(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [
            model._one_step_variance(
                float(eps),
                sigma2_ref,
            )
            for eps in eps_range
        ]
    )

    return eps_range, sigma2_response


def x_news_impact_curve__mutmut_28(
    model: Any,
    results: Any,
    n_points: int = 100,
    sigma_range: float = 3.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the news impact curve for a fitted volatility model.

    The news impact curve evaluates sigma^2_t as a function of eps_{t-1},
    holding sigma^2_{t-1} fixed at its average level.

    Parameters
    ----------
    model : VolatilityModel
        Fitted volatility model instance (must have _one_step_variance method).
    results : ArchResults
        Fitted model results.
    n_points : int
        Number of points in the shock grid. Default 100.
    sigma_range : float
        Range of shocks in multiples of unconditional sigma. Default 3.0.

    Returns
    -------
    tuple[ndarray, ndarray]
        (eps_range, sigma2_response) where:
        - eps_range: grid of eps_{t-1} values from -sigma_range*sigma to +sigma_range*sigma
        - sigma2_response: corresponding sigma^2_t for each eps value
    """
    # Use average conditional volatility as the reference level
    sigma2_ref = float(results.conditional_volatility.mean()) ** 2
    sigma_ref = np.sqrt(sigma2_ref)

    # Create grid of shocks
    eps_range = np.linspace(
        -sigma_range * sigma_ref,
        sigma_range * sigma_ref,
        n_points,
    )

    # Compute sigma^2_t for each shock value
    params = results.params
    sigma2_response = np.array(
        [model._one_step_variance(float(None), sigma2_ref, params) for eps in eps_range]
    )

    return eps_range, sigma2_response


x_news_impact_curve__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_news_impact_curve__mutmut_1": x_news_impact_curve__mutmut_1,
    "x_news_impact_curve__mutmut_2": x_news_impact_curve__mutmut_2,
    "x_news_impact_curve__mutmut_3": x_news_impact_curve__mutmut_3,
    "x_news_impact_curve__mutmut_4": x_news_impact_curve__mutmut_4,
    "x_news_impact_curve__mutmut_5": x_news_impact_curve__mutmut_5,
    "x_news_impact_curve__mutmut_6": x_news_impact_curve__mutmut_6,
    "x_news_impact_curve__mutmut_7": x_news_impact_curve__mutmut_7,
    "x_news_impact_curve__mutmut_8": x_news_impact_curve__mutmut_8,
    "x_news_impact_curve__mutmut_9": x_news_impact_curve__mutmut_9,
    "x_news_impact_curve__mutmut_10": x_news_impact_curve__mutmut_10,
    "x_news_impact_curve__mutmut_11": x_news_impact_curve__mutmut_11,
    "x_news_impact_curve__mutmut_12": x_news_impact_curve__mutmut_12,
    "x_news_impact_curve__mutmut_13": x_news_impact_curve__mutmut_13,
    "x_news_impact_curve__mutmut_14": x_news_impact_curve__mutmut_14,
    "x_news_impact_curve__mutmut_15": x_news_impact_curve__mutmut_15,
    "x_news_impact_curve__mutmut_16": x_news_impact_curve__mutmut_16,
    "x_news_impact_curve__mutmut_17": x_news_impact_curve__mutmut_17,
    "x_news_impact_curve__mutmut_18": x_news_impact_curve__mutmut_18,
    "x_news_impact_curve__mutmut_19": x_news_impact_curve__mutmut_19,
    "x_news_impact_curve__mutmut_20": x_news_impact_curve__mutmut_20,
    "x_news_impact_curve__mutmut_21": x_news_impact_curve__mutmut_21,
    "x_news_impact_curve__mutmut_22": x_news_impact_curve__mutmut_22,
    "x_news_impact_curve__mutmut_23": x_news_impact_curve__mutmut_23,
    "x_news_impact_curve__mutmut_24": x_news_impact_curve__mutmut_24,
    "x_news_impact_curve__mutmut_25": x_news_impact_curve__mutmut_25,
    "x_news_impact_curve__mutmut_26": x_news_impact_curve__mutmut_26,
    "x_news_impact_curve__mutmut_27": x_news_impact_curve__mutmut_27,
    "x_news_impact_curve__mutmut_28": x_news_impact_curve__mutmut_28,
}
x_news_impact_curve__mutmut_orig.__name__ = "x_news_impact_curve"


def plot_news_impact(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    args = [eps_range, sigma2_response, model_name, ax]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_plot_news_impact__mutmut_orig, x_plot_news_impact__mutmut_mutants, args, kwargs, None
    )


def x_plot_news_impact__mutmut_orig(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_1(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "XXModelXX",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_2(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_3(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "MODEL",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_4(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is not None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_5(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """

    if ax is None:
        _, ax = None

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_6(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=None)

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_7(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_8(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 6))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_9(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(None, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_10(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, None, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_11(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=None, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_12(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=None)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_13(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_14(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_15(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_16(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        eps_range,
        sigma2_response,
        linewidth=2,
    )
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_17(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=3, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_18(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=None, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_19(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color=None, linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_20(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle=None, alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_21(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=None)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_22(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_23(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_24(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_25(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(
        x=0,
        color="gray",
        linestyle="--",
    )
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_26(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=1, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_27(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="XXgrayXX", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_28(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="GRAY", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_29(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="XX--XX", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_30(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=1.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_31(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(None)
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_32(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"XX$\varepsilon_{t-1}$XX")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_33(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\vAREPSILON_{T-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_34(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(None)
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_35(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"XX$\sigma^2_t$XX")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_36(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sIGMA^2_T$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_37(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(None)
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_38(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(None, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_39(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=None)

    return ax


def x_plot_news_impact__mutmut_40(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_41(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(
        True,
    )

    return ax


def x_plot_news_impact__mutmut_42(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(False, alpha=0.3)

    return ax


def x_plot_news_impact__mutmut_43(
    eps_range: NDArray[np.float64],
    sigma2_response: NDArray[np.float64],
    model_name: str = "Model",
    ax: Any = None,
) -> Any:
    """Plot the news impact curve.

    Parameters
    ----------
    eps_range : ndarray
        Grid of shock values.
    sigma2_response : ndarray
        Corresponding variance responses.
    model_name : str
        Name of the model for the plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. If None, creates a new figure.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.plot(eps_range, sigma2_response, linewidth=2, label=model_name)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(f"News Impact Curve: {model_name}")
    ax.legend()
    ax.grid(True, alpha=1.3)

    return ax


x_plot_news_impact__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_plot_news_impact__mutmut_1": x_plot_news_impact__mutmut_1,
    "x_plot_news_impact__mutmut_2": x_plot_news_impact__mutmut_2,
    "x_plot_news_impact__mutmut_3": x_plot_news_impact__mutmut_3,
    "x_plot_news_impact__mutmut_4": x_plot_news_impact__mutmut_4,
    "x_plot_news_impact__mutmut_5": x_plot_news_impact__mutmut_5,
    "x_plot_news_impact__mutmut_6": x_plot_news_impact__mutmut_6,
    "x_plot_news_impact__mutmut_7": x_plot_news_impact__mutmut_7,
    "x_plot_news_impact__mutmut_8": x_plot_news_impact__mutmut_8,
    "x_plot_news_impact__mutmut_9": x_plot_news_impact__mutmut_9,
    "x_plot_news_impact__mutmut_10": x_plot_news_impact__mutmut_10,
    "x_plot_news_impact__mutmut_11": x_plot_news_impact__mutmut_11,
    "x_plot_news_impact__mutmut_12": x_plot_news_impact__mutmut_12,
    "x_plot_news_impact__mutmut_13": x_plot_news_impact__mutmut_13,
    "x_plot_news_impact__mutmut_14": x_plot_news_impact__mutmut_14,
    "x_plot_news_impact__mutmut_15": x_plot_news_impact__mutmut_15,
    "x_plot_news_impact__mutmut_16": x_plot_news_impact__mutmut_16,
    "x_plot_news_impact__mutmut_17": x_plot_news_impact__mutmut_17,
    "x_plot_news_impact__mutmut_18": x_plot_news_impact__mutmut_18,
    "x_plot_news_impact__mutmut_19": x_plot_news_impact__mutmut_19,
    "x_plot_news_impact__mutmut_20": x_plot_news_impact__mutmut_20,
    "x_plot_news_impact__mutmut_21": x_plot_news_impact__mutmut_21,
    "x_plot_news_impact__mutmut_22": x_plot_news_impact__mutmut_22,
    "x_plot_news_impact__mutmut_23": x_plot_news_impact__mutmut_23,
    "x_plot_news_impact__mutmut_24": x_plot_news_impact__mutmut_24,
    "x_plot_news_impact__mutmut_25": x_plot_news_impact__mutmut_25,
    "x_plot_news_impact__mutmut_26": x_plot_news_impact__mutmut_26,
    "x_plot_news_impact__mutmut_27": x_plot_news_impact__mutmut_27,
    "x_plot_news_impact__mutmut_28": x_plot_news_impact__mutmut_28,
    "x_plot_news_impact__mutmut_29": x_plot_news_impact__mutmut_29,
    "x_plot_news_impact__mutmut_30": x_plot_news_impact__mutmut_30,
    "x_plot_news_impact__mutmut_31": x_plot_news_impact__mutmut_31,
    "x_plot_news_impact__mutmut_32": x_plot_news_impact__mutmut_32,
    "x_plot_news_impact__mutmut_33": x_plot_news_impact__mutmut_33,
    "x_plot_news_impact__mutmut_34": x_plot_news_impact__mutmut_34,
    "x_plot_news_impact__mutmut_35": x_plot_news_impact__mutmut_35,
    "x_plot_news_impact__mutmut_36": x_plot_news_impact__mutmut_36,
    "x_plot_news_impact__mutmut_37": x_plot_news_impact__mutmut_37,
    "x_plot_news_impact__mutmut_38": x_plot_news_impact__mutmut_38,
    "x_plot_news_impact__mutmut_39": x_plot_news_impact__mutmut_39,
    "x_plot_news_impact__mutmut_40": x_plot_news_impact__mutmut_40,
    "x_plot_news_impact__mutmut_41": x_plot_news_impact__mutmut_41,
    "x_plot_news_impact__mutmut_42": x_plot_news_impact__mutmut_42,
    "x_plot_news_impact__mutmut_43": x_plot_news_impact__mutmut_43,
}
x_plot_news_impact__mutmut_orig.__name__ = "x_plot_news_impact"


def compare_news_impact(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    args = [models_results, n_points, sigma_range, ax]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_compare_news_impact__mutmut_orig,
        x_compare_news_impact__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_compare_news_impact__mutmut_orig(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_1(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 101,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_2(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 4.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_3(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is not None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_4(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """

    if ax is None:
        _, ax = None

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_5(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=None)

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_6(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(11, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_7(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 7))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_8(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = None
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_9(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            None, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_10(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, None, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_11(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=None, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_12(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=None
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_13(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_14(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_15(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(model, results, sigma_range=sigma_range)
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_16(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model,
            results,
            n_points=n_points,
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_17(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(None, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_18(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, None, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_19(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=None, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_20(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=None)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_21(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_22(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_23(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_24(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(
            eps_range,
            sigma2_response,
            linewidth=2,
        )

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_25(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=3, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_26(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=None, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_27(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color=None, linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_28(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle=None, alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_29(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=None)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_30(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_31(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_32(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_33(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(
        x=0,
        color="gray",
        linestyle="--",
    )
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_34(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=1, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_35(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="XXgrayXX", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_36(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="GRAY", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_37(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="XX--XX", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_38(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=1.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_39(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(None)
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_40(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"XX$\varepsilon_{t-1}$XX")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_41(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\vAREPSILON_{T-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_42(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(None)
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_43(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"XX$\sigma^2_t$XX")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_44(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sIGMA^2_T$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_45(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title(None)
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_46(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("XXNews Impact Curves ComparisonXX")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_47(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("news impact curves comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_48(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("NEWS IMPACT CURVES COMPARISON")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_49(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(None, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_50(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=None)

    return ax


def x_compare_news_impact__mutmut_51(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_52(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(
        True,
    )

    return ax


def x_compare_news_impact__mutmut_53(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(False, alpha=0.3)

    return ax


def x_compare_news_impact__mutmut_54(
    models_results: list[tuple[Any, Any, str]],
    n_points: int = 100,
    sigma_range: float = 3.0,
    ax: Any = None,
) -> Any:
    """Compare news impact curves for multiple models.

    Parameters
    ----------
    models_results : list of (model, results, name) tuples
        List of fitted models to compare.
    n_points : int
        Number of points in the shock grid.
    sigma_range : float
        Range of shocks in multiples of sigma.
    ax : matplotlib Axes, optional
        Axes to plot on.

    Returns
    -------
    matplotlib Axes
        The plot axes.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    for model, results, name in models_results:
        eps_range, sigma2_response = news_impact_curve(
            model, results, n_points=n_points, sigma_range=sigma_range
        )
        ax.plot(eps_range, sigma2_response, linewidth=2, label=name)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$\varepsilon_{t-1}$")
    ax.set_ylabel(r"$\sigma^2_t$")
    ax.set_title("News Impact Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=1.3)

    return ax


x_compare_news_impact__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_compare_news_impact__mutmut_1": x_compare_news_impact__mutmut_1,
    "x_compare_news_impact__mutmut_2": x_compare_news_impact__mutmut_2,
    "x_compare_news_impact__mutmut_3": x_compare_news_impact__mutmut_3,
    "x_compare_news_impact__mutmut_4": x_compare_news_impact__mutmut_4,
    "x_compare_news_impact__mutmut_5": x_compare_news_impact__mutmut_5,
    "x_compare_news_impact__mutmut_6": x_compare_news_impact__mutmut_6,
    "x_compare_news_impact__mutmut_7": x_compare_news_impact__mutmut_7,
    "x_compare_news_impact__mutmut_8": x_compare_news_impact__mutmut_8,
    "x_compare_news_impact__mutmut_9": x_compare_news_impact__mutmut_9,
    "x_compare_news_impact__mutmut_10": x_compare_news_impact__mutmut_10,
    "x_compare_news_impact__mutmut_11": x_compare_news_impact__mutmut_11,
    "x_compare_news_impact__mutmut_12": x_compare_news_impact__mutmut_12,
    "x_compare_news_impact__mutmut_13": x_compare_news_impact__mutmut_13,
    "x_compare_news_impact__mutmut_14": x_compare_news_impact__mutmut_14,
    "x_compare_news_impact__mutmut_15": x_compare_news_impact__mutmut_15,
    "x_compare_news_impact__mutmut_16": x_compare_news_impact__mutmut_16,
    "x_compare_news_impact__mutmut_17": x_compare_news_impact__mutmut_17,
    "x_compare_news_impact__mutmut_18": x_compare_news_impact__mutmut_18,
    "x_compare_news_impact__mutmut_19": x_compare_news_impact__mutmut_19,
    "x_compare_news_impact__mutmut_20": x_compare_news_impact__mutmut_20,
    "x_compare_news_impact__mutmut_21": x_compare_news_impact__mutmut_21,
    "x_compare_news_impact__mutmut_22": x_compare_news_impact__mutmut_22,
    "x_compare_news_impact__mutmut_23": x_compare_news_impact__mutmut_23,
    "x_compare_news_impact__mutmut_24": x_compare_news_impact__mutmut_24,
    "x_compare_news_impact__mutmut_25": x_compare_news_impact__mutmut_25,
    "x_compare_news_impact__mutmut_26": x_compare_news_impact__mutmut_26,
    "x_compare_news_impact__mutmut_27": x_compare_news_impact__mutmut_27,
    "x_compare_news_impact__mutmut_28": x_compare_news_impact__mutmut_28,
    "x_compare_news_impact__mutmut_29": x_compare_news_impact__mutmut_29,
    "x_compare_news_impact__mutmut_30": x_compare_news_impact__mutmut_30,
    "x_compare_news_impact__mutmut_31": x_compare_news_impact__mutmut_31,
    "x_compare_news_impact__mutmut_32": x_compare_news_impact__mutmut_32,
    "x_compare_news_impact__mutmut_33": x_compare_news_impact__mutmut_33,
    "x_compare_news_impact__mutmut_34": x_compare_news_impact__mutmut_34,
    "x_compare_news_impact__mutmut_35": x_compare_news_impact__mutmut_35,
    "x_compare_news_impact__mutmut_36": x_compare_news_impact__mutmut_36,
    "x_compare_news_impact__mutmut_37": x_compare_news_impact__mutmut_37,
    "x_compare_news_impact__mutmut_38": x_compare_news_impact__mutmut_38,
    "x_compare_news_impact__mutmut_39": x_compare_news_impact__mutmut_39,
    "x_compare_news_impact__mutmut_40": x_compare_news_impact__mutmut_40,
    "x_compare_news_impact__mutmut_41": x_compare_news_impact__mutmut_41,
    "x_compare_news_impact__mutmut_42": x_compare_news_impact__mutmut_42,
    "x_compare_news_impact__mutmut_43": x_compare_news_impact__mutmut_43,
    "x_compare_news_impact__mutmut_44": x_compare_news_impact__mutmut_44,
    "x_compare_news_impact__mutmut_45": x_compare_news_impact__mutmut_45,
    "x_compare_news_impact__mutmut_46": x_compare_news_impact__mutmut_46,
    "x_compare_news_impact__mutmut_47": x_compare_news_impact__mutmut_47,
    "x_compare_news_impact__mutmut_48": x_compare_news_impact__mutmut_48,
    "x_compare_news_impact__mutmut_49": x_compare_news_impact__mutmut_49,
    "x_compare_news_impact__mutmut_50": x_compare_news_impact__mutmut_50,
    "x_compare_news_impact__mutmut_51": x_compare_news_impact__mutmut_51,
    "x_compare_news_impact__mutmut_52": x_compare_news_impact__mutmut_52,
    "x_compare_news_impact__mutmut_53": x_compare_news_impact__mutmut_53,
    "x_compare_news_impact__mutmut_54": x_compare_news_impact__mutmut_54,
}
x_compare_news_impact__mutmut_orig.__name__ = "x_compare_news_impact"
