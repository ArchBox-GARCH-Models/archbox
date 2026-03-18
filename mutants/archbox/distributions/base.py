"""Base class for conditional distributions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Annotated

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


class Distribution(ABC):
    """Abstract base class for conditional distributions.

    The distribution defines the shape of the log-likelihood and provides
    simulation capabilities for z_t ~ D(0,1).
    """

    name: str = "Unknown"

    @abstractmethod
    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t = r_t - mu, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """

    @abstractmethod
    def ppf(self, q: float) -> float:
        """Percent point function (inverse CDF).

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """

    @abstractmethod
    def cdf(self, x: float) -> float:
        """Cumulative distribution function.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """

    @abstractmethod
    def simulate(self, n: int, rng: np.random.Generator) -> NDArray[np.float64]:
        """Simulate n draws from D(0, 1).

        Parameters
        ----------
        n : int
            Number of draws.
        rng : np.random.Generator
            Random number generator.

        Returns
        -------
        ndarray
            Simulated innovations z_t, shape (n,).
        """

    @property
    @abstractmethod
    def num_params(self) -> int:
        """Number of distribution parameters (0 for Normal)."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Distribution parameter names."""

    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""

    @abstractmethod
    def bounds(self) -> list[tuple[float, float]]:
        """Bounds for distribution parameters."""
