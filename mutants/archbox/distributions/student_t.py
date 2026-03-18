"""Student-t conditional distribution (Bollerslev, 1987).

f(z; nu) = Gamma((nu+1)/2) / (sqrt(pi*(nu-2)) * Gamma(nu/2)) * (1 + z^2/(nu-2))^{-(nu+1)/2}
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, ClassVar

import numpy as np
from numpy.typing import NDArray
from scipy import stats
from scipy.special import gammaln

from archbox.distributions.base import Distribution

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


class StudentT(Distribution):
    """Student-t distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Degrees of freedom. Must be > 2. If None, estimated from data.
    """

    name = "Student-t"

    def __init__(self, nu: float | None = None) -> None:
        args = [nu]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁ__init____mutmut_orig(self, nu: float | None = None) -> None:
        """Initialize Student-t distribution with optional degrees of freedom."""
        self._fixed_nu = nu

    def xǁStudentTǁ__init____mutmut_1(self, nu: float | None = None) -> None:
        """Initialize Student-t distribution with optional degrees of freedom."""
        self._fixed_nu = None

    xǁStudentTǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁ__init____mutmut_1": xǁStudentTǁ__init____mutmut_1
    }
    xǁStudentTǁ__init____mutmut_orig.__name__ = "xǁStudentTǁ__init__"

    @property
    def num_params(self) -> int:
        """Number of distribution shape parameters."""
        return 0 if self._fixed_nu is not None else 1

    @property
    def param_names(self) -> list[str]:
        """Distribution parameter names."""
        return [] if self._fixed_nu is not None else ["nu"]

    def start_params(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁstart_params__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁstart_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁstart_params__mutmut_orig(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=np.float64)
        return np.array([8.0])

    def xǁStudentTǁstart_params__mutmut_1(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is None:
            return np.array([], dtype=np.float64)
        return np.array([8.0])

    def xǁStudentTǁstart_params__mutmut_2(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array(None, dtype=np.float64)
        return np.array([8.0])

    def xǁStudentTǁstart_params__mutmut_3(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=None)
        return np.array([8.0])

    def xǁStudentTǁstart_params__mutmut_4(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array(dtype=np.float64)
        return np.array([8.0])

    def xǁStudentTǁstart_params__mutmut_5(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array(
                [],
            )
        return np.array([8.0])

    def xǁStudentTǁstart_params__mutmut_6(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=np.float64)
        return np.array(None)

    def xǁStudentTǁstart_params__mutmut_7(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=np.float64)
        return np.array([9.0])

    xǁStudentTǁstart_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁstart_params__mutmut_1": xǁStudentTǁstart_params__mutmut_1,
        "xǁStudentTǁstart_params__mutmut_2": xǁStudentTǁstart_params__mutmut_2,
        "xǁStudentTǁstart_params__mutmut_3": xǁStudentTǁstart_params__mutmut_3,
        "xǁStudentTǁstart_params__mutmut_4": xǁStudentTǁstart_params__mutmut_4,
        "xǁStudentTǁstart_params__mutmut_5": xǁStudentTǁstart_params__mutmut_5,
        "xǁStudentTǁstart_params__mutmut_6": xǁStudentTǁstart_params__mutmut_6,
        "xǁStudentTǁstart_params__mutmut_7": xǁStudentTǁstart_params__mutmut_7,
    }
    xǁStudentTǁstart_params__mutmut_orig.__name__ = "xǁStudentTǁstart_params"

    def _get_nu(self, dist_params: NDArray[np.float64] | None = None) -> float:
        args = [dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁ_get_nu__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁ_get_nu__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁ_get_nu__mutmut_orig(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_1(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_2(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = None
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_3(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None or len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_4(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_5(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) >= 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_6(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 1:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_7(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = None
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_8(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(None)
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_9(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[1])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_10(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = None
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_11(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 9.0
        return max(nu, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_12(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(None, 2.01)

    def xǁStudentTǁ_get_nu__mutmut_13(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, None)

    def xǁStudentTǁ_get_nu__mutmut_14(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(2.01)

    def xǁStudentTǁ_get_nu__mutmut_15(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(
            nu,
        )

    def xǁStudentTǁ_get_nu__mutmut_16(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 3.01)

    xǁStudentTǁ_get_nu__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁ_get_nu__mutmut_1": xǁStudentTǁ_get_nu__mutmut_1,
        "xǁStudentTǁ_get_nu__mutmut_2": xǁStudentTǁ_get_nu__mutmut_2,
        "xǁStudentTǁ_get_nu__mutmut_3": xǁStudentTǁ_get_nu__mutmut_3,
        "xǁStudentTǁ_get_nu__mutmut_4": xǁStudentTǁ_get_nu__mutmut_4,
        "xǁStudentTǁ_get_nu__mutmut_5": xǁStudentTǁ_get_nu__mutmut_5,
        "xǁStudentTǁ_get_nu__mutmut_6": xǁStudentTǁ_get_nu__mutmut_6,
        "xǁStudentTǁ_get_nu__mutmut_7": xǁStudentTǁ_get_nu__mutmut_7,
        "xǁStudentTǁ_get_nu__mutmut_8": xǁStudentTǁ_get_nu__mutmut_8,
        "xǁStudentTǁ_get_nu__mutmut_9": xǁStudentTǁ_get_nu__mutmut_9,
        "xǁStudentTǁ_get_nu__mutmut_10": xǁStudentTǁ_get_nu__mutmut_10,
        "xǁStudentTǁ_get_nu__mutmut_11": xǁStudentTǁ_get_nu__mutmut_11,
        "xǁStudentTǁ_get_nu__mutmut_12": xǁStudentTǁ_get_nu__mutmut_12,
        "xǁStudentTǁ_get_nu__mutmut_13": xǁStudentTǁ_get_nu__mutmut_13,
        "xǁStudentTǁ_get_nu__mutmut_14": xǁStudentTǁ_get_nu__mutmut_14,
        "xǁStudentTǁ_get_nu__mutmut_15": xǁStudentTǁ_get_nu__mutmut_15,
        "xǁStudentTǁ_get_nu__mutmut_16": xǁStudentTǁ_get_nu__mutmut_16,
    }
    xǁStudentTǁ_get_nu__mutmut_orig.__name__ = "xǁStudentTǁ_get_nu"

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [resids, sigma2, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁloglikelihood__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁloglikelihood__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁloglikelihood__mutmut_orig(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_1(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = None
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_2(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(None)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_3(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = None

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_4(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids * np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_5(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(None)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_6(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = None
        return ll

    def xǁStudentTǁloglikelihood__mutmut_7(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            + ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_8(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            + 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_9(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            + 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_10(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            + gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_11(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln(None)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_12(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) * 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_13(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu - 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_14(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 2) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_15(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 3)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_16(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(None)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_17(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu * 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_18(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 3)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_19(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 / np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_20(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 1.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_21(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(None)
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_22(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi / (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_23(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu + 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_24(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 3))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_25(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 / np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_26(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 1.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_27(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(None)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_28(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) / np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_29(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) * 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_30(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu - 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_31(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 2) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_32(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 3) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_33(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(None)
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_34(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 - z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_35(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(2 + z**2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_36(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 * (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_37(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z * 2 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_38(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**3 / (nu - 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_39(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu + 2))
        )
        return ll

    def xǁStudentTǁloglikelihood__mutmut_40(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 3))
        )
        return ll

    xǁStudentTǁloglikelihood__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁloglikelihood__mutmut_1": xǁStudentTǁloglikelihood__mutmut_1,
        "xǁStudentTǁloglikelihood__mutmut_2": xǁStudentTǁloglikelihood__mutmut_2,
        "xǁStudentTǁloglikelihood__mutmut_3": xǁStudentTǁloglikelihood__mutmut_3,
        "xǁStudentTǁloglikelihood__mutmut_4": xǁStudentTǁloglikelihood__mutmut_4,
        "xǁStudentTǁloglikelihood__mutmut_5": xǁStudentTǁloglikelihood__mutmut_5,
        "xǁStudentTǁloglikelihood__mutmut_6": xǁStudentTǁloglikelihood__mutmut_6,
        "xǁStudentTǁloglikelihood__mutmut_7": xǁStudentTǁloglikelihood__mutmut_7,
        "xǁStudentTǁloglikelihood__mutmut_8": xǁStudentTǁloglikelihood__mutmut_8,
        "xǁStudentTǁloglikelihood__mutmut_9": xǁStudentTǁloglikelihood__mutmut_9,
        "xǁStudentTǁloglikelihood__mutmut_10": xǁStudentTǁloglikelihood__mutmut_10,
        "xǁStudentTǁloglikelihood__mutmut_11": xǁStudentTǁloglikelihood__mutmut_11,
        "xǁStudentTǁloglikelihood__mutmut_12": xǁStudentTǁloglikelihood__mutmut_12,
        "xǁStudentTǁloglikelihood__mutmut_13": xǁStudentTǁloglikelihood__mutmut_13,
        "xǁStudentTǁloglikelihood__mutmut_14": xǁStudentTǁloglikelihood__mutmut_14,
        "xǁStudentTǁloglikelihood__mutmut_15": xǁStudentTǁloglikelihood__mutmut_15,
        "xǁStudentTǁloglikelihood__mutmut_16": xǁStudentTǁloglikelihood__mutmut_16,
        "xǁStudentTǁloglikelihood__mutmut_17": xǁStudentTǁloglikelihood__mutmut_17,
        "xǁStudentTǁloglikelihood__mutmut_18": xǁStudentTǁloglikelihood__mutmut_18,
        "xǁStudentTǁloglikelihood__mutmut_19": xǁStudentTǁloglikelihood__mutmut_19,
        "xǁStudentTǁloglikelihood__mutmut_20": xǁStudentTǁloglikelihood__mutmut_20,
        "xǁStudentTǁloglikelihood__mutmut_21": xǁStudentTǁloglikelihood__mutmut_21,
        "xǁStudentTǁloglikelihood__mutmut_22": xǁStudentTǁloglikelihood__mutmut_22,
        "xǁStudentTǁloglikelihood__mutmut_23": xǁStudentTǁloglikelihood__mutmut_23,
        "xǁStudentTǁloglikelihood__mutmut_24": xǁStudentTǁloglikelihood__mutmut_24,
        "xǁStudentTǁloglikelihood__mutmut_25": xǁStudentTǁloglikelihood__mutmut_25,
        "xǁStudentTǁloglikelihood__mutmut_26": xǁStudentTǁloglikelihood__mutmut_26,
        "xǁStudentTǁloglikelihood__mutmut_27": xǁStudentTǁloglikelihood__mutmut_27,
        "xǁStudentTǁloglikelihood__mutmut_28": xǁStudentTǁloglikelihood__mutmut_28,
        "xǁStudentTǁloglikelihood__mutmut_29": xǁStudentTǁloglikelihood__mutmut_29,
        "xǁStudentTǁloglikelihood__mutmut_30": xǁStudentTǁloglikelihood__mutmut_30,
        "xǁStudentTǁloglikelihood__mutmut_31": xǁStudentTǁloglikelihood__mutmut_31,
        "xǁStudentTǁloglikelihood__mutmut_32": xǁStudentTǁloglikelihood__mutmut_32,
        "xǁStudentTǁloglikelihood__mutmut_33": xǁStudentTǁloglikelihood__mutmut_33,
        "xǁStudentTǁloglikelihood__mutmut_34": xǁStudentTǁloglikelihood__mutmut_34,
        "xǁStudentTǁloglikelihood__mutmut_35": xǁStudentTǁloglikelihood__mutmut_35,
        "xǁStudentTǁloglikelihood__mutmut_36": xǁStudentTǁloglikelihood__mutmut_36,
        "xǁStudentTǁloglikelihood__mutmut_37": xǁStudentTǁloglikelihood__mutmut_37,
        "xǁStudentTǁloglikelihood__mutmut_38": xǁStudentTǁloglikelihood__mutmut_38,
        "xǁStudentTǁloglikelihood__mutmut_39": xǁStudentTǁloglikelihood__mutmut_39,
        "xǁStudentTǁloglikelihood__mutmut_40": xǁStudentTǁloglikelihood__mutmut_40,
    }
    xǁStudentTǁloglikelihood__mutmut_orig.__name__ = "xǁStudentTǁloglikelihood"

    def ppf(self, q: float) -> float:
        args = [q]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁppf__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁppf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁppf__mutmut_orig(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) / np.sqrt(nu / (nu - 2)))

    def xǁStudentTǁppf__mutmut_1(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = None
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) / np.sqrt(nu / (nu - 2)))

    def xǁStudentTǁppf__mutmut_2(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(None)

    def xǁStudentTǁppf__mutmut_3(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) * np.sqrt(nu / (nu - 2)))

    def xǁStudentTǁppf__mutmut_4(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(None, df=nu) / np.sqrt(nu / (nu - 2)))

    def xǁStudentTǁppf__mutmut_5(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=None) / np.sqrt(nu / (nu - 2)))

    def xǁStudentTǁppf__mutmut_6(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(df=nu) / np.sqrt(nu / (nu - 2)))

    def xǁStudentTǁppf__mutmut_7(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(
            stats.t.ppf(
                q,
            )
            / np.sqrt(nu / (nu - 2))
        )

    def xǁStudentTǁppf__mutmut_8(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) / np.sqrt(None))

    def xǁStudentTǁppf__mutmut_9(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) / np.sqrt(nu * (nu - 2)))

    def xǁStudentTǁppf__mutmut_10(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) / np.sqrt(nu / (nu + 2)))

    def xǁStudentTǁppf__mutmut_11(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) / np.sqrt(nu / (nu - 3)))

    xǁStudentTǁppf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁppf__mutmut_1": xǁStudentTǁppf__mutmut_1,
        "xǁStudentTǁppf__mutmut_2": xǁStudentTǁppf__mutmut_2,
        "xǁStudentTǁppf__mutmut_3": xǁStudentTǁppf__mutmut_3,
        "xǁStudentTǁppf__mutmut_4": xǁStudentTǁppf__mutmut_4,
        "xǁStudentTǁppf__mutmut_5": xǁStudentTǁppf__mutmut_5,
        "xǁStudentTǁppf__mutmut_6": xǁStudentTǁppf__mutmut_6,
        "xǁStudentTǁppf__mutmut_7": xǁStudentTǁppf__mutmut_7,
        "xǁStudentTǁppf__mutmut_8": xǁStudentTǁppf__mutmut_8,
        "xǁStudentTǁppf__mutmut_9": xǁStudentTǁppf__mutmut_9,
        "xǁStudentTǁppf__mutmut_10": xǁStudentTǁppf__mutmut_10,
        "xǁStudentTǁppf__mutmut_11": xǁStudentTǁppf__mutmut_11,
    }
    xǁStudentTǁppf__mutmut_orig.__name__ = "xǁStudentTǁppf"

    def cdf(self, x: float) -> float:
        args = [x]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁcdf__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁcdf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁcdf__mutmut_orig(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x * np.sqrt(nu / (nu - 2)), df=nu))

    def xǁStudentTǁcdf__mutmut_1(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = None
        return float(stats.t.cdf(x * np.sqrt(nu / (nu - 2)), df=nu))

    def xǁStudentTǁcdf__mutmut_2(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(None)

    def xǁStudentTǁcdf__mutmut_3(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(None, df=nu))

    def xǁStudentTǁcdf__mutmut_4(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x * np.sqrt(nu / (nu - 2)), df=None))

    def xǁStudentTǁcdf__mutmut_5(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(df=nu))

    def xǁStudentTǁcdf__mutmut_6(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(
            stats.t.cdf(
                x * np.sqrt(nu / (nu - 2)),
            )
        )

    def xǁStudentTǁcdf__mutmut_7(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x / np.sqrt(nu / (nu - 2)), df=nu))

    def xǁStudentTǁcdf__mutmut_8(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x * np.sqrt(None), df=nu))

    def xǁStudentTǁcdf__mutmut_9(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x * np.sqrt(nu * (nu - 2)), df=nu))

    def xǁStudentTǁcdf__mutmut_10(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x * np.sqrt(nu / (nu + 2)), df=nu))

    def xǁStudentTǁcdf__mutmut_11(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x * np.sqrt(nu / (nu - 3)), df=nu))

    xǁStudentTǁcdf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁcdf__mutmut_1": xǁStudentTǁcdf__mutmut_1,
        "xǁStudentTǁcdf__mutmut_2": xǁStudentTǁcdf__mutmut_2,
        "xǁStudentTǁcdf__mutmut_3": xǁStudentTǁcdf__mutmut_3,
        "xǁStudentTǁcdf__mutmut_4": xǁStudentTǁcdf__mutmut_4,
        "xǁStudentTǁcdf__mutmut_5": xǁStudentTǁcdf__mutmut_5,
        "xǁStudentTǁcdf__mutmut_6": xǁStudentTǁcdf__mutmut_6,
        "xǁStudentTǁcdf__mutmut_7": xǁStudentTǁcdf__mutmut_7,
        "xǁStudentTǁcdf__mutmut_8": xǁStudentTǁcdf__mutmut_8,
        "xǁStudentTǁcdf__mutmut_9": xǁStudentTǁcdf__mutmut_9,
        "xǁStudentTǁcdf__mutmut_10": xǁStudentTǁcdf__mutmut_10,
        "xǁStudentTǁcdf__mutmut_11": xǁStudentTǁcdf__mutmut_11,
    }
    xǁStudentTǁcdf__mutmut_orig.__name__ = "xǁStudentTǁcdf"

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [n, rng, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁsimulate__mutmut_orig(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_1(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = None
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_2(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(None)
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_3(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = None
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_4(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(None, size=n)
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_5(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=None)
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_6(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(size=n)
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_7(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(
            nu,
        )
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_8(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = None
        return z

    def xǁStudentTǁsimulate__mutmut_9(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = z * np.sqrt(nu / (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_10(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(None)
        return z

    def xǁStudentTǁsimulate__mutmut_11(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(nu * (nu - 2))
        return z

    def xǁStudentTǁsimulate__mutmut_12(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(nu / (nu + 2))
        return z

    def xǁStudentTǁsimulate__mutmut_13(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(nu / (nu - 3))
        return z

    xǁStudentTǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁsimulate__mutmut_1": xǁStudentTǁsimulate__mutmut_1,
        "xǁStudentTǁsimulate__mutmut_2": xǁStudentTǁsimulate__mutmut_2,
        "xǁStudentTǁsimulate__mutmut_3": xǁStudentTǁsimulate__mutmut_3,
        "xǁStudentTǁsimulate__mutmut_4": xǁStudentTǁsimulate__mutmut_4,
        "xǁStudentTǁsimulate__mutmut_5": xǁStudentTǁsimulate__mutmut_5,
        "xǁStudentTǁsimulate__mutmut_6": xǁStudentTǁsimulate__mutmut_6,
        "xǁStudentTǁsimulate__mutmut_7": xǁStudentTǁsimulate__mutmut_7,
        "xǁStudentTǁsimulate__mutmut_8": xǁStudentTǁsimulate__mutmut_8,
        "xǁStudentTǁsimulate__mutmut_9": xǁStudentTǁsimulate__mutmut_9,
        "xǁStudentTǁsimulate__mutmut_10": xǁStudentTǁsimulate__mutmut_10,
        "xǁStudentTǁsimulate__mutmut_11": xǁStudentTǁsimulate__mutmut_11,
        "xǁStudentTǁsimulate__mutmut_12": xǁStudentTǁsimulate__mutmut_12,
        "xǁStudentTǁsimulate__mutmut_13": xǁStudentTǁsimulate__mutmut_13,
    }
    xǁStudentTǁsimulate__mutmut_orig.__name__ = "xǁStudentTǁsimulate"

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 2.0 + np.exp(unconstrained[0])
        return constrained

    def xǁStudentTǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) != 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 2.0 + np.exp(unconstrained[0])
        return constrained

    def xǁStudentTǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 1:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 2.0 + np.exp(unconstrained[0])
        return constrained

    def xǁStudentTǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = None
        constrained[0] = 2.0 + np.exp(unconstrained[0])
        return constrained

    def xǁStudentTǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = None
        return constrained

    def xǁStudentTǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[1] = 2.0 + np.exp(unconstrained[0])
        return constrained

    def xǁStudentTǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 2.0 - np.exp(unconstrained[0])
        return constrained

    def xǁStudentTǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 3.0 + np.exp(unconstrained[0])
        return constrained

    def xǁStudentTǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 2.0 + np.exp(None)
        return constrained

    def xǁStudentTǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 2.0 + np.exp(unconstrained[1])
        return constrained

    xǁStudentTǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁtransform_params__mutmut_1": xǁStudentTǁtransform_params__mutmut_1,
        "xǁStudentTǁtransform_params__mutmut_2": xǁStudentTǁtransform_params__mutmut_2,
        "xǁStudentTǁtransform_params__mutmut_3": xǁStudentTǁtransform_params__mutmut_3,
        "xǁStudentTǁtransform_params__mutmut_4": xǁStudentTǁtransform_params__mutmut_4,
        "xǁStudentTǁtransform_params__mutmut_5": xǁStudentTǁtransform_params__mutmut_5,
        "xǁStudentTǁtransform_params__mutmut_6": xǁStudentTǁtransform_params__mutmut_6,
        "xǁStudentTǁtransform_params__mutmut_7": xǁStudentTǁtransform_params__mutmut_7,
        "xǁStudentTǁtransform_params__mutmut_8": xǁStudentTǁtransform_params__mutmut_8,
        "xǁStudentTǁtransform_params__mutmut_9": xǁStudentTǁtransform_params__mutmut_9,
    }
    xǁStudentTǁtransform_params__mutmut_orig.__name__ = "xǁStudentTǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] - 2.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) != 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] - 2.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 1:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] - 2.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = None
        unconstrained[0] = np.log(max(constrained[0] - 2.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = None
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[1] = np.log(max(constrained[0] - 2.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(None)
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(None, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] - 2.0, None))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(
            max(
                constrained[0] - 2.0,
            )
        )
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] + 2.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[1] - 2.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] - 3.0, 1e-6))
        return unconstrained

    def xǁStudentTǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] - 2.0, 1.000001))
        return unconstrained

    xǁStudentTǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁuntransform_params__mutmut_1": xǁStudentTǁuntransform_params__mutmut_1,
        "xǁStudentTǁuntransform_params__mutmut_2": xǁStudentTǁuntransform_params__mutmut_2,
        "xǁStudentTǁuntransform_params__mutmut_3": xǁStudentTǁuntransform_params__mutmut_3,
        "xǁStudentTǁuntransform_params__mutmut_4": xǁStudentTǁuntransform_params__mutmut_4,
        "xǁStudentTǁuntransform_params__mutmut_5": xǁStudentTǁuntransform_params__mutmut_5,
        "xǁStudentTǁuntransform_params__mutmut_6": xǁStudentTǁuntransform_params__mutmut_6,
        "xǁStudentTǁuntransform_params__mutmut_7": xǁStudentTǁuntransform_params__mutmut_7,
        "xǁStudentTǁuntransform_params__mutmut_8": xǁStudentTǁuntransform_params__mutmut_8,
        "xǁStudentTǁuntransform_params__mutmut_9": xǁStudentTǁuntransform_params__mutmut_9,
        "xǁStudentTǁuntransform_params__mutmut_10": xǁStudentTǁuntransform_params__mutmut_10,
        "xǁStudentTǁuntransform_params__mutmut_11": xǁStudentTǁuntransform_params__mutmut_11,
        "xǁStudentTǁuntransform_params__mutmut_12": xǁStudentTǁuntransform_params__mutmut_12,
        "xǁStudentTǁuntransform_params__mutmut_13": xǁStudentTǁuntransform_params__mutmut_13,
        "xǁStudentTǁuntransform_params__mutmut_14": xǁStudentTǁuntransform_params__mutmut_14,
    }
    xǁStudentTǁuntransform_params__mutmut_orig.__name__ = "xǁStudentTǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStudentTǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁStudentTǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStudentTǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(2.01, 100.0)]

    def xǁStudentTǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is None:
            return []
        return [(2.01, 100.0)]

    def xǁStudentTǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(3.01, 100.0)]

    def xǁStudentTǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(2.01, 101.0)]

    xǁStudentTǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStudentTǁbounds__mutmut_1": xǁStudentTǁbounds__mutmut_1,
        "xǁStudentTǁbounds__mutmut_2": xǁStudentTǁbounds__mutmut_2,
        "xǁStudentTǁbounds__mutmut_3": xǁStudentTǁbounds__mutmut_3,
    }
    xǁStudentTǁbounds__mutmut_orig.__name__ = "xǁStudentTǁbounds"
