"""Skewed Student-t distribution (Hansen, 1994).

f(z; nu, lambda) = {
    b*c*(1 + 1/(nu-2) * ((b*z+a)/(1-lambda))^2)^{-(nu+1)/2}  if z < -a/b
    b*c*(1 + 1/(nu-2) * ((b*z+a)/(1+lambda))^2)^{-(nu+1)/2}  if z >= -a/b
}

where:
    a = 4*lambda*c*(nu-2)/(nu-1)
    b^2 = 1 + 3*lambda^2 - a^2
    c = Gamma((nu+1)/2) / (sqrt(pi*(nu-2)) * Gamma(nu/2))
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, ClassVar

import numpy as np
from numpy.typing import NDArray
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


class SkewedT(Distribution):
    """Skewed Student-t distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Degrees of freedom. Must be > 2.
    lam : float, optional
        Skewness parameter. Must be in (-1, 1).
    """

    name = "Skewed Student-t"

    def __init__(self, nu: float | None = None, lam: float | None = None) -> None:
        args = [nu, lam]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁ__init____mutmut_orig(
        self, nu: float | None = None, lam: float | None = None
    ) -> None:
        """Initialize Skewed Student-t distribution with optional parameters."""
        self._fixed_nu = nu
        self._fixed_lam = lam

    def xǁSkewedTǁ__init____mutmut_1(
        self, nu: float | None = None, lam: float | None = None
    ) -> None:
        """Initialize Skewed Student-t distribution with optional parameters."""
        self._fixed_nu = None
        self._fixed_lam = lam

    def xǁSkewedTǁ__init____mutmut_2(
        self, nu: float | None = None, lam: float | None = None
    ) -> None:
        """Initialize Skewed Student-t distribution with optional parameters."""
        self._fixed_nu = nu
        self._fixed_lam = None

    xǁSkewedTǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁ__init____mutmut_1": xǁSkewedTǁ__init____mutmut_1,
        "xǁSkewedTǁ__init____mutmut_2": xǁSkewedTǁ__init____mutmut_2,
    }
    xǁSkewedTǁ__init____mutmut_orig.__name__ = "xǁSkewedTǁ__init__"

    @property
    def num_params(self) -> int:
        """Number of distribution shape parameters."""
        count = 0
        if self._fixed_nu is None:
            count += 1
        if self._fixed_lam is None:
            count += 1
        return count

    @property
    def param_names(self) -> list[str]:
        """Distribution parameter names."""
        names: list[str] = []
        if self._fixed_nu is None:
            names.append("nu")
        if self._fixed_lam is None:
            names.append("lambda")
        return names

    def start_params(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁstart_params__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁstart_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁstart_params__mutmut_orig(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_1(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = None
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_2(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is not None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_3(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(None)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_4(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(9.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_5(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is not None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_6(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(None)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_7(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(+0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_8(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-1.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_9(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(None, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_10(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=None) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_11(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_12(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return (
            np.array(
                params,
            )
            if params
            else np.array([], dtype=np.float64)
        )

    def xǁSkewedTǁstart_params__mutmut_13(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array(None, dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_14(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=None)

    def xǁSkewedTǁstart_params__mutmut_15(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array(dtype=np.float64)

    def xǁSkewedTǁstart_params__mutmut_16(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return (
            np.array(params, dtype=np.float64)
            if params
            else np.array(
                [],
            )
        )

    xǁSkewedTǁstart_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁstart_params__mutmut_1": xǁSkewedTǁstart_params__mutmut_1,
        "xǁSkewedTǁstart_params__mutmut_2": xǁSkewedTǁstart_params__mutmut_2,
        "xǁSkewedTǁstart_params__mutmut_3": xǁSkewedTǁstart_params__mutmut_3,
        "xǁSkewedTǁstart_params__mutmut_4": xǁSkewedTǁstart_params__mutmut_4,
        "xǁSkewedTǁstart_params__mutmut_5": xǁSkewedTǁstart_params__mutmut_5,
        "xǁSkewedTǁstart_params__mutmut_6": xǁSkewedTǁstart_params__mutmut_6,
        "xǁSkewedTǁstart_params__mutmut_7": xǁSkewedTǁstart_params__mutmut_7,
        "xǁSkewedTǁstart_params__mutmut_8": xǁSkewedTǁstart_params__mutmut_8,
        "xǁSkewedTǁstart_params__mutmut_9": xǁSkewedTǁstart_params__mutmut_9,
        "xǁSkewedTǁstart_params__mutmut_10": xǁSkewedTǁstart_params__mutmut_10,
        "xǁSkewedTǁstart_params__mutmut_11": xǁSkewedTǁstart_params__mutmut_11,
        "xǁSkewedTǁstart_params__mutmut_12": xǁSkewedTǁstart_params__mutmut_12,
        "xǁSkewedTǁstart_params__mutmut_13": xǁSkewedTǁstart_params__mutmut_13,
        "xǁSkewedTǁstart_params__mutmut_14": xǁSkewedTǁstart_params__mutmut_14,
        "xǁSkewedTǁstart_params__mutmut_15": xǁSkewedTǁstart_params__mutmut_15,
        "xǁSkewedTǁstart_params__mutmut_16": xǁSkewedTǁstart_params__mutmut_16,
    }
    xǁSkewedTǁstart_params__mutmut_orig.__name__ = "xǁSkewedTǁstart_params"

    def _get_nu_lam(self, dist_params: NDArray[np.float64] | None = None) -> tuple[float, float]:
        args = [dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁ_get_nu_lam__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁ_get_nu_lam__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁ_get_nu_lam__mutmut_orig(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_1(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = None
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_2(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 1
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_3(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_4(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = None
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_5(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None or idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_6(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_7(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx <= len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_8(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = None
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_9(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(None)
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_10(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx = 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_11(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx -= 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_12(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 2
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_13(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = None

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_14(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 9.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_15(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_16(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = None
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_17(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None or idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_18(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_19(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx <= len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_20(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = None
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_21(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(None)
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_22(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = None

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_23(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 1.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_24(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = None
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_25(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(None, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_26(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, None)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_27(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_28(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(
            nu,
        )
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_29(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 3.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_30(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = None
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_31(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(None)
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_32(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(None, -0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_33(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, None, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_34(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, None))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_35(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(-0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_36(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_37(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(
            np.clip(
                lam,
                -0.999,
            )
        )
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_38(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, +0.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_39(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -1.999, 0.999))
        return nu, lam

    def xǁSkewedTǁ_get_nu_lam__mutmut_40(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 1.999))
        return nu, lam

    xǁSkewedTǁ_get_nu_lam__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁ_get_nu_lam__mutmut_1": xǁSkewedTǁ_get_nu_lam__mutmut_1,
        "xǁSkewedTǁ_get_nu_lam__mutmut_2": xǁSkewedTǁ_get_nu_lam__mutmut_2,
        "xǁSkewedTǁ_get_nu_lam__mutmut_3": xǁSkewedTǁ_get_nu_lam__mutmut_3,
        "xǁSkewedTǁ_get_nu_lam__mutmut_4": xǁSkewedTǁ_get_nu_lam__mutmut_4,
        "xǁSkewedTǁ_get_nu_lam__mutmut_5": xǁSkewedTǁ_get_nu_lam__mutmut_5,
        "xǁSkewedTǁ_get_nu_lam__mutmut_6": xǁSkewedTǁ_get_nu_lam__mutmut_6,
        "xǁSkewedTǁ_get_nu_lam__mutmut_7": xǁSkewedTǁ_get_nu_lam__mutmut_7,
        "xǁSkewedTǁ_get_nu_lam__mutmut_8": xǁSkewedTǁ_get_nu_lam__mutmut_8,
        "xǁSkewedTǁ_get_nu_lam__mutmut_9": xǁSkewedTǁ_get_nu_lam__mutmut_9,
        "xǁSkewedTǁ_get_nu_lam__mutmut_10": xǁSkewedTǁ_get_nu_lam__mutmut_10,
        "xǁSkewedTǁ_get_nu_lam__mutmut_11": xǁSkewedTǁ_get_nu_lam__mutmut_11,
        "xǁSkewedTǁ_get_nu_lam__mutmut_12": xǁSkewedTǁ_get_nu_lam__mutmut_12,
        "xǁSkewedTǁ_get_nu_lam__mutmut_13": xǁSkewedTǁ_get_nu_lam__mutmut_13,
        "xǁSkewedTǁ_get_nu_lam__mutmut_14": xǁSkewedTǁ_get_nu_lam__mutmut_14,
        "xǁSkewedTǁ_get_nu_lam__mutmut_15": xǁSkewedTǁ_get_nu_lam__mutmut_15,
        "xǁSkewedTǁ_get_nu_lam__mutmut_16": xǁSkewedTǁ_get_nu_lam__mutmut_16,
        "xǁSkewedTǁ_get_nu_lam__mutmut_17": xǁSkewedTǁ_get_nu_lam__mutmut_17,
        "xǁSkewedTǁ_get_nu_lam__mutmut_18": xǁSkewedTǁ_get_nu_lam__mutmut_18,
        "xǁSkewedTǁ_get_nu_lam__mutmut_19": xǁSkewedTǁ_get_nu_lam__mutmut_19,
        "xǁSkewedTǁ_get_nu_lam__mutmut_20": xǁSkewedTǁ_get_nu_lam__mutmut_20,
        "xǁSkewedTǁ_get_nu_lam__mutmut_21": xǁSkewedTǁ_get_nu_lam__mutmut_21,
        "xǁSkewedTǁ_get_nu_lam__mutmut_22": xǁSkewedTǁ_get_nu_lam__mutmut_22,
        "xǁSkewedTǁ_get_nu_lam__mutmut_23": xǁSkewedTǁ_get_nu_lam__mutmut_23,
        "xǁSkewedTǁ_get_nu_lam__mutmut_24": xǁSkewedTǁ_get_nu_lam__mutmut_24,
        "xǁSkewedTǁ_get_nu_lam__mutmut_25": xǁSkewedTǁ_get_nu_lam__mutmut_25,
        "xǁSkewedTǁ_get_nu_lam__mutmut_26": xǁSkewedTǁ_get_nu_lam__mutmut_26,
        "xǁSkewedTǁ_get_nu_lam__mutmut_27": xǁSkewedTǁ_get_nu_lam__mutmut_27,
        "xǁSkewedTǁ_get_nu_lam__mutmut_28": xǁSkewedTǁ_get_nu_lam__mutmut_28,
        "xǁSkewedTǁ_get_nu_lam__mutmut_29": xǁSkewedTǁ_get_nu_lam__mutmut_29,
        "xǁSkewedTǁ_get_nu_lam__mutmut_30": xǁSkewedTǁ_get_nu_lam__mutmut_30,
        "xǁSkewedTǁ_get_nu_lam__mutmut_31": xǁSkewedTǁ_get_nu_lam__mutmut_31,
        "xǁSkewedTǁ_get_nu_lam__mutmut_32": xǁSkewedTǁ_get_nu_lam__mutmut_32,
        "xǁSkewedTǁ_get_nu_lam__mutmut_33": xǁSkewedTǁ_get_nu_lam__mutmut_33,
        "xǁSkewedTǁ_get_nu_lam__mutmut_34": xǁSkewedTǁ_get_nu_lam__mutmut_34,
        "xǁSkewedTǁ_get_nu_lam__mutmut_35": xǁSkewedTǁ_get_nu_lam__mutmut_35,
        "xǁSkewedTǁ_get_nu_lam__mutmut_36": xǁSkewedTǁ_get_nu_lam__mutmut_36,
        "xǁSkewedTǁ_get_nu_lam__mutmut_37": xǁSkewedTǁ_get_nu_lam__mutmut_37,
        "xǁSkewedTǁ_get_nu_lam__mutmut_38": xǁSkewedTǁ_get_nu_lam__mutmut_38,
        "xǁSkewedTǁ_get_nu_lam__mutmut_39": xǁSkewedTǁ_get_nu_lam__mutmut_39,
        "xǁSkewedTǁ_get_nu_lam__mutmut_40": xǁSkewedTǁ_get_nu_lam__mutmut_40,
    }
    xǁSkewedTǁ_get_nu_lam__mutmut_orig.__name__ = "xǁSkewedTǁ_get_nu_lam"

    @staticmethod
    def _compute_abc(nu: float, lam: float) -> tuple[float, float, float]:
        """Compute Hansen's a, b, c constants.

        Parameters
        ----------
        nu : float
            Degrees of freedom.
        lam : float
            Skewness parameter.

        Returns
        -------
        tuple[float, float, float]
            (a, b, c) constants.
        """
        c = float(np.exp(gammaln((nu + 1) / 2) - gammaln(nu / 2) - 0.5 * np.log(np.pi * (nu - 2))))
        a = 4 * lam * c * (nu - 2) / (nu - 1)
        b2 = 1 + 3 * lam**2 - a**2
        b = float(np.sqrt(max(b2, 1e-12)))
        return a, b, c

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [resids, sigma2, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁloglikelihood__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁloglikelihood__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁloglikelihood__mutmut_orig(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_1(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = None
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_2(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(None)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_3(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = None

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_4(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(None, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_5(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, None)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_6(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_7(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(
            nu,
        )

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_8(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = None
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_9(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids * np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_10(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(None)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_11(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = None

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_12(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a * b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_13(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = +a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_14(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = None

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_15(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) - np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_16(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(None) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_17(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(None)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_18(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = None
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_19(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z <= threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_20(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = None

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_21(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(None, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_22(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, None, (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_23(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), None)

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_24(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where((b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_25(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_26(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(
            left_mask,
            (b * z + a) / (1 - lam),
        )

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_27(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) * (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_28(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z - a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_29(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b / z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_30(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 + lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_31(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (2 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_32(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) * (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_33(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z - a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_34(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b / z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_35(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 - lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_36(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (2 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_37(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = None
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_38(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) + ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_39(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc + 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_40(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 / np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_41(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 1.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_42(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(None) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_43(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) / np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_44(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) * 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_45(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu - 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_46(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 2) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_47(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 3) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_48(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(None)
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_49(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 - eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_50(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(2 + eta**2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_51(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 * (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_52(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta * 2 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_53(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**3 / (nu - 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_54(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu + 2))
        return ll

    def xǁSkewedTǁloglikelihood__mutmut_55(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 3))
        return ll

    xǁSkewedTǁloglikelihood__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁloglikelihood__mutmut_1": xǁSkewedTǁloglikelihood__mutmut_1,
        "xǁSkewedTǁloglikelihood__mutmut_2": xǁSkewedTǁloglikelihood__mutmut_2,
        "xǁSkewedTǁloglikelihood__mutmut_3": xǁSkewedTǁloglikelihood__mutmut_3,
        "xǁSkewedTǁloglikelihood__mutmut_4": xǁSkewedTǁloglikelihood__mutmut_4,
        "xǁSkewedTǁloglikelihood__mutmut_5": xǁSkewedTǁloglikelihood__mutmut_5,
        "xǁSkewedTǁloglikelihood__mutmut_6": xǁSkewedTǁloglikelihood__mutmut_6,
        "xǁSkewedTǁloglikelihood__mutmut_7": xǁSkewedTǁloglikelihood__mutmut_7,
        "xǁSkewedTǁloglikelihood__mutmut_8": xǁSkewedTǁloglikelihood__mutmut_8,
        "xǁSkewedTǁloglikelihood__mutmut_9": xǁSkewedTǁloglikelihood__mutmut_9,
        "xǁSkewedTǁloglikelihood__mutmut_10": xǁSkewedTǁloglikelihood__mutmut_10,
        "xǁSkewedTǁloglikelihood__mutmut_11": xǁSkewedTǁloglikelihood__mutmut_11,
        "xǁSkewedTǁloglikelihood__mutmut_12": xǁSkewedTǁloglikelihood__mutmut_12,
        "xǁSkewedTǁloglikelihood__mutmut_13": xǁSkewedTǁloglikelihood__mutmut_13,
        "xǁSkewedTǁloglikelihood__mutmut_14": xǁSkewedTǁloglikelihood__mutmut_14,
        "xǁSkewedTǁloglikelihood__mutmut_15": xǁSkewedTǁloglikelihood__mutmut_15,
        "xǁSkewedTǁloglikelihood__mutmut_16": xǁSkewedTǁloglikelihood__mutmut_16,
        "xǁSkewedTǁloglikelihood__mutmut_17": xǁSkewedTǁloglikelihood__mutmut_17,
        "xǁSkewedTǁloglikelihood__mutmut_18": xǁSkewedTǁloglikelihood__mutmut_18,
        "xǁSkewedTǁloglikelihood__mutmut_19": xǁSkewedTǁloglikelihood__mutmut_19,
        "xǁSkewedTǁloglikelihood__mutmut_20": xǁSkewedTǁloglikelihood__mutmut_20,
        "xǁSkewedTǁloglikelihood__mutmut_21": xǁSkewedTǁloglikelihood__mutmut_21,
        "xǁSkewedTǁloglikelihood__mutmut_22": xǁSkewedTǁloglikelihood__mutmut_22,
        "xǁSkewedTǁloglikelihood__mutmut_23": xǁSkewedTǁloglikelihood__mutmut_23,
        "xǁSkewedTǁloglikelihood__mutmut_24": xǁSkewedTǁloglikelihood__mutmut_24,
        "xǁSkewedTǁloglikelihood__mutmut_25": xǁSkewedTǁloglikelihood__mutmut_25,
        "xǁSkewedTǁloglikelihood__mutmut_26": xǁSkewedTǁloglikelihood__mutmut_26,
        "xǁSkewedTǁloglikelihood__mutmut_27": xǁSkewedTǁloglikelihood__mutmut_27,
        "xǁSkewedTǁloglikelihood__mutmut_28": xǁSkewedTǁloglikelihood__mutmut_28,
        "xǁSkewedTǁloglikelihood__mutmut_29": xǁSkewedTǁloglikelihood__mutmut_29,
        "xǁSkewedTǁloglikelihood__mutmut_30": xǁSkewedTǁloglikelihood__mutmut_30,
        "xǁSkewedTǁloglikelihood__mutmut_31": xǁSkewedTǁloglikelihood__mutmut_31,
        "xǁSkewedTǁloglikelihood__mutmut_32": xǁSkewedTǁloglikelihood__mutmut_32,
        "xǁSkewedTǁloglikelihood__mutmut_33": xǁSkewedTǁloglikelihood__mutmut_33,
        "xǁSkewedTǁloglikelihood__mutmut_34": xǁSkewedTǁloglikelihood__mutmut_34,
        "xǁSkewedTǁloglikelihood__mutmut_35": xǁSkewedTǁloglikelihood__mutmut_35,
        "xǁSkewedTǁloglikelihood__mutmut_36": xǁSkewedTǁloglikelihood__mutmut_36,
        "xǁSkewedTǁloglikelihood__mutmut_37": xǁSkewedTǁloglikelihood__mutmut_37,
        "xǁSkewedTǁloglikelihood__mutmut_38": xǁSkewedTǁloglikelihood__mutmut_38,
        "xǁSkewedTǁloglikelihood__mutmut_39": xǁSkewedTǁloglikelihood__mutmut_39,
        "xǁSkewedTǁloglikelihood__mutmut_40": xǁSkewedTǁloglikelihood__mutmut_40,
        "xǁSkewedTǁloglikelihood__mutmut_41": xǁSkewedTǁloglikelihood__mutmut_41,
        "xǁSkewedTǁloglikelihood__mutmut_42": xǁSkewedTǁloglikelihood__mutmut_42,
        "xǁSkewedTǁloglikelihood__mutmut_43": xǁSkewedTǁloglikelihood__mutmut_43,
        "xǁSkewedTǁloglikelihood__mutmut_44": xǁSkewedTǁloglikelihood__mutmut_44,
        "xǁSkewedTǁloglikelihood__mutmut_45": xǁSkewedTǁloglikelihood__mutmut_45,
        "xǁSkewedTǁloglikelihood__mutmut_46": xǁSkewedTǁloglikelihood__mutmut_46,
        "xǁSkewedTǁloglikelihood__mutmut_47": xǁSkewedTǁloglikelihood__mutmut_47,
        "xǁSkewedTǁloglikelihood__mutmut_48": xǁSkewedTǁloglikelihood__mutmut_48,
        "xǁSkewedTǁloglikelihood__mutmut_49": xǁSkewedTǁloglikelihood__mutmut_49,
        "xǁSkewedTǁloglikelihood__mutmut_50": xǁSkewedTǁloglikelihood__mutmut_50,
        "xǁSkewedTǁloglikelihood__mutmut_51": xǁSkewedTǁloglikelihood__mutmut_51,
        "xǁSkewedTǁloglikelihood__mutmut_52": xǁSkewedTǁloglikelihood__mutmut_52,
        "xǁSkewedTǁloglikelihood__mutmut_53": xǁSkewedTǁloglikelihood__mutmut_53,
        "xǁSkewedTǁloglikelihood__mutmut_54": xǁSkewedTǁloglikelihood__mutmut_54,
        "xǁSkewedTǁloglikelihood__mutmut_55": xǁSkewedTǁloglikelihood__mutmut_55,
    }
    xǁSkewedTǁloglikelihood__mutmut_orig.__name__ = "xǁSkewedTǁloglikelihood"

    def ppf(self, q: float) -> float:
        args = [q]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁppf__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁppf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁppf__mutmut_orig(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_1(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) + q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_2(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(None) - q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_3(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = None  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_4(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(None, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_5(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, None, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_6(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, None)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_7(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(-50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_8(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_9(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(
            _cdf_minus_q,
            -50.0,
        )  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_10(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, +50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_11(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -51.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁSkewedTǁppf__mutmut_12(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, 51.0)  # type: ignore[assignment]
        return result

    xǁSkewedTǁppf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁppf__mutmut_1": xǁSkewedTǁppf__mutmut_1,
        "xǁSkewedTǁppf__mutmut_2": xǁSkewedTǁppf__mutmut_2,
        "xǁSkewedTǁppf__mutmut_3": xǁSkewedTǁppf__mutmut_3,
        "xǁSkewedTǁppf__mutmut_4": xǁSkewedTǁppf__mutmut_4,
        "xǁSkewedTǁppf__mutmut_5": xǁSkewedTǁppf__mutmut_5,
        "xǁSkewedTǁppf__mutmut_6": xǁSkewedTǁppf__mutmut_6,
        "xǁSkewedTǁppf__mutmut_7": xǁSkewedTǁppf__mutmut_7,
        "xǁSkewedTǁppf__mutmut_8": xǁSkewedTǁppf__mutmut_8,
        "xǁSkewedTǁppf__mutmut_9": xǁSkewedTǁppf__mutmut_9,
        "xǁSkewedTǁppf__mutmut_10": xǁSkewedTǁppf__mutmut_10,
        "xǁSkewedTǁppf__mutmut_11": xǁSkewedTǁppf__mutmut_11,
        "xǁSkewedTǁppf__mutmut_12": xǁSkewedTǁppf__mutmut_12,
    }
    xǁSkewedTǁppf__mutmut_orig.__name__ = "xǁSkewedTǁppf"

    def cdf(self, x: float) -> float:
        args = [x]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁcdf__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁcdf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁcdf__mutmut_orig(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_1(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = None
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_2(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = None
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_3(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(None, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_4(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, None)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_5(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_6(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(
            nu,
        )
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_7(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = None

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_8(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a * b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_9(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = +a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_10(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x <= threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_11(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = None
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_12(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) * (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_13(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x - a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_14(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b / x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_15(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 + lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_16(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (2 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_17(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = None
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_18(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(None, df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_19(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=None)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_20(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_21(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(
                eta * np.sqrt(nu / (nu - 2)),
            )
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_22(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta / np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_23(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(None), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_24(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu * (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_25(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu + 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_26(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 3)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_27(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float(None)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_28(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) / p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_29(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_30(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((2 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_31(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = None
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_32(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) * (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_33(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x - a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_34(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b / x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_35(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 - lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_36(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (2 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_37(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = None
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_38(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(None, df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_39(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=None)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_40(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_41(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(
                eta * np.sqrt(nu / (nu - 2)),
            )
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_42(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta / np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_43(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(None), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_44(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu * (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_45(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu + 2)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_46(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 3)), df=nu)
            return float((1 + lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_47(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float(None)

    def xǁSkewedTǁcdf__mutmut_48(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p + lam)

    def xǁSkewedTǁcdf__mutmut_49(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) / p - lam)

    def xǁSkewedTǁcdf__mutmut_50(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p - lam)

    def xǁSkewedTǁcdf__mutmut_51(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((2 + lam) * p - lam)

    xǁSkewedTǁcdf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁcdf__mutmut_1": xǁSkewedTǁcdf__mutmut_1,
        "xǁSkewedTǁcdf__mutmut_2": xǁSkewedTǁcdf__mutmut_2,
        "xǁSkewedTǁcdf__mutmut_3": xǁSkewedTǁcdf__mutmut_3,
        "xǁSkewedTǁcdf__mutmut_4": xǁSkewedTǁcdf__mutmut_4,
        "xǁSkewedTǁcdf__mutmut_5": xǁSkewedTǁcdf__mutmut_5,
        "xǁSkewedTǁcdf__mutmut_6": xǁSkewedTǁcdf__mutmut_6,
        "xǁSkewedTǁcdf__mutmut_7": xǁSkewedTǁcdf__mutmut_7,
        "xǁSkewedTǁcdf__mutmut_8": xǁSkewedTǁcdf__mutmut_8,
        "xǁSkewedTǁcdf__mutmut_9": xǁSkewedTǁcdf__mutmut_9,
        "xǁSkewedTǁcdf__mutmut_10": xǁSkewedTǁcdf__mutmut_10,
        "xǁSkewedTǁcdf__mutmut_11": xǁSkewedTǁcdf__mutmut_11,
        "xǁSkewedTǁcdf__mutmut_12": xǁSkewedTǁcdf__mutmut_12,
        "xǁSkewedTǁcdf__mutmut_13": xǁSkewedTǁcdf__mutmut_13,
        "xǁSkewedTǁcdf__mutmut_14": xǁSkewedTǁcdf__mutmut_14,
        "xǁSkewedTǁcdf__mutmut_15": xǁSkewedTǁcdf__mutmut_15,
        "xǁSkewedTǁcdf__mutmut_16": xǁSkewedTǁcdf__mutmut_16,
        "xǁSkewedTǁcdf__mutmut_17": xǁSkewedTǁcdf__mutmut_17,
        "xǁSkewedTǁcdf__mutmut_18": xǁSkewedTǁcdf__mutmut_18,
        "xǁSkewedTǁcdf__mutmut_19": xǁSkewedTǁcdf__mutmut_19,
        "xǁSkewedTǁcdf__mutmut_20": xǁSkewedTǁcdf__mutmut_20,
        "xǁSkewedTǁcdf__mutmut_21": xǁSkewedTǁcdf__mutmut_21,
        "xǁSkewedTǁcdf__mutmut_22": xǁSkewedTǁcdf__mutmut_22,
        "xǁSkewedTǁcdf__mutmut_23": xǁSkewedTǁcdf__mutmut_23,
        "xǁSkewedTǁcdf__mutmut_24": xǁSkewedTǁcdf__mutmut_24,
        "xǁSkewedTǁcdf__mutmut_25": xǁSkewedTǁcdf__mutmut_25,
        "xǁSkewedTǁcdf__mutmut_26": xǁSkewedTǁcdf__mutmut_26,
        "xǁSkewedTǁcdf__mutmut_27": xǁSkewedTǁcdf__mutmut_27,
        "xǁSkewedTǁcdf__mutmut_28": xǁSkewedTǁcdf__mutmut_28,
        "xǁSkewedTǁcdf__mutmut_29": xǁSkewedTǁcdf__mutmut_29,
        "xǁSkewedTǁcdf__mutmut_30": xǁSkewedTǁcdf__mutmut_30,
        "xǁSkewedTǁcdf__mutmut_31": xǁSkewedTǁcdf__mutmut_31,
        "xǁSkewedTǁcdf__mutmut_32": xǁSkewedTǁcdf__mutmut_32,
        "xǁSkewedTǁcdf__mutmut_33": xǁSkewedTǁcdf__mutmut_33,
        "xǁSkewedTǁcdf__mutmut_34": xǁSkewedTǁcdf__mutmut_34,
        "xǁSkewedTǁcdf__mutmut_35": xǁSkewedTǁcdf__mutmut_35,
        "xǁSkewedTǁcdf__mutmut_36": xǁSkewedTǁcdf__mutmut_36,
        "xǁSkewedTǁcdf__mutmut_37": xǁSkewedTǁcdf__mutmut_37,
        "xǁSkewedTǁcdf__mutmut_38": xǁSkewedTǁcdf__mutmut_38,
        "xǁSkewedTǁcdf__mutmut_39": xǁSkewedTǁcdf__mutmut_39,
        "xǁSkewedTǁcdf__mutmut_40": xǁSkewedTǁcdf__mutmut_40,
        "xǁSkewedTǁcdf__mutmut_41": xǁSkewedTǁcdf__mutmut_41,
        "xǁSkewedTǁcdf__mutmut_42": xǁSkewedTǁcdf__mutmut_42,
        "xǁSkewedTǁcdf__mutmut_43": xǁSkewedTǁcdf__mutmut_43,
        "xǁSkewedTǁcdf__mutmut_44": xǁSkewedTǁcdf__mutmut_44,
        "xǁSkewedTǁcdf__mutmut_45": xǁSkewedTǁcdf__mutmut_45,
        "xǁSkewedTǁcdf__mutmut_46": xǁSkewedTǁcdf__mutmut_46,
        "xǁSkewedTǁcdf__mutmut_47": xǁSkewedTǁcdf__mutmut_47,
        "xǁSkewedTǁcdf__mutmut_48": xǁSkewedTǁcdf__mutmut_48,
        "xǁSkewedTǁcdf__mutmut_49": xǁSkewedTǁcdf__mutmut_49,
        "xǁSkewedTǁcdf__mutmut_50": xǁSkewedTǁcdf__mutmut_50,
        "xǁSkewedTǁcdf__mutmut_51": xǁSkewedTǁcdf__mutmut_51,
    }
    xǁSkewedTǁcdf__mutmut_orig.__name__ = "xǁSkewedTǁcdf"

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [n, rng, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁsimulate__mutmut_orig(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_1(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = None
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_2(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(None)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_3(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = None

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_4(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(None, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_5(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, None)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_6(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_7(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(
            nu,
        )

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_8(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = None

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_9(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) * np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_10(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(None, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_11(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=None) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_12(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_13(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(
            nu,
        ) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_14(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(None)

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_15(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu * (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_16(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu + 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_17(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 3))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_18(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = None
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_19(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=None)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_20(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = None

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_21(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) * 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_22(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 + lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_23(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (2 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_24(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 3

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_25(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = None
        return z

    def xǁSkewedTǁsimulate__mutmut_26(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            None,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_27(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            None,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_28(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            None,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_29(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_30(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_31(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_32(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u <= threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_33(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples + a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_34(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) / t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_35(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) * b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_36(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 + lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_37(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((2 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_38(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a * b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_39(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples + a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_40(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) / t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_41(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) * b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_42(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 - lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_43(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((2 + lam) / b) * t_samples - a / b,
        )
        return z

    def xǁSkewedTǁsimulate__mutmut_44(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a * b,
        )
        return z

    xǁSkewedTǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁsimulate__mutmut_1": xǁSkewedTǁsimulate__mutmut_1,
        "xǁSkewedTǁsimulate__mutmut_2": xǁSkewedTǁsimulate__mutmut_2,
        "xǁSkewedTǁsimulate__mutmut_3": xǁSkewedTǁsimulate__mutmut_3,
        "xǁSkewedTǁsimulate__mutmut_4": xǁSkewedTǁsimulate__mutmut_4,
        "xǁSkewedTǁsimulate__mutmut_5": xǁSkewedTǁsimulate__mutmut_5,
        "xǁSkewedTǁsimulate__mutmut_6": xǁSkewedTǁsimulate__mutmut_6,
        "xǁSkewedTǁsimulate__mutmut_7": xǁSkewedTǁsimulate__mutmut_7,
        "xǁSkewedTǁsimulate__mutmut_8": xǁSkewedTǁsimulate__mutmut_8,
        "xǁSkewedTǁsimulate__mutmut_9": xǁSkewedTǁsimulate__mutmut_9,
        "xǁSkewedTǁsimulate__mutmut_10": xǁSkewedTǁsimulate__mutmut_10,
        "xǁSkewedTǁsimulate__mutmut_11": xǁSkewedTǁsimulate__mutmut_11,
        "xǁSkewedTǁsimulate__mutmut_12": xǁSkewedTǁsimulate__mutmut_12,
        "xǁSkewedTǁsimulate__mutmut_13": xǁSkewedTǁsimulate__mutmut_13,
        "xǁSkewedTǁsimulate__mutmut_14": xǁSkewedTǁsimulate__mutmut_14,
        "xǁSkewedTǁsimulate__mutmut_15": xǁSkewedTǁsimulate__mutmut_15,
        "xǁSkewedTǁsimulate__mutmut_16": xǁSkewedTǁsimulate__mutmut_16,
        "xǁSkewedTǁsimulate__mutmut_17": xǁSkewedTǁsimulate__mutmut_17,
        "xǁSkewedTǁsimulate__mutmut_18": xǁSkewedTǁsimulate__mutmut_18,
        "xǁSkewedTǁsimulate__mutmut_19": xǁSkewedTǁsimulate__mutmut_19,
        "xǁSkewedTǁsimulate__mutmut_20": xǁSkewedTǁsimulate__mutmut_20,
        "xǁSkewedTǁsimulate__mutmut_21": xǁSkewedTǁsimulate__mutmut_21,
        "xǁSkewedTǁsimulate__mutmut_22": xǁSkewedTǁsimulate__mutmut_22,
        "xǁSkewedTǁsimulate__mutmut_23": xǁSkewedTǁsimulate__mutmut_23,
        "xǁSkewedTǁsimulate__mutmut_24": xǁSkewedTǁsimulate__mutmut_24,
        "xǁSkewedTǁsimulate__mutmut_25": xǁSkewedTǁsimulate__mutmut_25,
        "xǁSkewedTǁsimulate__mutmut_26": xǁSkewedTǁsimulate__mutmut_26,
        "xǁSkewedTǁsimulate__mutmut_27": xǁSkewedTǁsimulate__mutmut_27,
        "xǁSkewedTǁsimulate__mutmut_28": xǁSkewedTǁsimulate__mutmut_28,
        "xǁSkewedTǁsimulate__mutmut_29": xǁSkewedTǁsimulate__mutmut_29,
        "xǁSkewedTǁsimulate__mutmut_30": xǁSkewedTǁsimulate__mutmut_30,
        "xǁSkewedTǁsimulate__mutmut_31": xǁSkewedTǁsimulate__mutmut_31,
        "xǁSkewedTǁsimulate__mutmut_32": xǁSkewedTǁsimulate__mutmut_32,
        "xǁSkewedTǁsimulate__mutmut_33": xǁSkewedTǁsimulate__mutmut_33,
        "xǁSkewedTǁsimulate__mutmut_34": xǁSkewedTǁsimulate__mutmut_34,
        "xǁSkewedTǁsimulate__mutmut_35": xǁSkewedTǁsimulate__mutmut_35,
        "xǁSkewedTǁsimulate__mutmut_36": xǁSkewedTǁsimulate__mutmut_36,
        "xǁSkewedTǁsimulate__mutmut_37": xǁSkewedTǁsimulate__mutmut_37,
        "xǁSkewedTǁsimulate__mutmut_38": xǁSkewedTǁsimulate__mutmut_38,
        "xǁSkewedTǁsimulate__mutmut_39": xǁSkewedTǁsimulate__mutmut_39,
        "xǁSkewedTǁsimulate__mutmut_40": xǁSkewedTǁsimulate__mutmut_40,
        "xǁSkewedTǁsimulate__mutmut_41": xǁSkewedTǁsimulate__mutmut_41,
        "xǁSkewedTǁsimulate__mutmut_42": xǁSkewedTǁsimulate__mutmut_42,
        "xǁSkewedTǁsimulate__mutmut_43": xǁSkewedTǁsimulate__mutmut_43,
        "xǁSkewedTǁsimulate__mutmut_44": xǁSkewedTǁsimulate__mutmut_44,
    }
    xǁSkewedTǁsimulate__mutmut_orig.__name__ = "xǁSkewedTǁsimulate"

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) != 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 1:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = None
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = None
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 1
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is not None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = None
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 - np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 3.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(None)
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx = 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx -= 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 2
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is not None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = None
        return constrained

    def xǁSkewedTǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(None)
        return constrained

    xǁSkewedTǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁtransform_params__mutmut_1": xǁSkewedTǁtransform_params__mutmut_1,
        "xǁSkewedTǁtransform_params__mutmut_2": xǁSkewedTǁtransform_params__mutmut_2,
        "xǁSkewedTǁtransform_params__mutmut_3": xǁSkewedTǁtransform_params__mutmut_3,
        "xǁSkewedTǁtransform_params__mutmut_4": xǁSkewedTǁtransform_params__mutmut_4,
        "xǁSkewedTǁtransform_params__mutmut_5": xǁSkewedTǁtransform_params__mutmut_5,
        "xǁSkewedTǁtransform_params__mutmut_6": xǁSkewedTǁtransform_params__mutmut_6,
        "xǁSkewedTǁtransform_params__mutmut_7": xǁSkewedTǁtransform_params__mutmut_7,
        "xǁSkewedTǁtransform_params__mutmut_8": xǁSkewedTǁtransform_params__mutmut_8,
        "xǁSkewedTǁtransform_params__mutmut_9": xǁSkewedTǁtransform_params__mutmut_9,
        "xǁSkewedTǁtransform_params__mutmut_10": xǁSkewedTǁtransform_params__mutmut_10,
        "xǁSkewedTǁtransform_params__mutmut_11": xǁSkewedTǁtransform_params__mutmut_11,
        "xǁSkewedTǁtransform_params__mutmut_12": xǁSkewedTǁtransform_params__mutmut_12,
        "xǁSkewedTǁtransform_params__mutmut_13": xǁSkewedTǁtransform_params__mutmut_13,
        "xǁSkewedTǁtransform_params__mutmut_14": xǁSkewedTǁtransform_params__mutmut_14,
        "xǁSkewedTǁtransform_params__mutmut_15": xǁSkewedTǁtransform_params__mutmut_15,
        "xǁSkewedTǁtransform_params__mutmut_16": xǁSkewedTǁtransform_params__mutmut_16,
    }
    xǁSkewedTǁtransform_params__mutmut_orig.__name__ = "xǁSkewedTǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) != 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 1:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = None
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = None
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 1
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is not None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = None
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(None)
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(None, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, None))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(
                max(
                    constrained[idx] - 2.0,
                )
            )
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] + 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 3.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1.000001))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx = 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx -= 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 2
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is not None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = None
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(None)
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(None, -0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], None, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, None))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(-0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(
                np.clip(
                    constrained[idx],
                    -0.999,
                )
            )
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], +0.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_29(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -1.999, 0.999))
        return unconstrained

    def xǁSkewedTǁuntransform_params__mutmut_30(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 1.999))
        return unconstrained

    xǁSkewedTǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁuntransform_params__mutmut_1": xǁSkewedTǁuntransform_params__mutmut_1,
        "xǁSkewedTǁuntransform_params__mutmut_2": xǁSkewedTǁuntransform_params__mutmut_2,
        "xǁSkewedTǁuntransform_params__mutmut_3": xǁSkewedTǁuntransform_params__mutmut_3,
        "xǁSkewedTǁuntransform_params__mutmut_4": xǁSkewedTǁuntransform_params__mutmut_4,
        "xǁSkewedTǁuntransform_params__mutmut_5": xǁSkewedTǁuntransform_params__mutmut_5,
        "xǁSkewedTǁuntransform_params__mutmut_6": xǁSkewedTǁuntransform_params__mutmut_6,
        "xǁSkewedTǁuntransform_params__mutmut_7": xǁSkewedTǁuntransform_params__mutmut_7,
        "xǁSkewedTǁuntransform_params__mutmut_8": xǁSkewedTǁuntransform_params__mutmut_8,
        "xǁSkewedTǁuntransform_params__mutmut_9": xǁSkewedTǁuntransform_params__mutmut_9,
        "xǁSkewedTǁuntransform_params__mutmut_10": xǁSkewedTǁuntransform_params__mutmut_10,
        "xǁSkewedTǁuntransform_params__mutmut_11": xǁSkewedTǁuntransform_params__mutmut_11,
        "xǁSkewedTǁuntransform_params__mutmut_12": xǁSkewedTǁuntransform_params__mutmut_12,
        "xǁSkewedTǁuntransform_params__mutmut_13": xǁSkewedTǁuntransform_params__mutmut_13,
        "xǁSkewedTǁuntransform_params__mutmut_14": xǁSkewedTǁuntransform_params__mutmut_14,
        "xǁSkewedTǁuntransform_params__mutmut_15": xǁSkewedTǁuntransform_params__mutmut_15,
        "xǁSkewedTǁuntransform_params__mutmut_16": xǁSkewedTǁuntransform_params__mutmut_16,
        "xǁSkewedTǁuntransform_params__mutmut_17": xǁSkewedTǁuntransform_params__mutmut_17,
        "xǁSkewedTǁuntransform_params__mutmut_18": xǁSkewedTǁuntransform_params__mutmut_18,
        "xǁSkewedTǁuntransform_params__mutmut_19": xǁSkewedTǁuntransform_params__mutmut_19,
        "xǁSkewedTǁuntransform_params__mutmut_20": xǁSkewedTǁuntransform_params__mutmut_20,
        "xǁSkewedTǁuntransform_params__mutmut_21": xǁSkewedTǁuntransform_params__mutmut_21,
        "xǁSkewedTǁuntransform_params__mutmut_22": xǁSkewedTǁuntransform_params__mutmut_22,
        "xǁSkewedTǁuntransform_params__mutmut_23": xǁSkewedTǁuntransform_params__mutmut_23,
        "xǁSkewedTǁuntransform_params__mutmut_24": xǁSkewedTǁuntransform_params__mutmut_24,
        "xǁSkewedTǁuntransform_params__mutmut_25": xǁSkewedTǁuntransform_params__mutmut_25,
        "xǁSkewedTǁuntransform_params__mutmut_26": xǁSkewedTǁuntransform_params__mutmut_26,
        "xǁSkewedTǁuntransform_params__mutmut_27": xǁSkewedTǁuntransform_params__mutmut_27,
        "xǁSkewedTǁuntransform_params__mutmut_28": xǁSkewedTǁuntransform_params__mutmut_28,
        "xǁSkewedTǁuntransform_params__mutmut_29": xǁSkewedTǁuntransform_params__mutmut_29,
        "xǁSkewedTǁuntransform_params__mutmut_30": xǁSkewedTǁuntransform_params__mutmut_30,
    }
    xǁSkewedTǁuntransform_params__mutmut_orig.__name__ = "xǁSkewedTǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁSkewedTǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁSkewedTǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁSkewedTǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((-0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = None
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((-0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is not None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((-0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append(None)
        if self._fixed_lam is None:
            bnds.append((-0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((3.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((-0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 101.0))
        if self._fixed_lam is None:
            bnds.append((-0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is not None:
            bnds.append((-0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append(None)
        return bnds

    def xǁSkewedTǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((+0.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((-1.999, 0.999))
        return bnds

    def xǁSkewedTǁbounds__mutmut_10(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((-0.999, 1.999))
        return bnds

    xǁSkewedTǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁSkewedTǁbounds__mutmut_1": xǁSkewedTǁbounds__mutmut_1,
        "xǁSkewedTǁbounds__mutmut_2": xǁSkewedTǁbounds__mutmut_2,
        "xǁSkewedTǁbounds__mutmut_3": xǁSkewedTǁbounds__mutmut_3,
        "xǁSkewedTǁbounds__mutmut_4": xǁSkewedTǁbounds__mutmut_4,
        "xǁSkewedTǁbounds__mutmut_5": xǁSkewedTǁbounds__mutmut_5,
        "xǁSkewedTǁbounds__mutmut_6": xǁSkewedTǁbounds__mutmut_6,
        "xǁSkewedTǁbounds__mutmut_7": xǁSkewedTǁbounds__mutmut_7,
        "xǁSkewedTǁbounds__mutmut_8": xǁSkewedTǁbounds__mutmut_8,
        "xǁSkewedTǁbounds__mutmut_9": xǁSkewedTǁbounds__mutmut_9,
        "xǁSkewedTǁbounds__mutmut_10": xǁSkewedTǁbounds__mutmut_10,
    }
    xǁSkewedTǁbounds__mutmut_orig.__name__ = "xǁSkewedTǁbounds"
