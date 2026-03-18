"""Results container for Markov-Switching models."""

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


class RegimeResults:
    """Container for Markov-Switching model results.

    Attributes
    ----------
    params : NDArray[np.float64]
        All estimated parameters, shape (n_params,).
    regime_params : dict[int, dict[str, float]]
        Parameters organized by regime.
    transition_matrix : NDArray[np.float64]
        Transition matrix P, shape (k, k). p_{ij} = P(S_t=j | S_{t-1}=i).
    filtered_probs : NDArray[np.float64]
        Filtered probabilities P(S_t=j | Y_t), shape (T, k).
    smoothed_probs : NDArray[np.float64]
        Smoothed probabilities P(S_t=j | Y_T), shape (T, k).
    predicted_probs : NDArray[np.float64]
        Predicted probabilities P(S_t=j | Y_{t-1}), shape (T, k).
    loglike : float
        Total log-likelihood.
    aic : float
        Akaike Information Criterion.
    bic : float
        Bayesian Information Criterion.
    nobs : int
        Number of observations.
    k_regimes : int
        Number of regimes.
    n_params : int
        Number of estimated parameters.
    model_name : str
        Name of the fitted model.
    param_names : list[str]
        Names of all parameters.
    converged : bool
        Whether estimation converged.
    n_iter : int
        Number of iterations to convergence.
    """

    def __init__(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        args = [
            params,
            regime_params,
            transition_matrix,
            filtered_probs,
            smoothed_probs,
            predicted_probs,
            loglike,
            nobs,
            k_regimes,
            model_name,
            param_names,
            converged,
            n_iter,
        ]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeResultsǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeResultsǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeResultsǁ__init____mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_1(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "XXMarkovSwitchingXX",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_2(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "markovswitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_3(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MARKOVSWITCHING",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_4(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = False,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_5(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 1,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_6(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = None
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_7(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = None
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_8(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = None
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_9(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = None
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_10(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = None
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_11(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = None
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_12(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = None
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_13(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = None
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_14(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = None
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_15(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = None
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_16(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = None
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_17(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = None
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_18(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names and [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_19(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(None)]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_20(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = None
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_21(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = None

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_22(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = None
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_23(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike - 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_24(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 / loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_25(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = +2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_26(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -3.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_27(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 / self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_28(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 3.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_29(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = None

    def xǁRegimeResultsǁ__init____mutmut_30(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike - np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_31(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 / loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_32(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = +2.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_33(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -3.0 * loglike + np.log(nobs) * self.n_params

    def xǁRegimeResultsǁ__init____mutmut_34(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(nobs) / self.n_params

    def xǁRegimeResultsǁ__init____mutmut_35(
        self,
        params: NDArray[np.float64],
        regime_params: dict[int, dict[str, Any]],
        transition_matrix: NDArray[np.float64],
        filtered_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        loglike: float,
        nobs: int,
        k_regimes: int,
        model_name: str = "MarkovSwitching",
        param_names: list[str] | None = None,
        converged: bool = True,
        n_iter: int = 0,
    ) -> None:
        """Initialize regime switching results container."""
        self.params = params
        self.regime_params = regime_params
        self.transition_matrix = transition_matrix
        self.filtered_probs = filtered_probs
        self.smoothed_probs = smoothed_probs
        self.predicted_probs = predicted_probs
        self.loglike = loglike
        self.nobs = nobs
        self.k_regimes = k_regimes
        self.n_params = len(params)
        self.model_name = model_name
        self.param_names = param_names or [f"param_{i}" for i in range(len(params))]
        self.converged = converged
        self.n_iter = n_iter

        # Information criteria
        self.aic = -2.0 * loglike + 2.0 * self.n_params
        self.bic = -2.0 * loglike + np.log(None) * self.n_params

    xǁRegimeResultsǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeResultsǁ__init____mutmut_1": xǁRegimeResultsǁ__init____mutmut_1,
        "xǁRegimeResultsǁ__init____mutmut_2": xǁRegimeResultsǁ__init____mutmut_2,
        "xǁRegimeResultsǁ__init____mutmut_3": xǁRegimeResultsǁ__init____mutmut_3,
        "xǁRegimeResultsǁ__init____mutmut_4": xǁRegimeResultsǁ__init____mutmut_4,
        "xǁRegimeResultsǁ__init____mutmut_5": xǁRegimeResultsǁ__init____mutmut_5,
        "xǁRegimeResultsǁ__init____mutmut_6": xǁRegimeResultsǁ__init____mutmut_6,
        "xǁRegimeResultsǁ__init____mutmut_7": xǁRegimeResultsǁ__init____mutmut_7,
        "xǁRegimeResultsǁ__init____mutmut_8": xǁRegimeResultsǁ__init____mutmut_8,
        "xǁRegimeResultsǁ__init____mutmut_9": xǁRegimeResultsǁ__init____mutmut_9,
        "xǁRegimeResultsǁ__init____mutmut_10": xǁRegimeResultsǁ__init____mutmut_10,
        "xǁRegimeResultsǁ__init____mutmut_11": xǁRegimeResultsǁ__init____mutmut_11,
        "xǁRegimeResultsǁ__init____mutmut_12": xǁRegimeResultsǁ__init____mutmut_12,
        "xǁRegimeResultsǁ__init____mutmut_13": xǁRegimeResultsǁ__init____mutmut_13,
        "xǁRegimeResultsǁ__init____mutmut_14": xǁRegimeResultsǁ__init____mutmut_14,
        "xǁRegimeResultsǁ__init____mutmut_15": xǁRegimeResultsǁ__init____mutmut_15,
        "xǁRegimeResultsǁ__init____mutmut_16": xǁRegimeResultsǁ__init____mutmut_16,
        "xǁRegimeResultsǁ__init____mutmut_17": xǁRegimeResultsǁ__init____mutmut_17,
        "xǁRegimeResultsǁ__init____mutmut_18": xǁRegimeResultsǁ__init____mutmut_18,
        "xǁRegimeResultsǁ__init____mutmut_19": xǁRegimeResultsǁ__init____mutmut_19,
        "xǁRegimeResultsǁ__init____mutmut_20": xǁRegimeResultsǁ__init____mutmut_20,
        "xǁRegimeResultsǁ__init____mutmut_21": xǁRegimeResultsǁ__init____mutmut_21,
        "xǁRegimeResultsǁ__init____mutmut_22": xǁRegimeResultsǁ__init____mutmut_22,
        "xǁRegimeResultsǁ__init____mutmut_23": xǁRegimeResultsǁ__init____mutmut_23,
        "xǁRegimeResultsǁ__init____mutmut_24": xǁRegimeResultsǁ__init____mutmut_24,
        "xǁRegimeResultsǁ__init____mutmut_25": xǁRegimeResultsǁ__init____mutmut_25,
        "xǁRegimeResultsǁ__init____mutmut_26": xǁRegimeResultsǁ__init____mutmut_26,
        "xǁRegimeResultsǁ__init____mutmut_27": xǁRegimeResultsǁ__init____mutmut_27,
        "xǁRegimeResultsǁ__init____mutmut_28": xǁRegimeResultsǁ__init____mutmut_28,
        "xǁRegimeResultsǁ__init____mutmut_29": xǁRegimeResultsǁ__init____mutmut_29,
        "xǁRegimeResultsǁ__init____mutmut_30": xǁRegimeResultsǁ__init____mutmut_30,
        "xǁRegimeResultsǁ__init____mutmut_31": xǁRegimeResultsǁ__init____mutmut_31,
        "xǁRegimeResultsǁ__init____mutmut_32": xǁRegimeResultsǁ__init____mutmut_32,
        "xǁRegimeResultsǁ__init____mutmut_33": xǁRegimeResultsǁ__init____mutmut_33,
        "xǁRegimeResultsǁ__init____mutmut_34": xǁRegimeResultsǁ__init____mutmut_34,
        "xǁRegimeResultsǁ__init____mutmut_35": xǁRegimeResultsǁ__init____mutmut_35,
    }
    xǁRegimeResultsǁ__init____mutmut_orig.__name__ = "xǁRegimeResultsǁ__init__"

    def summary(self) -> str:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeResultsǁsummary__mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeResultsǁsummary__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeResultsǁsummary__mutmut_orig(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_1(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = None
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_2(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = None
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_3(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" / 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_4(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "XX=XX" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_5(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 66
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_6(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(None)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_7(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(None)
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_8(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(None)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_9(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(None)
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_10(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(None)
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_11(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(None)
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_12(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(None)
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_13(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(None)
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_14(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(None)
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_15(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(None)
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_16(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(None)
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_17(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(None)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_18(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append(None)
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_19(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("XX\n  Regime Parameters:XX")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_20(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  regime parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_21(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  REGIME PARAMETERS:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_22(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append(None)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_23(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" / 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_24(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("XX-XX" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_25(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 66)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_26(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(None)
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_27(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(None)
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_28(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append(None)

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_29(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("XXXX")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_30(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append(None)
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_31(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("XX  Transition Matrix P:XX")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_32(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  transition matrix p:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_33(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  TRANSITION MATRIX P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_34(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append(None)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_35(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" / 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_36(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("XX-XX" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_37(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 66)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_38(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = None
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_39(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " - "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_40(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "XX       XX" + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_41(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(None)
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_42(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "XX  XX".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_43(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(None))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_44(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(None)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_45(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(None):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_46(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = None
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_47(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " - "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_48(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(None)
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_49(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "XX  XX".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_50(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(None)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_51(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(None)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_52(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append(None)

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_53(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("XXXX")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_54(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = None
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_55(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append(None)
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_56(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("XX  Expected Durations:XX")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_57(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  expected durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_58(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  EXPECTED DURATIONS:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_59(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append(None)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_60(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" / 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_61(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("XX-XX" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_62(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 66)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_63(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(None):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_64(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(None)
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_65(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append(None)

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_66(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("XXXX")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_67(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = None
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_68(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append(None)
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_69(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("XX  Ergodic Probabilities:XX")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_70(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  ergodic probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_71(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  ERGODIC PROBABILITIES:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_72(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append(None)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_73(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" / 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_74(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("XX-XX" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_75(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 66)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_76(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(None):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_77(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(None)

        lines.append(sep)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_78(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(None)
        return "\n".join(lines)

    def xǁRegimeResultsǁsummary__mutmut_79(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "\n".join(None)

    def xǁRegimeResultsǁsummary__mutmut_80(self) -> str:
        """Generate a formatted summary table.

        Returns
        -------
        str
            Formatted summary string with parameters per regime,
            transition matrix, expected durations, and info criteria.
        """
        lines: list[str] = []
        sep = "=" * 65
        lines.append(sep)
        lines.append(f"  {self.model_name} Results")
        lines.append(sep)
        lines.append(f"  Observations:    {self.nobs}")
        lines.append(f"  Regimes:         {self.k_regimes}")
        lines.append(f"  Parameters:      {self.n_params}")
        lines.append(f"  Log-Likelihood:  {self.loglike:.4f}")
        lines.append(f"  AIC:             {self.aic:.4f}")
        lines.append(f"  BIC:             {self.bic:.4f}")
        lines.append(f"  Converged:       {self.converged}")
        lines.append(f"  Iterations:      {self.n_iter}")
        lines.append(sep)

        # Parameters by regime
        lines.append("\n  Regime Parameters:")
        lines.append("-" * 65)
        for regime, rparams in self.regime_params.items():
            lines.append(f"  Regime {regime}:")
            for name, value in rparams.items():
                lines.append(f"    {name:20s} = {value:12.6f}")
        lines.append("")

        # Transition matrix
        lines.append("  Transition Matrix P:")
        lines.append("-" * 65)
        header = "       " + "  ".join(f"Regime {j:d}" for j in range(self.k_regimes))
        lines.append(header)
        for i in range(self.k_regimes):
            row = f"  S={i}  " + "  ".join(
                f"{self.transition_matrix[i, j]:.4f}" for j in range(self.k_regimes)
            )
            lines.append(row)
        lines.append("")

        # Expected durations
        durations = self.expected_durations()
        lines.append("  Expected Durations:")
        lines.append("-" * 65)
        for i, d in enumerate(durations):
            lines.append(f"    Regime {i}: {d:.2f} periods")
        lines.append("")

        # Ergodic probabilities
        ergodic = self.ergodic_probabilities()
        lines.append("  Ergodic Probabilities:")
        lines.append("-" * 65)
        for i, p in enumerate(ergodic):
            lines.append(f"    Regime {i}: {p:.4f}")

        lines.append(sep)
        return "XX\nXX".join(lines)

    xǁRegimeResultsǁsummary__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeResultsǁsummary__mutmut_1": xǁRegimeResultsǁsummary__mutmut_1,
        "xǁRegimeResultsǁsummary__mutmut_2": xǁRegimeResultsǁsummary__mutmut_2,
        "xǁRegimeResultsǁsummary__mutmut_3": xǁRegimeResultsǁsummary__mutmut_3,
        "xǁRegimeResultsǁsummary__mutmut_4": xǁRegimeResultsǁsummary__mutmut_4,
        "xǁRegimeResultsǁsummary__mutmut_5": xǁRegimeResultsǁsummary__mutmut_5,
        "xǁRegimeResultsǁsummary__mutmut_6": xǁRegimeResultsǁsummary__mutmut_6,
        "xǁRegimeResultsǁsummary__mutmut_7": xǁRegimeResultsǁsummary__mutmut_7,
        "xǁRegimeResultsǁsummary__mutmut_8": xǁRegimeResultsǁsummary__mutmut_8,
        "xǁRegimeResultsǁsummary__mutmut_9": xǁRegimeResultsǁsummary__mutmut_9,
        "xǁRegimeResultsǁsummary__mutmut_10": xǁRegimeResultsǁsummary__mutmut_10,
        "xǁRegimeResultsǁsummary__mutmut_11": xǁRegimeResultsǁsummary__mutmut_11,
        "xǁRegimeResultsǁsummary__mutmut_12": xǁRegimeResultsǁsummary__mutmut_12,
        "xǁRegimeResultsǁsummary__mutmut_13": xǁRegimeResultsǁsummary__mutmut_13,
        "xǁRegimeResultsǁsummary__mutmut_14": xǁRegimeResultsǁsummary__mutmut_14,
        "xǁRegimeResultsǁsummary__mutmut_15": xǁRegimeResultsǁsummary__mutmut_15,
        "xǁRegimeResultsǁsummary__mutmut_16": xǁRegimeResultsǁsummary__mutmut_16,
        "xǁRegimeResultsǁsummary__mutmut_17": xǁRegimeResultsǁsummary__mutmut_17,
        "xǁRegimeResultsǁsummary__mutmut_18": xǁRegimeResultsǁsummary__mutmut_18,
        "xǁRegimeResultsǁsummary__mutmut_19": xǁRegimeResultsǁsummary__mutmut_19,
        "xǁRegimeResultsǁsummary__mutmut_20": xǁRegimeResultsǁsummary__mutmut_20,
        "xǁRegimeResultsǁsummary__mutmut_21": xǁRegimeResultsǁsummary__mutmut_21,
        "xǁRegimeResultsǁsummary__mutmut_22": xǁRegimeResultsǁsummary__mutmut_22,
        "xǁRegimeResultsǁsummary__mutmut_23": xǁRegimeResultsǁsummary__mutmut_23,
        "xǁRegimeResultsǁsummary__mutmut_24": xǁRegimeResultsǁsummary__mutmut_24,
        "xǁRegimeResultsǁsummary__mutmut_25": xǁRegimeResultsǁsummary__mutmut_25,
        "xǁRegimeResultsǁsummary__mutmut_26": xǁRegimeResultsǁsummary__mutmut_26,
        "xǁRegimeResultsǁsummary__mutmut_27": xǁRegimeResultsǁsummary__mutmut_27,
        "xǁRegimeResultsǁsummary__mutmut_28": xǁRegimeResultsǁsummary__mutmut_28,
        "xǁRegimeResultsǁsummary__mutmut_29": xǁRegimeResultsǁsummary__mutmut_29,
        "xǁRegimeResultsǁsummary__mutmut_30": xǁRegimeResultsǁsummary__mutmut_30,
        "xǁRegimeResultsǁsummary__mutmut_31": xǁRegimeResultsǁsummary__mutmut_31,
        "xǁRegimeResultsǁsummary__mutmut_32": xǁRegimeResultsǁsummary__mutmut_32,
        "xǁRegimeResultsǁsummary__mutmut_33": xǁRegimeResultsǁsummary__mutmut_33,
        "xǁRegimeResultsǁsummary__mutmut_34": xǁRegimeResultsǁsummary__mutmut_34,
        "xǁRegimeResultsǁsummary__mutmut_35": xǁRegimeResultsǁsummary__mutmut_35,
        "xǁRegimeResultsǁsummary__mutmut_36": xǁRegimeResultsǁsummary__mutmut_36,
        "xǁRegimeResultsǁsummary__mutmut_37": xǁRegimeResultsǁsummary__mutmut_37,
        "xǁRegimeResultsǁsummary__mutmut_38": xǁRegimeResultsǁsummary__mutmut_38,
        "xǁRegimeResultsǁsummary__mutmut_39": xǁRegimeResultsǁsummary__mutmut_39,
        "xǁRegimeResultsǁsummary__mutmut_40": xǁRegimeResultsǁsummary__mutmut_40,
        "xǁRegimeResultsǁsummary__mutmut_41": xǁRegimeResultsǁsummary__mutmut_41,
        "xǁRegimeResultsǁsummary__mutmut_42": xǁRegimeResultsǁsummary__mutmut_42,
        "xǁRegimeResultsǁsummary__mutmut_43": xǁRegimeResultsǁsummary__mutmut_43,
        "xǁRegimeResultsǁsummary__mutmut_44": xǁRegimeResultsǁsummary__mutmut_44,
        "xǁRegimeResultsǁsummary__mutmut_45": xǁRegimeResultsǁsummary__mutmut_45,
        "xǁRegimeResultsǁsummary__mutmut_46": xǁRegimeResultsǁsummary__mutmut_46,
        "xǁRegimeResultsǁsummary__mutmut_47": xǁRegimeResultsǁsummary__mutmut_47,
        "xǁRegimeResultsǁsummary__mutmut_48": xǁRegimeResultsǁsummary__mutmut_48,
        "xǁRegimeResultsǁsummary__mutmut_49": xǁRegimeResultsǁsummary__mutmut_49,
        "xǁRegimeResultsǁsummary__mutmut_50": xǁRegimeResultsǁsummary__mutmut_50,
        "xǁRegimeResultsǁsummary__mutmut_51": xǁRegimeResultsǁsummary__mutmut_51,
        "xǁRegimeResultsǁsummary__mutmut_52": xǁRegimeResultsǁsummary__mutmut_52,
        "xǁRegimeResultsǁsummary__mutmut_53": xǁRegimeResultsǁsummary__mutmut_53,
        "xǁRegimeResultsǁsummary__mutmut_54": xǁRegimeResultsǁsummary__mutmut_54,
        "xǁRegimeResultsǁsummary__mutmut_55": xǁRegimeResultsǁsummary__mutmut_55,
        "xǁRegimeResultsǁsummary__mutmut_56": xǁRegimeResultsǁsummary__mutmut_56,
        "xǁRegimeResultsǁsummary__mutmut_57": xǁRegimeResultsǁsummary__mutmut_57,
        "xǁRegimeResultsǁsummary__mutmut_58": xǁRegimeResultsǁsummary__mutmut_58,
        "xǁRegimeResultsǁsummary__mutmut_59": xǁRegimeResultsǁsummary__mutmut_59,
        "xǁRegimeResultsǁsummary__mutmut_60": xǁRegimeResultsǁsummary__mutmut_60,
        "xǁRegimeResultsǁsummary__mutmut_61": xǁRegimeResultsǁsummary__mutmut_61,
        "xǁRegimeResultsǁsummary__mutmut_62": xǁRegimeResultsǁsummary__mutmut_62,
        "xǁRegimeResultsǁsummary__mutmut_63": xǁRegimeResultsǁsummary__mutmut_63,
        "xǁRegimeResultsǁsummary__mutmut_64": xǁRegimeResultsǁsummary__mutmut_64,
        "xǁRegimeResultsǁsummary__mutmut_65": xǁRegimeResultsǁsummary__mutmut_65,
        "xǁRegimeResultsǁsummary__mutmut_66": xǁRegimeResultsǁsummary__mutmut_66,
        "xǁRegimeResultsǁsummary__mutmut_67": xǁRegimeResultsǁsummary__mutmut_67,
        "xǁRegimeResultsǁsummary__mutmut_68": xǁRegimeResultsǁsummary__mutmut_68,
        "xǁRegimeResultsǁsummary__mutmut_69": xǁRegimeResultsǁsummary__mutmut_69,
        "xǁRegimeResultsǁsummary__mutmut_70": xǁRegimeResultsǁsummary__mutmut_70,
        "xǁRegimeResultsǁsummary__mutmut_71": xǁRegimeResultsǁsummary__mutmut_71,
        "xǁRegimeResultsǁsummary__mutmut_72": xǁRegimeResultsǁsummary__mutmut_72,
        "xǁRegimeResultsǁsummary__mutmut_73": xǁRegimeResultsǁsummary__mutmut_73,
        "xǁRegimeResultsǁsummary__mutmut_74": xǁRegimeResultsǁsummary__mutmut_74,
        "xǁRegimeResultsǁsummary__mutmut_75": xǁRegimeResultsǁsummary__mutmut_75,
        "xǁRegimeResultsǁsummary__mutmut_76": xǁRegimeResultsǁsummary__mutmut_76,
        "xǁRegimeResultsǁsummary__mutmut_77": xǁRegimeResultsǁsummary__mutmut_77,
        "xǁRegimeResultsǁsummary__mutmut_78": xǁRegimeResultsǁsummary__mutmut_78,
        "xǁRegimeResultsǁsummary__mutmut_79": xǁRegimeResultsǁsummary__mutmut_79,
        "xǁRegimeResultsǁsummary__mutmut_80": xǁRegimeResultsǁsummary__mutmut_80,
    }
    xǁRegimeResultsǁsummary__mutmut_orig.__name__ = "xǁRegimeResultsǁsummary"

    def expected_durations(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeResultsǁexpected_durations__mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeResultsǁexpected_durations__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeResultsǁexpected_durations__mutmut_orig(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_1(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = None
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_2(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = None
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_3(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(None)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_4(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(None):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_5(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = None
            durations[j] = 1.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_6(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = None
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_7(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 * max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_8(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 2.0 / max(1.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_9(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(None, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_10(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, None)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_11(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_12(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(
                1.0 - p_jj,
            )
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_13(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 + p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_14(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(2.0 - p_jj, 1e-12)
        return durations

    def xǁRegimeResultsǁexpected_durations__mutmut_15(self) -> NDArray[np.float64]:
        """Compute expected duration of each regime.

        E[duration of regime j] = 1 / (1 - p_{jj})

        Returns
        -------
        ndarray
            Expected durations, shape (k,).
        """
        k = self.k_regimes
        durations = np.zeros(k)
        for j in range(k):
            p_jj = self.transition_matrix[j, j]
            durations[j] = 1.0 / max(1.0 - p_jj, 1.000000000001)
        return durations

    xǁRegimeResultsǁexpected_durations__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeResultsǁexpected_durations__mutmut_1": xǁRegimeResultsǁexpected_durations__mutmut_1,
        "xǁRegimeResultsǁexpected_durations__mutmut_2": xǁRegimeResultsǁexpected_durations__mutmut_2,
        "xǁRegimeResultsǁexpected_durations__mutmut_3": xǁRegimeResultsǁexpected_durations__mutmut_3,
        "xǁRegimeResultsǁexpected_durations__mutmut_4": xǁRegimeResultsǁexpected_durations__mutmut_4,
        "xǁRegimeResultsǁexpected_durations__mutmut_5": xǁRegimeResultsǁexpected_durations__mutmut_5,
        "xǁRegimeResultsǁexpected_durations__mutmut_6": xǁRegimeResultsǁexpected_durations__mutmut_6,
        "xǁRegimeResultsǁexpected_durations__mutmut_7": xǁRegimeResultsǁexpected_durations__mutmut_7,
        "xǁRegimeResultsǁexpected_durations__mutmut_8": xǁRegimeResultsǁexpected_durations__mutmut_8,
        "xǁRegimeResultsǁexpected_durations__mutmut_9": xǁRegimeResultsǁexpected_durations__mutmut_9,
        "xǁRegimeResultsǁexpected_durations__mutmut_10": xǁRegimeResultsǁexpected_durations__mutmut_10,
        "xǁRegimeResultsǁexpected_durations__mutmut_11": xǁRegimeResultsǁexpected_durations__mutmut_11,
        "xǁRegimeResultsǁexpected_durations__mutmut_12": xǁRegimeResultsǁexpected_durations__mutmut_12,
        "xǁRegimeResultsǁexpected_durations__mutmut_13": xǁRegimeResultsǁexpected_durations__mutmut_13,
        "xǁRegimeResultsǁexpected_durations__mutmut_14": xǁRegimeResultsǁexpected_durations__mutmut_14,
        "xǁRegimeResultsǁexpected_durations__mutmut_15": xǁRegimeResultsǁexpected_durations__mutmut_15,
    }
    xǁRegimeResultsǁexpected_durations__mutmut_orig.__name__ = "xǁRegimeResultsǁexpected_durations"

    def ergodic_probabilities(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeResultsǁergodic_probabilities__mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeResultsǁergodic_probabilities__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeResultsǁergodic_probabilities__mutmut_orig(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_1(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = None
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_2(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = None
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_3(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = None
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_4(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack(None)
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_5(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T + np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_6(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(None), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_7(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(None)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_8(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = None
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_9(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(None)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_10(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k - 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_11(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 2)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_12(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = None
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_13(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[+1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_14(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-2] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_15(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 2.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_16(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = None
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_17(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(None, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_18(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, None, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_19(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_20(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_21(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(
            a_mat,
            b,
        )[0]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_22(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[1]
        pi = np.maximum(pi, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_23(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = None
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_24(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(None, 0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_25(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, None)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_26(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(0.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_27(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(
            pi,
        )
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_28(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 1.0)
        pi /= pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_29(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi = pi.sum()
        return pi

    def xǁRegimeResultsǁergodic_probabilities__mutmut_30(self) -> NDArray[np.float64]:
        """Compute ergodic (long-run) probabilities.

        Solve pi = P' * pi with sum(pi) = 1.

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = self.k_regimes
        p_mat = self.transition_matrix
        a_mat = np.vstack([p_mat.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0
        pi = np.linalg.lstsq(a_mat, b, rcond=None)[0]
        pi = np.maximum(pi, 0.0)
        pi *= pi.sum()
        return pi

    xǁRegimeResultsǁergodic_probabilities__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeResultsǁergodic_probabilities__mutmut_1": xǁRegimeResultsǁergodic_probabilities__mutmut_1,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_2": xǁRegimeResultsǁergodic_probabilities__mutmut_2,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_3": xǁRegimeResultsǁergodic_probabilities__mutmut_3,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_4": xǁRegimeResultsǁergodic_probabilities__mutmut_4,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_5": xǁRegimeResultsǁergodic_probabilities__mutmut_5,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_6": xǁRegimeResultsǁergodic_probabilities__mutmut_6,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_7": xǁRegimeResultsǁergodic_probabilities__mutmut_7,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_8": xǁRegimeResultsǁergodic_probabilities__mutmut_8,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_9": xǁRegimeResultsǁergodic_probabilities__mutmut_9,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_10": xǁRegimeResultsǁergodic_probabilities__mutmut_10,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_11": xǁRegimeResultsǁergodic_probabilities__mutmut_11,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_12": xǁRegimeResultsǁergodic_probabilities__mutmut_12,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_13": xǁRegimeResultsǁergodic_probabilities__mutmut_13,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_14": xǁRegimeResultsǁergodic_probabilities__mutmut_14,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_15": xǁRegimeResultsǁergodic_probabilities__mutmut_15,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_16": xǁRegimeResultsǁergodic_probabilities__mutmut_16,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_17": xǁRegimeResultsǁergodic_probabilities__mutmut_17,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_18": xǁRegimeResultsǁergodic_probabilities__mutmut_18,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_19": xǁRegimeResultsǁergodic_probabilities__mutmut_19,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_20": xǁRegimeResultsǁergodic_probabilities__mutmut_20,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_21": xǁRegimeResultsǁergodic_probabilities__mutmut_21,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_22": xǁRegimeResultsǁergodic_probabilities__mutmut_22,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_23": xǁRegimeResultsǁergodic_probabilities__mutmut_23,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_24": xǁRegimeResultsǁergodic_probabilities__mutmut_24,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_25": xǁRegimeResultsǁergodic_probabilities__mutmut_25,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_26": xǁRegimeResultsǁergodic_probabilities__mutmut_26,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_27": xǁRegimeResultsǁergodic_probabilities__mutmut_27,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_28": xǁRegimeResultsǁergodic_probabilities__mutmut_28,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_29": xǁRegimeResultsǁergodic_probabilities__mutmut_29,
        "xǁRegimeResultsǁergodic_probabilities__mutmut_30": xǁRegimeResultsǁergodic_probabilities__mutmut_30,
    }
    xǁRegimeResultsǁergodic_probabilities__mutmut_orig.__name__ = (
        "xǁRegimeResultsǁergodic_probabilities"
    )

    def classify(self, threshold: float = 0.5) -> NDArray[np.int64]:
        args = [threshold]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeResultsǁclassify__mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeResultsǁclassify__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeResultsǁclassify__mutmut_orig(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(self.smoothed_probs, axis=1).astype(np.int64)

    def xǁRegimeResultsǁclassify__mutmut_1(self, threshold: float = 1.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(self.smoothed_probs, axis=1).astype(np.int64)

    def xǁRegimeResultsǁclassify__mutmut_2(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(self.smoothed_probs, axis=1).astype(None)

    def xǁRegimeResultsǁclassify__mutmut_3(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(None, axis=1).astype(np.int64)

    def xǁRegimeResultsǁclassify__mutmut_4(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(self.smoothed_probs, axis=None).astype(np.int64)

    def xǁRegimeResultsǁclassify__mutmut_5(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(axis=1).astype(np.int64)

    def xǁRegimeResultsǁclassify__mutmut_6(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(
            self.smoothed_probs,
        ).astype(np.int64)

    def xǁRegimeResultsǁclassify__mutmut_7(self, threshold: float = 0.5) -> NDArray[np.int64]:
        """Classify each observation into the most probable regime.

        Parameters
        ----------
        threshold : float
            Minimum probability to classify (not used for argmax;
            kept for compatibility). Default is 0.5.

        Returns
        -------
        ndarray
            Regime classification, shape (T,).
        """
        return np.argmax(self.smoothed_probs, axis=2).astype(np.int64)

    xǁRegimeResultsǁclassify__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeResultsǁclassify__mutmut_1": xǁRegimeResultsǁclassify__mutmut_1,
        "xǁRegimeResultsǁclassify__mutmut_2": xǁRegimeResultsǁclassify__mutmut_2,
        "xǁRegimeResultsǁclassify__mutmut_3": xǁRegimeResultsǁclassify__mutmut_3,
        "xǁRegimeResultsǁclassify__mutmut_4": xǁRegimeResultsǁclassify__mutmut_4,
        "xǁRegimeResultsǁclassify__mutmut_5": xǁRegimeResultsǁclassify__mutmut_5,
        "xǁRegimeResultsǁclassify__mutmut_6": xǁRegimeResultsǁclassify__mutmut_6,
        "xǁRegimeResultsǁclassify__mutmut_7": xǁRegimeResultsǁclassify__mutmut_7,
    }
    xǁRegimeResultsǁclassify__mutmut_orig.__name__ = "xǁRegimeResultsǁclassify"

    def plot_regimes(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        args = [y, ax, figsize]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeResultsǁplot_regimes__mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeResultsǁplot_regimes__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeResultsǁplot_regimes__mutmut_orig(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_1(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is not None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_2(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """

        if ax is None:
            _, ax = None

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_3(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=None)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_4(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = None
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_5(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[1]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_6(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = None

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_7(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(None)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_8(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_9(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(None, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_10(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, None, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_11(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, None, linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_12(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=None, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_13(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=None, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_14(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label=None)

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_15(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_16(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_17(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_18(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_19(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_20(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(
                t,
                y,
                "k-",
                linewidth=0.8,
                alpha=0.8,
            )

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_21(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "XXk-XX", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_22(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "K-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_23(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=1.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_24(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=1.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_25(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="XXDataXX")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_26(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_27(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="DATA")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_28(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = None
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_29(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 1]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_30(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            None,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_31(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            None,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_32(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            None,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_33(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=None,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_34(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=None,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_35(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color=None,
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_36(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label=None,
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_37(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_38(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_39(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_40(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_41(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_42(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_43(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_44(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[1] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_45(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_46(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 1,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_47(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[2] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_48(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_49(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 2,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_50(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob >= 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_51(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 1.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_52(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=1.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_53(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="XXredXX",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_54(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="RED",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_55(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="XXRegime 0XX",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_56(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_57(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="REGIME 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_58(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel(None)
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_59(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("XXTimeXX")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_60(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("time")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_61(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("TIME")
        ax.set_title(f"{self.model_name} - Regime Classification")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_regimes__mutmut_62(
        self,
        y: NDArray[np.float64] | None = None,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 6),
    ) -> Any:
        """Plot the time series with regime shading.

        Parameters
        ----------
        y : ndarray, optional
            Time series to plot. If None, uses regime 0 smoothed prob.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        if y is not None:
            ax.plot(t, y, "k-", linewidth=0.8, alpha=0.8, label="Data")

        # Shade regime 0 (typically recession/high-vol)
        regime0_prob = self.smoothed_probs[:, 0]
        ax.fill_between(
            t,
            ax.get_ylim()[0] if y is not None else 0,
            ax.get_ylim()[1] if y is not None else 1,
            where=regime0_prob > 0.5,
            alpha=0.2,
            color="red",
            label="Regime 0",
        )

        ax.set_xlabel("Time")
        ax.set_title(None)
        ax.legend()

        return ax

    xǁRegimeResultsǁplot_regimes__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeResultsǁplot_regimes__mutmut_1": xǁRegimeResultsǁplot_regimes__mutmut_1,
        "xǁRegimeResultsǁplot_regimes__mutmut_2": xǁRegimeResultsǁplot_regimes__mutmut_2,
        "xǁRegimeResultsǁplot_regimes__mutmut_3": xǁRegimeResultsǁplot_regimes__mutmut_3,
        "xǁRegimeResultsǁplot_regimes__mutmut_4": xǁRegimeResultsǁplot_regimes__mutmut_4,
        "xǁRegimeResultsǁplot_regimes__mutmut_5": xǁRegimeResultsǁplot_regimes__mutmut_5,
        "xǁRegimeResultsǁplot_regimes__mutmut_6": xǁRegimeResultsǁplot_regimes__mutmut_6,
        "xǁRegimeResultsǁplot_regimes__mutmut_7": xǁRegimeResultsǁplot_regimes__mutmut_7,
        "xǁRegimeResultsǁplot_regimes__mutmut_8": xǁRegimeResultsǁplot_regimes__mutmut_8,
        "xǁRegimeResultsǁplot_regimes__mutmut_9": xǁRegimeResultsǁplot_regimes__mutmut_9,
        "xǁRegimeResultsǁplot_regimes__mutmut_10": xǁRegimeResultsǁplot_regimes__mutmut_10,
        "xǁRegimeResultsǁplot_regimes__mutmut_11": xǁRegimeResultsǁplot_regimes__mutmut_11,
        "xǁRegimeResultsǁplot_regimes__mutmut_12": xǁRegimeResultsǁplot_regimes__mutmut_12,
        "xǁRegimeResultsǁplot_regimes__mutmut_13": xǁRegimeResultsǁplot_regimes__mutmut_13,
        "xǁRegimeResultsǁplot_regimes__mutmut_14": xǁRegimeResultsǁplot_regimes__mutmut_14,
        "xǁRegimeResultsǁplot_regimes__mutmut_15": xǁRegimeResultsǁplot_regimes__mutmut_15,
        "xǁRegimeResultsǁplot_regimes__mutmut_16": xǁRegimeResultsǁplot_regimes__mutmut_16,
        "xǁRegimeResultsǁplot_regimes__mutmut_17": xǁRegimeResultsǁplot_regimes__mutmut_17,
        "xǁRegimeResultsǁplot_regimes__mutmut_18": xǁRegimeResultsǁplot_regimes__mutmut_18,
        "xǁRegimeResultsǁplot_regimes__mutmut_19": xǁRegimeResultsǁplot_regimes__mutmut_19,
        "xǁRegimeResultsǁplot_regimes__mutmut_20": xǁRegimeResultsǁplot_regimes__mutmut_20,
        "xǁRegimeResultsǁplot_regimes__mutmut_21": xǁRegimeResultsǁplot_regimes__mutmut_21,
        "xǁRegimeResultsǁplot_regimes__mutmut_22": xǁRegimeResultsǁplot_regimes__mutmut_22,
        "xǁRegimeResultsǁplot_regimes__mutmut_23": xǁRegimeResultsǁplot_regimes__mutmut_23,
        "xǁRegimeResultsǁplot_regimes__mutmut_24": xǁRegimeResultsǁplot_regimes__mutmut_24,
        "xǁRegimeResultsǁplot_regimes__mutmut_25": xǁRegimeResultsǁplot_regimes__mutmut_25,
        "xǁRegimeResultsǁplot_regimes__mutmut_26": xǁRegimeResultsǁplot_regimes__mutmut_26,
        "xǁRegimeResultsǁplot_regimes__mutmut_27": xǁRegimeResultsǁplot_regimes__mutmut_27,
        "xǁRegimeResultsǁplot_regimes__mutmut_28": xǁRegimeResultsǁplot_regimes__mutmut_28,
        "xǁRegimeResultsǁplot_regimes__mutmut_29": xǁRegimeResultsǁplot_regimes__mutmut_29,
        "xǁRegimeResultsǁplot_regimes__mutmut_30": xǁRegimeResultsǁplot_regimes__mutmut_30,
        "xǁRegimeResultsǁplot_regimes__mutmut_31": xǁRegimeResultsǁplot_regimes__mutmut_31,
        "xǁRegimeResultsǁplot_regimes__mutmut_32": xǁRegimeResultsǁplot_regimes__mutmut_32,
        "xǁRegimeResultsǁplot_regimes__mutmut_33": xǁRegimeResultsǁplot_regimes__mutmut_33,
        "xǁRegimeResultsǁplot_regimes__mutmut_34": xǁRegimeResultsǁplot_regimes__mutmut_34,
        "xǁRegimeResultsǁplot_regimes__mutmut_35": xǁRegimeResultsǁplot_regimes__mutmut_35,
        "xǁRegimeResultsǁplot_regimes__mutmut_36": xǁRegimeResultsǁplot_regimes__mutmut_36,
        "xǁRegimeResultsǁplot_regimes__mutmut_37": xǁRegimeResultsǁplot_regimes__mutmut_37,
        "xǁRegimeResultsǁplot_regimes__mutmut_38": xǁRegimeResultsǁplot_regimes__mutmut_38,
        "xǁRegimeResultsǁplot_regimes__mutmut_39": xǁRegimeResultsǁplot_regimes__mutmut_39,
        "xǁRegimeResultsǁplot_regimes__mutmut_40": xǁRegimeResultsǁplot_regimes__mutmut_40,
        "xǁRegimeResultsǁplot_regimes__mutmut_41": xǁRegimeResultsǁplot_regimes__mutmut_41,
        "xǁRegimeResultsǁplot_regimes__mutmut_42": xǁRegimeResultsǁplot_regimes__mutmut_42,
        "xǁRegimeResultsǁplot_regimes__mutmut_43": xǁRegimeResultsǁplot_regimes__mutmut_43,
        "xǁRegimeResultsǁplot_regimes__mutmut_44": xǁRegimeResultsǁplot_regimes__mutmut_44,
        "xǁRegimeResultsǁplot_regimes__mutmut_45": xǁRegimeResultsǁplot_regimes__mutmut_45,
        "xǁRegimeResultsǁplot_regimes__mutmut_46": xǁRegimeResultsǁplot_regimes__mutmut_46,
        "xǁRegimeResultsǁplot_regimes__mutmut_47": xǁRegimeResultsǁplot_regimes__mutmut_47,
        "xǁRegimeResultsǁplot_regimes__mutmut_48": xǁRegimeResultsǁplot_regimes__mutmut_48,
        "xǁRegimeResultsǁplot_regimes__mutmut_49": xǁRegimeResultsǁplot_regimes__mutmut_49,
        "xǁRegimeResultsǁplot_regimes__mutmut_50": xǁRegimeResultsǁplot_regimes__mutmut_50,
        "xǁRegimeResultsǁplot_regimes__mutmut_51": xǁRegimeResultsǁplot_regimes__mutmut_51,
        "xǁRegimeResultsǁplot_regimes__mutmut_52": xǁRegimeResultsǁplot_regimes__mutmut_52,
        "xǁRegimeResultsǁplot_regimes__mutmut_53": xǁRegimeResultsǁplot_regimes__mutmut_53,
        "xǁRegimeResultsǁplot_regimes__mutmut_54": xǁRegimeResultsǁplot_regimes__mutmut_54,
        "xǁRegimeResultsǁplot_regimes__mutmut_55": xǁRegimeResultsǁplot_regimes__mutmut_55,
        "xǁRegimeResultsǁplot_regimes__mutmut_56": xǁRegimeResultsǁplot_regimes__mutmut_56,
        "xǁRegimeResultsǁplot_regimes__mutmut_57": xǁRegimeResultsǁplot_regimes__mutmut_57,
        "xǁRegimeResultsǁplot_regimes__mutmut_58": xǁRegimeResultsǁplot_regimes__mutmut_58,
        "xǁRegimeResultsǁplot_regimes__mutmut_59": xǁRegimeResultsǁplot_regimes__mutmut_59,
        "xǁRegimeResultsǁplot_regimes__mutmut_60": xǁRegimeResultsǁplot_regimes__mutmut_60,
        "xǁRegimeResultsǁplot_regimes__mutmut_61": xǁRegimeResultsǁplot_regimes__mutmut_61,
        "xǁRegimeResultsǁplot_regimes__mutmut_62": xǁRegimeResultsǁplot_regimes__mutmut_62,
    }
    xǁRegimeResultsǁplot_regimes__mutmut_orig.__name__ = "xǁRegimeResultsǁplot_regimes"

    def plot_probabilities(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        args = [regime, smoothed, ax, figsize]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeResultsǁplot_probabilities__mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeResultsǁplot_probabilities__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeResultsǁplot_probabilities__mutmut_orig(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_1(
        self,
        regime: int = 1,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_2(
        self,
        regime: int = 0,
        smoothed: bool = False,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_3(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is not None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_4(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """

        if ax is None:
            _, ax = None

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_5(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=None)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_6(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = None
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_7(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[1]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_8(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = None

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_9(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(None)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_10(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            None,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_11(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            None,
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_12(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            None,
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_13(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=None,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_14(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=None,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_15(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=None,
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_16(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_17(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_18(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_19(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_20(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_21(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_22(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "XXb-XX",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_23(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "B-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_24(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=1.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_25(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=1.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_26(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                None,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_27(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                None,
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_28(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                None,
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_29(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=None,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_30(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=None,
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_31(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_32(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_33(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_34(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_35(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_36(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "XXr-XX",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_37(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "R-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_38(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=2.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_39(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(None, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_40(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, None)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_41(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_42(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(
            -0.05,
        )
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_43(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(+0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_44(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-1.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_45(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 2.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_46(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel(None)
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_47(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("XXTimeXX")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_48(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("time")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_49(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("TIME")
        ax.set_ylabel("Probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_50(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel(None)
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_51(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("XXProbabilityXX")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_52(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("probability")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_53(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("PROBABILITY")
        ax.set_title(f"Regime {regime} Probabilities")
        ax.legend()

        return ax

    def xǁRegimeResultsǁplot_probabilities__mutmut_54(
        self,
        regime: int = 0,
        smoothed: bool = True,
        ax: Any = None,
        figsize: tuple[int, int] = (14, 4),
    ) -> Any:
        """Plot filtered and/or smoothed regime probabilities.

        Parameters
        ----------
        regime : int
            Which regime to plot probabilities for.
        smoothed : bool
            If True, plot smoothed probs. Otherwise, filtered.
        ax : matplotlib Axes, optional
            Axes to plot on.
        figsize : tuple
            Figure size.

        Returns
        -------
        matplotlib Axes
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        n_obs = self.smoothed_probs.shape[0]
        t = np.arange(n_obs)

        ax.plot(
            t,
            self.filtered_probs[:, regime],
            "b-",
            alpha=0.5,
            linewidth=0.8,
            label=f"Filtered P(S_t={regime}|Y_t)",
        )

        if smoothed:
            ax.plot(
                t,
                self.smoothed_probs[:, regime],
                "r-",
                linewidth=1.2,
                label=f"Smoothed P(S_t={regime}|Y_T)",
            )

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")
        ax.set_title(None)
        ax.legend()

        return ax

    xǁRegimeResultsǁplot_probabilities__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeResultsǁplot_probabilities__mutmut_1": xǁRegimeResultsǁplot_probabilities__mutmut_1,
        "xǁRegimeResultsǁplot_probabilities__mutmut_2": xǁRegimeResultsǁplot_probabilities__mutmut_2,
        "xǁRegimeResultsǁplot_probabilities__mutmut_3": xǁRegimeResultsǁplot_probabilities__mutmut_3,
        "xǁRegimeResultsǁplot_probabilities__mutmut_4": xǁRegimeResultsǁplot_probabilities__mutmut_4,
        "xǁRegimeResultsǁplot_probabilities__mutmut_5": xǁRegimeResultsǁplot_probabilities__mutmut_5,
        "xǁRegimeResultsǁplot_probabilities__mutmut_6": xǁRegimeResultsǁplot_probabilities__mutmut_6,
        "xǁRegimeResultsǁplot_probabilities__mutmut_7": xǁRegimeResultsǁplot_probabilities__mutmut_7,
        "xǁRegimeResultsǁplot_probabilities__mutmut_8": xǁRegimeResultsǁplot_probabilities__mutmut_8,
        "xǁRegimeResultsǁplot_probabilities__mutmut_9": xǁRegimeResultsǁplot_probabilities__mutmut_9,
        "xǁRegimeResultsǁplot_probabilities__mutmut_10": xǁRegimeResultsǁplot_probabilities__mutmut_10,
        "xǁRegimeResultsǁplot_probabilities__mutmut_11": xǁRegimeResultsǁplot_probabilities__mutmut_11,
        "xǁRegimeResultsǁplot_probabilities__mutmut_12": xǁRegimeResultsǁplot_probabilities__mutmut_12,
        "xǁRegimeResultsǁplot_probabilities__mutmut_13": xǁRegimeResultsǁplot_probabilities__mutmut_13,
        "xǁRegimeResultsǁplot_probabilities__mutmut_14": xǁRegimeResultsǁplot_probabilities__mutmut_14,
        "xǁRegimeResultsǁplot_probabilities__mutmut_15": xǁRegimeResultsǁplot_probabilities__mutmut_15,
        "xǁRegimeResultsǁplot_probabilities__mutmut_16": xǁRegimeResultsǁplot_probabilities__mutmut_16,
        "xǁRegimeResultsǁplot_probabilities__mutmut_17": xǁRegimeResultsǁplot_probabilities__mutmut_17,
        "xǁRegimeResultsǁplot_probabilities__mutmut_18": xǁRegimeResultsǁplot_probabilities__mutmut_18,
        "xǁRegimeResultsǁplot_probabilities__mutmut_19": xǁRegimeResultsǁplot_probabilities__mutmut_19,
        "xǁRegimeResultsǁplot_probabilities__mutmut_20": xǁRegimeResultsǁplot_probabilities__mutmut_20,
        "xǁRegimeResultsǁplot_probabilities__mutmut_21": xǁRegimeResultsǁplot_probabilities__mutmut_21,
        "xǁRegimeResultsǁplot_probabilities__mutmut_22": xǁRegimeResultsǁplot_probabilities__mutmut_22,
        "xǁRegimeResultsǁplot_probabilities__mutmut_23": xǁRegimeResultsǁplot_probabilities__mutmut_23,
        "xǁRegimeResultsǁplot_probabilities__mutmut_24": xǁRegimeResultsǁplot_probabilities__mutmut_24,
        "xǁRegimeResultsǁplot_probabilities__mutmut_25": xǁRegimeResultsǁplot_probabilities__mutmut_25,
        "xǁRegimeResultsǁplot_probabilities__mutmut_26": xǁRegimeResultsǁplot_probabilities__mutmut_26,
        "xǁRegimeResultsǁplot_probabilities__mutmut_27": xǁRegimeResultsǁplot_probabilities__mutmut_27,
        "xǁRegimeResultsǁplot_probabilities__mutmut_28": xǁRegimeResultsǁplot_probabilities__mutmut_28,
        "xǁRegimeResultsǁplot_probabilities__mutmut_29": xǁRegimeResultsǁplot_probabilities__mutmut_29,
        "xǁRegimeResultsǁplot_probabilities__mutmut_30": xǁRegimeResultsǁplot_probabilities__mutmut_30,
        "xǁRegimeResultsǁplot_probabilities__mutmut_31": xǁRegimeResultsǁplot_probabilities__mutmut_31,
        "xǁRegimeResultsǁplot_probabilities__mutmut_32": xǁRegimeResultsǁplot_probabilities__mutmut_32,
        "xǁRegimeResultsǁplot_probabilities__mutmut_33": xǁRegimeResultsǁplot_probabilities__mutmut_33,
        "xǁRegimeResultsǁplot_probabilities__mutmut_34": xǁRegimeResultsǁplot_probabilities__mutmut_34,
        "xǁRegimeResultsǁplot_probabilities__mutmut_35": xǁRegimeResultsǁplot_probabilities__mutmut_35,
        "xǁRegimeResultsǁplot_probabilities__mutmut_36": xǁRegimeResultsǁplot_probabilities__mutmut_36,
        "xǁRegimeResultsǁplot_probabilities__mutmut_37": xǁRegimeResultsǁplot_probabilities__mutmut_37,
        "xǁRegimeResultsǁplot_probabilities__mutmut_38": xǁRegimeResultsǁplot_probabilities__mutmut_38,
        "xǁRegimeResultsǁplot_probabilities__mutmut_39": xǁRegimeResultsǁplot_probabilities__mutmut_39,
        "xǁRegimeResultsǁplot_probabilities__mutmut_40": xǁRegimeResultsǁplot_probabilities__mutmut_40,
        "xǁRegimeResultsǁplot_probabilities__mutmut_41": xǁRegimeResultsǁplot_probabilities__mutmut_41,
        "xǁRegimeResultsǁplot_probabilities__mutmut_42": xǁRegimeResultsǁplot_probabilities__mutmut_42,
        "xǁRegimeResultsǁplot_probabilities__mutmut_43": xǁRegimeResultsǁplot_probabilities__mutmut_43,
        "xǁRegimeResultsǁplot_probabilities__mutmut_44": xǁRegimeResultsǁplot_probabilities__mutmut_44,
        "xǁRegimeResultsǁplot_probabilities__mutmut_45": xǁRegimeResultsǁplot_probabilities__mutmut_45,
        "xǁRegimeResultsǁplot_probabilities__mutmut_46": xǁRegimeResultsǁplot_probabilities__mutmut_46,
        "xǁRegimeResultsǁplot_probabilities__mutmut_47": xǁRegimeResultsǁplot_probabilities__mutmut_47,
        "xǁRegimeResultsǁplot_probabilities__mutmut_48": xǁRegimeResultsǁplot_probabilities__mutmut_48,
        "xǁRegimeResultsǁplot_probabilities__mutmut_49": xǁRegimeResultsǁplot_probabilities__mutmut_49,
        "xǁRegimeResultsǁplot_probabilities__mutmut_50": xǁRegimeResultsǁplot_probabilities__mutmut_50,
        "xǁRegimeResultsǁplot_probabilities__mutmut_51": xǁRegimeResultsǁplot_probabilities__mutmut_51,
        "xǁRegimeResultsǁplot_probabilities__mutmut_52": xǁRegimeResultsǁplot_probabilities__mutmut_52,
        "xǁRegimeResultsǁplot_probabilities__mutmut_53": xǁRegimeResultsǁplot_probabilities__mutmut_53,
        "xǁRegimeResultsǁplot_probabilities__mutmut_54": xǁRegimeResultsǁplot_probabilities__mutmut_54,
    }
    xǁRegimeResultsǁplot_probabilities__mutmut_orig.__name__ = "xǁRegimeResultsǁplot_probabilities"
