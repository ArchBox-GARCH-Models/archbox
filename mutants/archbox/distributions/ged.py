"""GED - Generalized Error Distribution (Nelson, 1991).

f(z; nu) = nu / (lambda * 2^{1+1/nu} * Gamma(1/nu)) * exp(-0.5 * |z/lambda|^nu)

lambda = sqrt(2^{-2/nu} * Gamma(1/nu) / Gamma(3/nu))

Special cases: nu=2 (Normal), nu=1 (Laplace).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, ClassVar

import numpy as np
from numpy.typing import NDArray
from scipy.special import gammainc, gammaincinv, gammaln

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


class GeneralizedError(Distribution):
    """Generalized Error Distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Shape parameter. Must be > 0. If None, estimated from data.
        nu=2 is Normal, nu=1 is Laplace.
    """

    name = "GED"

    def __init__(self, nu: float | None = None) -> None:
        args = [nu]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁ__init____mutmut_orig(self, nu: float | None = None) -> None:
        """Initialize GED distribution with optional shape parameter."""
        self._fixed_nu = nu

    def xǁGeneralizedErrorǁ__init____mutmut_1(self, nu: float | None = None) -> None:
        """Initialize GED distribution with optional shape parameter."""
        self._fixed_nu = None

    xǁGeneralizedErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁ__init____mutmut_1": xǁGeneralizedErrorǁ__init____mutmut_1
    }
    xǁGeneralizedErrorǁ__init____mutmut_orig.__name__ = "xǁGeneralizedErrorǁ__init__"

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
            object.__getattribute__(self, "xǁGeneralizedErrorǁstart_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁstart_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁstart_params__mutmut_orig(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=np.float64)
        return np.array([1.5])  # between Laplace and Normal

    def xǁGeneralizedErrorǁstart_params__mutmut_1(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is None:
            return np.array([], dtype=np.float64)
        return np.array([1.5])  # between Laplace and Normal

    def xǁGeneralizedErrorǁstart_params__mutmut_2(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array(None, dtype=np.float64)
        return np.array([1.5])  # between Laplace and Normal

    def xǁGeneralizedErrorǁstart_params__mutmut_3(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=None)
        return np.array([1.5])  # between Laplace and Normal

    def xǁGeneralizedErrorǁstart_params__mutmut_4(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array(dtype=np.float64)
        return np.array([1.5])  # between Laplace and Normal

    def xǁGeneralizedErrorǁstart_params__mutmut_5(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array(
                [],
            )
        return np.array([1.5])  # between Laplace and Normal

    def xǁGeneralizedErrorǁstart_params__mutmut_6(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=np.float64)
        return np.array(None)  # between Laplace and Normal

    def xǁGeneralizedErrorǁstart_params__mutmut_7(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=np.float64)
        return np.array([2.5])  # between Laplace and Normal

    xǁGeneralizedErrorǁstart_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁstart_params__mutmut_1": xǁGeneralizedErrorǁstart_params__mutmut_1,
        "xǁGeneralizedErrorǁstart_params__mutmut_2": xǁGeneralizedErrorǁstart_params__mutmut_2,
        "xǁGeneralizedErrorǁstart_params__mutmut_3": xǁGeneralizedErrorǁstart_params__mutmut_3,
        "xǁGeneralizedErrorǁstart_params__mutmut_4": xǁGeneralizedErrorǁstart_params__mutmut_4,
        "xǁGeneralizedErrorǁstart_params__mutmut_5": xǁGeneralizedErrorǁstart_params__mutmut_5,
        "xǁGeneralizedErrorǁstart_params__mutmut_6": xǁGeneralizedErrorǁstart_params__mutmut_6,
        "xǁGeneralizedErrorǁstart_params__mutmut_7": xǁGeneralizedErrorǁstart_params__mutmut_7,
    }
    xǁGeneralizedErrorǁstart_params__mutmut_orig.__name__ = "xǁGeneralizedErrorǁstart_params"

    def _get_nu(self, dist_params: NDArray[np.float64] | None = None) -> float:
        args = [dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁ_get_nu__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁ_get_nu__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁ_get_nu__mutmut_orig(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_1(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_2(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = None
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_3(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None or len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_4(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_5(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) >= 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_6(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 1:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_7(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = None
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_8(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(None)
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_9(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[1])
        else:
            nu = 1.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_10(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = None
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_11(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 2.5
        return max(nu, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_12(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(None, 0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_13(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, None)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_14(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(0.1)

    def xǁGeneralizedErrorǁ_get_nu__mutmut_15(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(
            nu,
        )

    def xǁGeneralizedErrorǁ_get_nu__mutmut_16(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 1.1)

    xǁGeneralizedErrorǁ_get_nu__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁ_get_nu__mutmut_1": xǁGeneralizedErrorǁ_get_nu__mutmut_1,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_2": xǁGeneralizedErrorǁ_get_nu__mutmut_2,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_3": xǁGeneralizedErrorǁ_get_nu__mutmut_3,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_4": xǁGeneralizedErrorǁ_get_nu__mutmut_4,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_5": xǁGeneralizedErrorǁ_get_nu__mutmut_5,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_6": xǁGeneralizedErrorǁ_get_nu__mutmut_6,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_7": xǁGeneralizedErrorǁ_get_nu__mutmut_7,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_8": xǁGeneralizedErrorǁ_get_nu__mutmut_8,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_9": xǁGeneralizedErrorǁ_get_nu__mutmut_9,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_10": xǁGeneralizedErrorǁ_get_nu__mutmut_10,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_11": xǁGeneralizedErrorǁ_get_nu__mutmut_11,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_12": xǁGeneralizedErrorǁ_get_nu__mutmut_12,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_13": xǁGeneralizedErrorǁ_get_nu__mutmut_13,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_14": xǁGeneralizedErrorǁ_get_nu__mutmut_14,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_15": xǁGeneralizedErrorǁ_get_nu__mutmut_15,
        "xǁGeneralizedErrorǁ_get_nu__mutmut_16": xǁGeneralizedErrorǁ_get_nu__mutmut_16,
    }
    xǁGeneralizedErrorǁ_get_nu__mutmut_orig.__name__ = "xǁGeneralizedErrorǁ_get_nu"

    @staticmethod
    def _lambda_ged(nu: float) -> float:
        """Compute the GED scale parameter lambda.

        lambda = sqrt(2^{-2/nu} * Gamma(1/nu) / Gamma(3/nu))
        """
        return float(np.sqrt(2 ** (-2.0 / nu) * np.exp(gammaln(1.0 / nu) - gammaln(3.0 / nu))))

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [resids, sigma2, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁloglikelihood__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁloglikelihood__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁloglikelihood__mutmut_orig(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_1(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = None
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_2(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(None)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_3(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = None
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_4(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(None)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_5(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = None

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_6(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids * np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_7(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(None)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_8(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = None
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_9(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            + 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_10(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            + 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_11(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            + gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_12(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            + (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_13(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            + np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_14(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(None)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_15(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(None)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_16(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) / np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_17(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 - 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_18(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (2 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_19(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 * nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_20(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 2.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_21(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(None)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_22(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(3)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_23(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(None)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_24(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 * nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_25(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(2.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_26(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 / np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_27(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 1.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_28(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) * nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_29(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(None) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_30(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z * lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_31(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 / np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_32(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 1.5 * np.log(sigma2)
        )
        return ll

    def xǁGeneralizedErrorǁloglikelihood__mutmut_33(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(None)
        )
        return ll

    xǁGeneralizedErrorǁloglikelihood__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁloglikelihood__mutmut_1": xǁGeneralizedErrorǁloglikelihood__mutmut_1,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_2": xǁGeneralizedErrorǁloglikelihood__mutmut_2,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_3": xǁGeneralizedErrorǁloglikelihood__mutmut_3,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_4": xǁGeneralizedErrorǁloglikelihood__mutmut_4,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_5": xǁGeneralizedErrorǁloglikelihood__mutmut_5,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_6": xǁGeneralizedErrorǁloglikelihood__mutmut_6,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_7": xǁGeneralizedErrorǁloglikelihood__mutmut_7,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_8": xǁGeneralizedErrorǁloglikelihood__mutmut_8,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_9": xǁGeneralizedErrorǁloglikelihood__mutmut_9,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_10": xǁGeneralizedErrorǁloglikelihood__mutmut_10,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_11": xǁGeneralizedErrorǁloglikelihood__mutmut_11,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_12": xǁGeneralizedErrorǁloglikelihood__mutmut_12,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_13": xǁGeneralizedErrorǁloglikelihood__mutmut_13,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_14": xǁGeneralizedErrorǁloglikelihood__mutmut_14,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_15": xǁGeneralizedErrorǁloglikelihood__mutmut_15,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_16": xǁGeneralizedErrorǁloglikelihood__mutmut_16,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_17": xǁGeneralizedErrorǁloglikelihood__mutmut_17,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_18": xǁGeneralizedErrorǁloglikelihood__mutmut_18,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_19": xǁGeneralizedErrorǁloglikelihood__mutmut_19,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_20": xǁGeneralizedErrorǁloglikelihood__mutmut_20,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_21": xǁGeneralizedErrorǁloglikelihood__mutmut_21,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_22": xǁGeneralizedErrorǁloglikelihood__mutmut_22,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_23": xǁGeneralizedErrorǁloglikelihood__mutmut_23,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_24": xǁGeneralizedErrorǁloglikelihood__mutmut_24,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_25": xǁGeneralizedErrorǁloglikelihood__mutmut_25,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_26": xǁGeneralizedErrorǁloglikelihood__mutmut_26,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_27": xǁGeneralizedErrorǁloglikelihood__mutmut_27,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_28": xǁGeneralizedErrorǁloglikelihood__mutmut_28,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_29": xǁGeneralizedErrorǁloglikelihood__mutmut_29,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_30": xǁGeneralizedErrorǁloglikelihood__mutmut_30,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_31": xǁGeneralizedErrorǁloglikelihood__mutmut_31,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_32": xǁGeneralizedErrorǁloglikelihood__mutmut_32,
        "xǁGeneralizedErrorǁloglikelihood__mutmut_33": xǁGeneralizedErrorǁloglikelihood__mutmut_33,
    }
    xǁGeneralizedErrorǁloglikelihood__mutmut_orig.__name__ = "xǁGeneralizedErrorǁloglikelihood"

    def ppf(self, q: float) -> float:
        args = [q]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁppf__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁppf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁppf__mutmut_orig(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_1(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_2(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = None

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_3(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(None)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_4(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q <= 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_5(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 1.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_6(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = None
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_7(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 + 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_8(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 2.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_9(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 / q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_10(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 3.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_11(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = None
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_12(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(None)
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_13(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(None, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_14(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, None))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_15(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_16(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(
                gammaincinv(
                    1.0 / nu,
                )
            )
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_17(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 * nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_18(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(2.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_19(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = None
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_20(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam / (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_21(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) * (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_22(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 / val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_23(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (3.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_24(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 * nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_25(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (2.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_26(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return +x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_27(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q >= 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_28(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 1.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_29(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = None
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_30(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q + 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_31(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 / q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_32(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 3.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_33(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 2.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_34(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = None
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_35(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(None)
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_36(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(None, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_37(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, None))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_38(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_39(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(
                gammaincinv(
                    1.0 / nu,
                )
            )
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_40(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 * nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_41(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(2.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_42(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = None
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_43(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam / (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_44(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) * (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_45(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 / val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_46(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (3.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_47(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 * nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_48(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (2.0 / nu)
            return float(x)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_49(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(None)
        else:
            return 0.0

    def xǁGeneralizedErrorǁppf__mutmut_50(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 1.0

    xǁGeneralizedErrorǁppf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁppf__mutmut_1": xǁGeneralizedErrorǁppf__mutmut_1,
        "xǁGeneralizedErrorǁppf__mutmut_2": xǁGeneralizedErrorǁppf__mutmut_2,
        "xǁGeneralizedErrorǁppf__mutmut_3": xǁGeneralizedErrorǁppf__mutmut_3,
        "xǁGeneralizedErrorǁppf__mutmut_4": xǁGeneralizedErrorǁppf__mutmut_4,
        "xǁGeneralizedErrorǁppf__mutmut_5": xǁGeneralizedErrorǁppf__mutmut_5,
        "xǁGeneralizedErrorǁppf__mutmut_6": xǁGeneralizedErrorǁppf__mutmut_6,
        "xǁGeneralizedErrorǁppf__mutmut_7": xǁGeneralizedErrorǁppf__mutmut_7,
        "xǁGeneralizedErrorǁppf__mutmut_8": xǁGeneralizedErrorǁppf__mutmut_8,
        "xǁGeneralizedErrorǁppf__mutmut_9": xǁGeneralizedErrorǁppf__mutmut_9,
        "xǁGeneralizedErrorǁppf__mutmut_10": xǁGeneralizedErrorǁppf__mutmut_10,
        "xǁGeneralizedErrorǁppf__mutmut_11": xǁGeneralizedErrorǁppf__mutmut_11,
        "xǁGeneralizedErrorǁppf__mutmut_12": xǁGeneralizedErrorǁppf__mutmut_12,
        "xǁGeneralizedErrorǁppf__mutmut_13": xǁGeneralizedErrorǁppf__mutmut_13,
        "xǁGeneralizedErrorǁppf__mutmut_14": xǁGeneralizedErrorǁppf__mutmut_14,
        "xǁGeneralizedErrorǁppf__mutmut_15": xǁGeneralizedErrorǁppf__mutmut_15,
        "xǁGeneralizedErrorǁppf__mutmut_16": xǁGeneralizedErrorǁppf__mutmut_16,
        "xǁGeneralizedErrorǁppf__mutmut_17": xǁGeneralizedErrorǁppf__mutmut_17,
        "xǁGeneralizedErrorǁppf__mutmut_18": xǁGeneralizedErrorǁppf__mutmut_18,
        "xǁGeneralizedErrorǁppf__mutmut_19": xǁGeneralizedErrorǁppf__mutmut_19,
        "xǁGeneralizedErrorǁppf__mutmut_20": xǁGeneralizedErrorǁppf__mutmut_20,
        "xǁGeneralizedErrorǁppf__mutmut_21": xǁGeneralizedErrorǁppf__mutmut_21,
        "xǁGeneralizedErrorǁppf__mutmut_22": xǁGeneralizedErrorǁppf__mutmut_22,
        "xǁGeneralizedErrorǁppf__mutmut_23": xǁGeneralizedErrorǁppf__mutmut_23,
        "xǁGeneralizedErrorǁppf__mutmut_24": xǁGeneralizedErrorǁppf__mutmut_24,
        "xǁGeneralizedErrorǁppf__mutmut_25": xǁGeneralizedErrorǁppf__mutmut_25,
        "xǁGeneralizedErrorǁppf__mutmut_26": xǁGeneralizedErrorǁppf__mutmut_26,
        "xǁGeneralizedErrorǁppf__mutmut_27": xǁGeneralizedErrorǁppf__mutmut_27,
        "xǁGeneralizedErrorǁppf__mutmut_28": xǁGeneralizedErrorǁppf__mutmut_28,
        "xǁGeneralizedErrorǁppf__mutmut_29": xǁGeneralizedErrorǁppf__mutmut_29,
        "xǁGeneralizedErrorǁppf__mutmut_30": xǁGeneralizedErrorǁppf__mutmut_30,
        "xǁGeneralizedErrorǁppf__mutmut_31": xǁGeneralizedErrorǁppf__mutmut_31,
        "xǁGeneralizedErrorǁppf__mutmut_32": xǁGeneralizedErrorǁppf__mutmut_32,
        "xǁGeneralizedErrorǁppf__mutmut_33": xǁGeneralizedErrorǁppf__mutmut_33,
        "xǁGeneralizedErrorǁppf__mutmut_34": xǁGeneralizedErrorǁppf__mutmut_34,
        "xǁGeneralizedErrorǁppf__mutmut_35": xǁGeneralizedErrorǁppf__mutmut_35,
        "xǁGeneralizedErrorǁppf__mutmut_36": xǁGeneralizedErrorǁppf__mutmut_36,
        "xǁGeneralizedErrorǁppf__mutmut_37": xǁGeneralizedErrorǁppf__mutmut_37,
        "xǁGeneralizedErrorǁppf__mutmut_38": xǁGeneralizedErrorǁppf__mutmut_38,
        "xǁGeneralizedErrorǁppf__mutmut_39": xǁGeneralizedErrorǁppf__mutmut_39,
        "xǁGeneralizedErrorǁppf__mutmut_40": xǁGeneralizedErrorǁppf__mutmut_40,
        "xǁGeneralizedErrorǁppf__mutmut_41": xǁGeneralizedErrorǁppf__mutmut_41,
        "xǁGeneralizedErrorǁppf__mutmut_42": xǁGeneralizedErrorǁppf__mutmut_42,
        "xǁGeneralizedErrorǁppf__mutmut_43": xǁGeneralizedErrorǁppf__mutmut_43,
        "xǁGeneralizedErrorǁppf__mutmut_44": xǁGeneralizedErrorǁppf__mutmut_44,
        "xǁGeneralizedErrorǁppf__mutmut_45": xǁGeneralizedErrorǁppf__mutmut_45,
        "xǁGeneralizedErrorǁppf__mutmut_46": xǁGeneralizedErrorǁppf__mutmut_46,
        "xǁGeneralizedErrorǁppf__mutmut_47": xǁGeneralizedErrorǁppf__mutmut_47,
        "xǁGeneralizedErrorǁppf__mutmut_48": xǁGeneralizedErrorǁppf__mutmut_48,
        "xǁGeneralizedErrorǁppf__mutmut_49": xǁGeneralizedErrorǁppf__mutmut_49,
        "xǁGeneralizedErrorǁppf__mutmut_50": xǁGeneralizedErrorǁppf__mutmut_50,
    }
    xǁGeneralizedErrorǁppf__mutmut_orig.__name__ = "xǁGeneralizedErrorǁppf"

    def cdf(self, x: float) -> float:
        args = [x]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁcdf__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁcdf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁcdf__mutmut_orig(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_1(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_2(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = None

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_3(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(None)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_4(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = None
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_5(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 / np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_6(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 1.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_7(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) * nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_8(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(None) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_9(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x * lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_10(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = None

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_11(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(None)

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_12(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(None, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_13(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, None))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_14(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_15(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(
            gammainc(
                1.0 / nu,
            )
        )

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_16(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 * nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_17(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(2.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_18(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x > 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_19(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 1:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_20(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 / (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_21(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 1.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_22(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 - g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_23(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (2.0 + g)
        else:
            return 0.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_24(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 / (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_25(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 1.5 * (1.0 - g)

    def xǁGeneralizedErrorǁcdf__mutmut_26(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 + g)

    def xǁGeneralizedErrorǁcdf__mutmut_27(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (2.0 - g)

    xǁGeneralizedErrorǁcdf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁcdf__mutmut_1": xǁGeneralizedErrorǁcdf__mutmut_1,
        "xǁGeneralizedErrorǁcdf__mutmut_2": xǁGeneralizedErrorǁcdf__mutmut_2,
        "xǁGeneralizedErrorǁcdf__mutmut_3": xǁGeneralizedErrorǁcdf__mutmut_3,
        "xǁGeneralizedErrorǁcdf__mutmut_4": xǁGeneralizedErrorǁcdf__mutmut_4,
        "xǁGeneralizedErrorǁcdf__mutmut_5": xǁGeneralizedErrorǁcdf__mutmut_5,
        "xǁGeneralizedErrorǁcdf__mutmut_6": xǁGeneralizedErrorǁcdf__mutmut_6,
        "xǁGeneralizedErrorǁcdf__mutmut_7": xǁGeneralizedErrorǁcdf__mutmut_7,
        "xǁGeneralizedErrorǁcdf__mutmut_8": xǁGeneralizedErrorǁcdf__mutmut_8,
        "xǁGeneralizedErrorǁcdf__mutmut_9": xǁGeneralizedErrorǁcdf__mutmut_9,
        "xǁGeneralizedErrorǁcdf__mutmut_10": xǁGeneralizedErrorǁcdf__mutmut_10,
        "xǁGeneralizedErrorǁcdf__mutmut_11": xǁGeneralizedErrorǁcdf__mutmut_11,
        "xǁGeneralizedErrorǁcdf__mutmut_12": xǁGeneralizedErrorǁcdf__mutmut_12,
        "xǁGeneralizedErrorǁcdf__mutmut_13": xǁGeneralizedErrorǁcdf__mutmut_13,
        "xǁGeneralizedErrorǁcdf__mutmut_14": xǁGeneralizedErrorǁcdf__mutmut_14,
        "xǁGeneralizedErrorǁcdf__mutmut_15": xǁGeneralizedErrorǁcdf__mutmut_15,
        "xǁGeneralizedErrorǁcdf__mutmut_16": xǁGeneralizedErrorǁcdf__mutmut_16,
        "xǁGeneralizedErrorǁcdf__mutmut_17": xǁGeneralizedErrorǁcdf__mutmut_17,
        "xǁGeneralizedErrorǁcdf__mutmut_18": xǁGeneralizedErrorǁcdf__mutmut_18,
        "xǁGeneralizedErrorǁcdf__mutmut_19": xǁGeneralizedErrorǁcdf__mutmut_19,
        "xǁGeneralizedErrorǁcdf__mutmut_20": xǁGeneralizedErrorǁcdf__mutmut_20,
        "xǁGeneralizedErrorǁcdf__mutmut_21": xǁGeneralizedErrorǁcdf__mutmut_21,
        "xǁGeneralizedErrorǁcdf__mutmut_22": xǁGeneralizedErrorǁcdf__mutmut_22,
        "xǁGeneralizedErrorǁcdf__mutmut_23": xǁGeneralizedErrorǁcdf__mutmut_23,
        "xǁGeneralizedErrorǁcdf__mutmut_24": xǁGeneralizedErrorǁcdf__mutmut_24,
        "xǁGeneralizedErrorǁcdf__mutmut_25": xǁGeneralizedErrorǁcdf__mutmut_25,
        "xǁGeneralizedErrorǁcdf__mutmut_26": xǁGeneralizedErrorǁcdf__mutmut_26,
        "xǁGeneralizedErrorǁcdf__mutmut_27": xǁGeneralizedErrorǁcdf__mutmut_27,
    }
    xǁGeneralizedErrorǁcdf__mutmut_orig.__name__ = "xǁGeneralizedErrorǁcdf"

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [n, rng, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁsimulate__mutmut_orig(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_1(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = None
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_2(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(None)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_3(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = None

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_4(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(None)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_5(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = None
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_6(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(None, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_7(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=None, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_8(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=None)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_9(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_10(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_11(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(
            1.0 / nu,
            scale=1.0,
        )
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_12(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 * nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_13(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(2.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_14(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=2.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_15(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = None
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_16(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) + 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_17(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 / rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_18(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 3 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_19(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(None, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_20(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, None, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_21(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=None) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_22(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_23(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_24(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = (
            2
            * rng.integers(
                0,
                2,
            )
            - 1
        )
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_25(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(1, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_26(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 3, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_27(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 2
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_28(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = None

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_29(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) / lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_30(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs / (2 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_31(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) * (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_32(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 / u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_33(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (3 * u) ** (1.0 / nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_34(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 * nu) * lam

        return z

    def xǁGeneralizedErrorǁsimulate__mutmut_35(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (2.0 / nu) * lam

        return z

    xǁGeneralizedErrorǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁsimulate__mutmut_1": xǁGeneralizedErrorǁsimulate__mutmut_1,
        "xǁGeneralizedErrorǁsimulate__mutmut_2": xǁGeneralizedErrorǁsimulate__mutmut_2,
        "xǁGeneralizedErrorǁsimulate__mutmut_3": xǁGeneralizedErrorǁsimulate__mutmut_3,
        "xǁGeneralizedErrorǁsimulate__mutmut_4": xǁGeneralizedErrorǁsimulate__mutmut_4,
        "xǁGeneralizedErrorǁsimulate__mutmut_5": xǁGeneralizedErrorǁsimulate__mutmut_5,
        "xǁGeneralizedErrorǁsimulate__mutmut_6": xǁGeneralizedErrorǁsimulate__mutmut_6,
        "xǁGeneralizedErrorǁsimulate__mutmut_7": xǁGeneralizedErrorǁsimulate__mutmut_7,
        "xǁGeneralizedErrorǁsimulate__mutmut_8": xǁGeneralizedErrorǁsimulate__mutmut_8,
        "xǁGeneralizedErrorǁsimulate__mutmut_9": xǁGeneralizedErrorǁsimulate__mutmut_9,
        "xǁGeneralizedErrorǁsimulate__mutmut_10": xǁGeneralizedErrorǁsimulate__mutmut_10,
        "xǁGeneralizedErrorǁsimulate__mutmut_11": xǁGeneralizedErrorǁsimulate__mutmut_11,
        "xǁGeneralizedErrorǁsimulate__mutmut_12": xǁGeneralizedErrorǁsimulate__mutmut_12,
        "xǁGeneralizedErrorǁsimulate__mutmut_13": xǁGeneralizedErrorǁsimulate__mutmut_13,
        "xǁGeneralizedErrorǁsimulate__mutmut_14": xǁGeneralizedErrorǁsimulate__mutmut_14,
        "xǁGeneralizedErrorǁsimulate__mutmut_15": xǁGeneralizedErrorǁsimulate__mutmut_15,
        "xǁGeneralizedErrorǁsimulate__mutmut_16": xǁGeneralizedErrorǁsimulate__mutmut_16,
        "xǁGeneralizedErrorǁsimulate__mutmut_17": xǁGeneralizedErrorǁsimulate__mutmut_17,
        "xǁGeneralizedErrorǁsimulate__mutmut_18": xǁGeneralizedErrorǁsimulate__mutmut_18,
        "xǁGeneralizedErrorǁsimulate__mutmut_19": xǁGeneralizedErrorǁsimulate__mutmut_19,
        "xǁGeneralizedErrorǁsimulate__mutmut_20": xǁGeneralizedErrorǁsimulate__mutmut_20,
        "xǁGeneralizedErrorǁsimulate__mutmut_21": xǁGeneralizedErrorǁsimulate__mutmut_21,
        "xǁGeneralizedErrorǁsimulate__mutmut_22": xǁGeneralizedErrorǁsimulate__mutmut_22,
        "xǁGeneralizedErrorǁsimulate__mutmut_23": xǁGeneralizedErrorǁsimulate__mutmut_23,
        "xǁGeneralizedErrorǁsimulate__mutmut_24": xǁGeneralizedErrorǁsimulate__mutmut_24,
        "xǁGeneralizedErrorǁsimulate__mutmut_25": xǁGeneralizedErrorǁsimulate__mutmut_25,
        "xǁGeneralizedErrorǁsimulate__mutmut_26": xǁGeneralizedErrorǁsimulate__mutmut_26,
        "xǁGeneralizedErrorǁsimulate__mutmut_27": xǁGeneralizedErrorǁsimulate__mutmut_27,
        "xǁGeneralizedErrorǁsimulate__mutmut_28": xǁGeneralizedErrorǁsimulate__mutmut_28,
        "xǁGeneralizedErrorǁsimulate__mutmut_29": xǁGeneralizedErrorǁsimulate__mutmut_29,
        "xǁGeneralizedErrorǁsimulate__mutmut_30": xǁGeneralizedErrorǁsimulate__mutmut_30,
        "xǁGeneralizedErrorǁsimulate__mutmut_31": xǁGeneralizedErrorǁsimulate__mutmut_31,
        "xǁGeneralizedErrorǁsimulate__mutmut_32": xǁGeneralizedErrorǁsimulate__mutmut_32,
        "xǁGeneralizedErrorǁsimulate__mutmut_33": xǁGeneralizedErrorǁsimulate__mutmut_33,
        "xǁGeneralizedErrorǁsimulate__mutmut_34": xǁGeneralizedErrorǁsimulate__mutmut_34,
        "xǁGeneralizedErrorǁsimulate__mutmut_35": xǁGeneralizedErrorǁsimulate__mutmut_35,
    }
    xǁGeneralizedErrorǁsimulate__mutmut_orig.__name__ = "xǁGeneralizedErrorǁsimulate"

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = np.exp(unconstrained[0])
        return constrained

    def xǁGeneralizedErrorǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) != 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = np.exp(unconstrained[0])
        return constrained

    def xǁGeneralizedErrorǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 1:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = np.exp(unconstrained[0])
        return constrained

    def xǁGeneralizedErrorǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = None
        constrained[0] = np.exp(unconstrained[0])
        return constrained

    def xǁGeneralizedErrorǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = None
        return constrained

    def xǁGeneralizedErrorǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[1] = np.exp(unconstrained[0])
        return constrained

    def xǁGeneralizedErrorǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = np.exp(None)
        return constrained

    def xǁGeneralizedErrorǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = np.exp(unconstrained[1])
        return constrained

    xǁGeneralizedErrorǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁtransform_params__mutmut_1": xǁGeneralizedErrorǁtransform_params__mutmut_1,
        "xǁGeneralizedErrorǁtransform_params__mutmut_2": xǁGeneralizedErrorǁtransform_params__mutmut_2,
        "xǁGeneralizedErrorǁtransform_params__mutmut_3": xǁGeneralizedErrorǁtransform_params__mutmut_3,
        "xǁGeneralizedErrorǁtransform_params__mutmut_4": xǁGeneralizedErrorǁtransform_params__mutmut_4,
        "xǁGeneralizedErrorǁtransform_params__mutmut_5": xǁGeneralizedErrorǁtransform_params__mutmut_5,
        "xǁGeneralizedErrorǁtransform_params__mutmut_6": xǁGeneralizedErrorǁtransform_params__mutmut_6,
        "xǁGeneralizedErrorǁtransform_params__mutmut_7": xǁGeneralizedErrorǁtransform_params__mutmut_7,
    }
    xǁGeneralizedErrorǁtransform_params__mutmut_orig.__name__ = (
        "xǁGeneralizedErrorǁtransform_params"
    )

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) != 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 1:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = None
        unconstrained[0] = np.log(max(constrained[0], 1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = None
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[1] = np.log(max(constrained[0], 1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(None)
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(None, 1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], None))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(
            max(
                constrained[0],
            )
        )
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[1], 1e-6))
        return unconstrained

    def xǁGeneralizedErrorǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1.000001))
        return unconstrained

    xǁGeneralizedErrorǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁuntransform_params__mutmut_1": xǁGeneralizedErrorǁuntransform_params__mutmut_1,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_2": xǁGeneralizedErrorǁuntransform_params__mutmut_2,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_3": xǁGeneralizedErrorǁuntransform_params__mutmut_3,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_4": xǁGeneralizedErrorǁuntransform_params__mutmut_4,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_5": xǁGeneralizedErrorǁuntransform_params__mutmut_5,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_6": xǁGeneralizedErrorǁuntransform_params__mutmut_6,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_7": xǁGeneralizedErrorǁuntransform_params__mutmut_7,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_8": xǁGeneralizedErrorǁuntransform_params__mutmut_8,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_9": xǁGeneralizedErrorǁuntransform_params__mutmut_9,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_10": xǁGeneralizedErrorǁuntransform_params__mutmut_10,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_11": xǁGeneralizedErrorǁuntransform_params__mutmut_11,
        "xǁGeneralizedErrorǁuntransform_params__mutmut_12": xǁGeneralizedErrorǁuntransform_params__mutmut_12,
    }
    xǁGeneralizedErrorǁuntransform_params__mutmut_orig.__name__ = (
        "xǁGeneralizedErrorǁuntransform_params"
    )

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGeneralizedErrorǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁGeneralizedErrorǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGeneralizedErrorǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(0.1, 20.0)]

    def xǁGeneralizedErrorǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is None:
            return []
        return [(0.1, 20.0)]

    def xǁGeneralizedErrorǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(1.1, 20.0)]

    def xǁGeneralizedErrorǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(0.1, 21.0)]

    xǁGeneralizedErrorǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGeneralizedErrorǁbounds__mutmut_1": xǁGeneralizedErrorǁbounds__mutmut_1,
        "xǁGeneralizedErrorǁbounds__mutmut_2": xǁGeneralizedErrorǁbounds__mutmut_2,
        "xǁGeneralizedErrorǁbounds__mutmut_3": xǁGeneralizedErrorǁbounds__mutmut_3,
    }
    xǁGeneralizedErrorǁbounds__mutmut_orig.__name__ = "xǁGeneralizedErrorǁbounds"
