"""Normal (Gaussian) conditional distribution."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from archbox.distributions.base import Distribution

_LOG_2PI = np.log(2.0 * np.pi)
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


class Normal(Distribution):
    """Standard Normal distribution for GARCH innovations.

    The log-likelihood per observation is:
        ll_t = -0.5 * (log(2*pi) + log(sigma^2_t) + eps^2_t / sigma^2_t)

    No additional parameters.
    """

    name: str = "Normal"

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [resids, sigma2]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁNormalǁloglikelihood__mutmut_orig"),
            object.__getattribute__(self, "xǁNormalǁloglikelihood__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁNormalǁloglikelihood__mutmut_orig(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI + np.log(sigma2) + resids**2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_1(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 / (_LOG_2PI + np.log(sigma2) + resids**2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_2(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return +0.5 * (_LOG_2PI + np.log(sigma2) + resids**2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_3(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -1.5 * (_LOG_2PI + np.log(sigma2) + resids**2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_4(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI + np.log(sigma2) - resids**2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_5(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI - np.log(sigma2) + resids**2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_6(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI + np.log(None) + resids**2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_7(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI + np.log(sigma2) + resids**2 * sigma2)

    def xǁNormalǁloglikelihood__mutmut_8(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI + np.log(sigma2) + resids * 2 / sigma2)

    def xǁNormalǁloglikelihood__mutmut_9(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI + np.log(sigma2) + resids**3 / sigma2)

    xǁNormalǁloglikelihood__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁNormalǁloglikelihood__mutmut_1": xǁNormalǁloglikelihood__mutmut_1,
        "xǁNormalǁloglikelihood__mutmut_2": xǁNormalǁloglikelihood__mutmut_2,
        "xǁNormalǁloglikelihood__mutmut_3": xǁNormalǁloglikelihood__mutmut_3,
        "xǁNormalǁloglikelihood__mutmut_4": xǁNormalǁloglikelihood__mutmut_4,
        "xǁNormalǁloglikelihood__mutmut_5": xǁNormalǁloglikelihood__mutmut_5,
        "xǁNormalǁloglikelihood__mutmut_6": xǁNormalǁloglikelihood__mutmut_6,
        "xǁNormalǁloglikelihood__mutmut_7": xǁNormalǁloglikelihood__mutmut_7,
        "xǁNormalǁloglikelihood__mutmut_8": xǁNormalǁloglikelihood__mutmut_8,
        "xǁNormalǁloglikelihood__mutmut_9": xǁNormalǁloglikelihood__mutmut_9,
    }
    xǁNormalǁloglikelihood__mutmut_orig.__name__ = "xǁNormalǁloglikelihood"

    def ppf(self, q: float) -> float:
        args = [q]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁNormalǁppf__mutmut_orig"),
            object.__getattribute__(self, "xǁNormalǁppf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁNormalǁppf__mutmut_orig(self, q: float) -> float:
        """Normal percent point function.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that Phi(x) = q.
        """
        return float(stats.norm.ppf(q))

    def xǁNormalǁppf__mutmut_1(self, q: float) -> float:
        """Normal percent point function.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that Phi(x) = q.
        """
        return float(None)

    def xǁNormalǁppf__mutmut_2(self, q: float) -> float:
        """Normal percent point function.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that Phi(x) = q.
        """
        return float(stats.norm.ppf(None))

    xǁNormalǁppf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁNormalǁppf__mutmut_1": xǁNormalǁppf__mutmut_1,
        "xǁNormalǁppf__mutmut_2": xǁNormalǁppf__mutmut_2,
    }
    xǁNormalǁppf__mutmut_orig.__name__ = "xǁNormalǁppf"

    def cdf(self, x: float) -> float:
        args = [x]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁNormalǁcdf__mutmut_orig"),
            object.__getattribute__(self, "xǁNormalǁcdf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁNormalǁcdf__mutmut_orig(self, x: float) -> float:
        """Normal CDF.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            Phi(x).
        """
        return float(stats.norm.cdf(x))

    def xǁNormalǁcdf__mutmut_1(self, x: float) -> float:
        """Normal CDF.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            Phi(x).
        """
        return float(None)

    def xǁNormalǁcdf__mutmut_2(self, x: float) -> float:
        """Normal CDF.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            Phi(x).
        """
        return float(stats.norm.cdf(None))

    xǁNormalǁcdf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁNormalǁcdf__mutmut_1": xǁNormalǁcdf__mutmut_1,
        "xǁNormalǁcdf__mutmut_2": xǁNormalǁcdf__mutmut_2,
    }
    xǁNormalǁcdf__mutmut_orig.__name__ = "xǁNormalǁcdf"

    def simulate(self, n: int, rng: np.random.Generator) -> NDArray[np.float64]:
        args = [n, rng]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁNormalǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁNormalǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁNormalǁsimulate__mutmut_orig(
        self, n: int, rng: np.random.Generator
    ) -> NDArray[np.float64]:
        """Simulate n standard normal draws.

        Parameters
        ----------
        n : int
            Number of draws.
        rng : np.random.Generator
            Random number generator.

        Returns
        -------
        ndarray
            z_t ~ N(0,1), shape (n,).
        """
        return rng.standard_normal(n)

    def xǁNormalǁsimulate__mutmut_1(self, n: int, rng: np.random.Generator) -> NDArray[np.float64]:
        """Simulate n standard normal draws.

        Parameters
        ----------
        n : int
            Number of draws.
        rng : np.random.Generator
            Random number generator.

        Returns
        -------
        ndarray
            z_t ~ N(0,1), shape (n,).
        """
        return rng.standard_normal(None)

    xǁNormalǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁNormalǁsimulate__mutmut_1": xǁNormalǁsimulate__mutmut_1
    }
    xǁNormalǁsimulate__mutmut_orig.__name__ = "xǁNormalǁsimulate"

    @property
    def num_params(self) -> int:
        """Normal has no additional parameters."""
        return 0

    @property
    def param_names(self) -> list[str]:
        """No parameter names."""
        return []

    def start_params(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁNormalǁstart_params__mutmut_orig"),
            object.__getattribute__(self, "xǁNormalǁstart_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁNormalǁstart_params__mutmut_orig(self) -> NDArray[np.float64]:
        """Empty array (no parameters)."""
        return np.array([], dtype=np.float64)

    def xǁNormalǁstart_params__mutmut_1(self) -> NDArray[np.float64]:
        """Empty array (no parameters)."""
        return np.array(None, dtype=np.float64)

    def xǁNormalǁstart_params__mutmut_2(self) -> NDArray[np.float64]:
        """Empty array (no parameters)."""
        return np.array([], dtype=None)

    def xǁNormalǁstart_params__mutmut_3(self) -> NDArray[np.float64]:
        """Empty array (no parameters)."""
        return np.array(dtype=np.float64)

    def xǁNormalǁstart_params__mutmut_4(self) -> NDArray[np.float64]:
        """Empty array (no parameters)."""
        return np.array(
            [],
        )

    xǁNormalǁstart_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁNormalǁstart_params__mutmut_1": xǁNormalǁstart_params__mutmut_1,
        "xǁNormalǁstart_params__mutmut_2": xǁNormalǁstart_params__mutmut_2,
        "xǁNormalǁstart_params__mutmut_3": xǁNormalǁstart_params__mutmut_3,
        "xǁNormalǁstart_params__mutmut_4": xǁNormalǁstart_params__mutmut_4,
    }
    xǁNormalǁstart_params__mutmut_orig.__name__ = "xǁNormalǁstart_params"

    def bounds(self) -> list[tuple[float, float]]:
        """Empty list (no parameters)."""
        return []
