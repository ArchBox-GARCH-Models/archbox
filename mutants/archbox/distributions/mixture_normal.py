"""Mixture Normal distribution (Haas, Mittnik & Paolella, 2004).

f(z) = p * N(0, sigma1^2) + (1-p) * N(0, sigma2^2)

Unit variance constraint: p * sigma1^2 + (1-p) * sigma2^2 = 1
=> sigma2^2 = (1 - p * sigma1^2) / (1 - p)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, ClassVar

import numpy as np
from numpy.typing import NDArray
from scipy import stats

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


class MixtureNormal(Distribution):
    """Mixture of two Normal distributions for GARCH models.

    The unit variance constraint ensures:
    p * sigma1^2 + (1-p) * sigma2^2 = 1

    Parameters
    ----------
    p : float, optional
        Mixing probability. Must be in (0, 1).
    sigma1 : float, optional
        Standard deviation of first component. Must be > 0.
    """

    name = "Mixture Normal"

    def __init__(self, p: float | None = None, sigma1: float | None = None) -> None:
        args = [p, sigma1]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁ__init____mutmut_orig(
        self, p: float | None = None, sigma1: float | None = None
    ) -> None:
        """Initialize Mixture Normal distribution with optional parameters."""
        self._fixed_p = p
        self._fixed_sigma1 = sigma1

    def xǁMixtureNormalǁ__init____mutmut_1(
        self, p: float | None = None, sigma1: float | None = None
    ) -> None:
        """Initialize Mixture Normal distribution with optional parameters."""
        self._fixed_p = None
        self._fixed_sigma1 = sigma1

    def xǁMixtureNormalǁ__init____mutmut_2(
        self, p: float | None = None, sigma1: float | None = None
    ) -> None:
        """Initialize Mixture Normal distribution with optional parameters."""
        self._fixed_p = p
        self._fixed_sigma1 = None

    xǁMixtureNormalǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁ__init____mutmut_1": xǁMixtureNormalǁ__init____mutmut_1,
        "xǁMixtureNormalǁ__init____mutmut_2": xǁMixtureNormalǁ__init____mutmut_2,
    }
    xǁMixtureNormalǁ__init____mutmut_orig.__name__ = "xǁMixtureNormalǁ__init__"

    @property
    def num_params(self) -> int:
        """Number of distribution shape parameters."""
        count = 0
        if self._fixed_p is None:
            count += 1
        if self._fixed_sigma1 is None:
            count += 1
        return count

    @property
    def param_names(self) -> list[str]:
        """Distribution parameter names."""
        names: list[str] = []
        if self._fixed_p is None:
            names.append("p")
        if self._fixed_sigma1 is None:
            names.append("sigma1")
        return names

    def start_params(self) -> NDArray[np.float64]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁstart_params__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁstart_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁstart_params__mutmut_orig(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_1(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = None
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_2(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is not None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_3(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(None)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_4(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(1.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_5(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is not None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_6(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(None)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_7(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(1.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_8(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(None, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_9(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=None) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_10(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(dtype=np.float64) if params else np.array([], dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_11(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return (
            np.array(
                params,
            )
            if params
            else np.array([], dtype=np.float64)
        )

    def xǁMixtureNormalǁstart_params__mutmut_12(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array(None, dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_13(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=None)

    def xǁMixtureNormalǁstart_params__mutmut_14(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array(dtype=np.float64)

    def xǁMixtureNormalǁstart_params__mutmut_15(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return (
            np.array(params, dtype=np.float64)
            if params
            else np.array(
                [],
            )
        )

    xǁMixtureNormalǁstart_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁstart_params__mutmut_1": xǁMixtureNormalǁstart_params__mutmut_1,
        "xǁMixtureNormalǁstart_params__mutmut_2": xǁMixtureNormalǁstart_params__mutmut_2,
        "xǁMixtureNormalǁstart_params__mutmut_3": xǁMixtureNormalǁstart_params__mutmut_3,
        "xǁMixtureNormalǁstart_params__mutmut_4": xǁMixtureNormalǁstart_params__mutmut_4,
        "xǁMixtureNormalǁstart_params__mutmut_5": xǁMixtureNormalǁstart_params__mutmut_5,
        "xǁMixtureNormalǁstart_params__mutmut_6": xǁMixtureNormalǁstart_params__mutmut_6,
        "xǁMixtureNormalǁstart_params__mutmut_7": xǁMixtureNormalǁstart_params__mutmut_7,
        "xǁMixtureNormalǁstart_params__mutmut_8": xǁMixtureNormalǁstart_params__mutmut_8,
        "xǁMixtureNormalǁstart_params__mutmut_9": xǁMixtureNormalǁstart_params__mutmut_9,
        "xǁMixtureNormalǁstart_params__mutmut_10": xǁMixtureNormalǁstart_params__mutmut_10,
        "xǁMixtureNormalǁstart_params__mutmut_11": xǁMixtureNormalǁstart_params__mutmut_11,
        "xǁMixtureNormalǁstart_params__mutmut_12": xǁMixtureNormalǁstart_params__mutmut_12,
        "xǁMixtureNormalǁstart_params__mutmut_13": xǁMixtureNormalǁstart_params__mutmut_13,
        "xǁMixtureNormalǁstart_params__mutmut_14": xǁMixtureNormalǁstart_params__mutmut_14,
        "xǁMixtureNormalǁstart_params__mutmut_15": xǁMixtureNormalǁstart_params__mutmut_15,
    }
    xǁMixtureNormalǁstart_params__mutmut_orig.__name__ = "xǁMixtureNormalǁstart_params"

    def _get_p_sigma1(self, dist_params: NDArray[np.float64] | None = None) -> tuple[float, float]:
        args = [dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁ_get_p_sigma1__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁ_get_p_sigma1__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_orig(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_1(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = None
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_2(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 1
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_3(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_4(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = None
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_5(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None or idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_6(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_7(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx <= len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_8(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = None
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_9(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(None)
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_10(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx = 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_11(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx -= 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_12(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 2
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_13(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = None

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_14(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 1.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_15(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_16(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = None
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_17(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None or idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_18(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_19(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx <= len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_20(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = None
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_21(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(None)
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_22(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = None

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_23(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 1.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_24(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = None
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_25(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(None)
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_26(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(None, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_27(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, None, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_28(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, None))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_29(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_30(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_31(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(
            np.clip(
                p,
                0.01,
            )
        )
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_32(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 1.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_33(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 1.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_34(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = None
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_35(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(None, 0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_36(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, None)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_37(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(0.01)
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_38(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(
            sigma1,
        )
        return p, sigma1

    def xǁMixtureNormalǁ_get_p_sigma1__mutmut_39(
        self, dist_params: NDArray[np.float64] | None = None
    ) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 1.01)
        return p, sigma1

    xǁMixtureNormalǁ_get_p_sigma1__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_1": xǁMixtureNormalǁ_get_p_sigma1__mutmut_1,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_2": xǁMixtureNormalǁ_get_p_sigma1__mutmut_2,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_3": xǁMixtureNormalǁ_get_p_sigma1__mutmut_3,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_4": xǁMixtureNormalǁ_get_p_sigma1__mutmut_4,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_5": xǁMixtureNormalǁ_get_p_sigma1__mutmut_5,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_6": xǁMixtureNormalǁ_get_p_sigma1__mutmut_6,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_7": xǁMixtureNormalǁ_get_p_sigma1__mutmut_7,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_8": xǁMixtureNormalǁ_get_p_sigma1__mutmut_8,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_9": xǁMixtureNormalǁ_get_p_sigma1__mutmut_9,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_10": xǁMixtureNormalǁ_get_p_sigma1__mutmut_10,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_11": xǁMixtureNormalǁ_get_p_sigma1__mutmut_11,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_12": xǁMixtureNormalǁ_get_p_sigma1__mutmut_12,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_13": xǁMixtureNormalǁ_get_p_sigma1__mutmut_13,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_14": xǁMixtureNormalǁ_get_p_sigma1__mutmut_14,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_15": xǁMixtureNormalǁ_get_p_sigma1__mutmut_15,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_16": xǁMixtureNormalǁ_get_p_sigma1__mutmut_16,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_17": xǁMixtureNormalǁ_get_p_sigma1__mutmut_17,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_18": xǁMixtureNormalǁ_get_p_sigma1__mutmut_18,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_19": xǁMixtureNormalǁ_get_p_sigma1__mutmut_19,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_20": xǁMixtureNormalǁ_get_p_sigma1__mutmut_20,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_21": xǁMixtureNormalǁ_get_p_sigma1__mutmut_21,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_22": xǁMixtureNormalǁ_get_p_sigma1__mutmut_22,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_23": xǁMixtureNormalǁ_get_p_sigma1__mutmut_23,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_24": xǁMixtureNormalǁ_get_p_sigma1__mutmut_24,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_25": xǁMixtureNormalǁ_get_p_sigma1__mutmut_25,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_26": xǁMixtureNormalǁ_get_p_sigma1__mutmut_26,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_27": xǁMixtureNormalǁ_get_p_sigma1__mutmut_27,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_28": xǁMixtureNormalǁ_get_p_sigma1__mutmut_28,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_29": xǁMixtureNormalǁ_get_p_sigma1__mutmut_29,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_30": xǁMixtureNormalǁ_get_p_sigma1__mutmut_30,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_31": xǁMixtureNormalǁ_get_p_sigma1__mutmut_31,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_32": xǁMixtureNormalǁ_get_p_sigma1__mutmut_32,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_33": xǁMixtureNormalǁ_get_p_sigma1__mutmut_33,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_34": xǁMixtureNormalǁ_get_p_sigma1__mutmut_34,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_35": xǁMixtureNormalǁ_get_p_sigma1__mutmut_35,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_36": xǁMixtureNormalǁ_get_p_sigma1__mutmut_36,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_37": xǁMixtureNormalǁ_get_p_sigma1__mutmut_37,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_38": xǁMixtureNormalǁ_get_p_sigma1__mutmut_38,
        "xǁMixtureNormalǁ_get_p_sigma1__mutmut_39": xǁMixtureNormalǁ_get_p_sigma1__mutmut_39,
    }
    xǁMixtureNormalǁ_get_p_sigma1__mutmut_orig.__name__ = "xǁMixtureNormalǁ_get_p_sigma1"

    @staticmethod
    def _compute_sigma2(p: float, sigma1: float) -> float:
        """Compute sigma2 from unit variance constraint.

        sigma2^2 = (1 - p * sigma1^2) / (1 - p)

        Parameters
        ----------
        p : float
            Mixing probability.
        sigma1 : float
            Std dev of first component.

        Returns
        -------
        float
            sigma2 (std dev of second component).
        """
        numerator = 1.0 - p * sigma1**2
        denominator = 1.0 - p
        if numerator <= 0 or denominator <= 0:
            return 1.0  # fallback
        return float(np.sqrt(numerator / denominator))

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [resids, sigma2, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁloglikelihood__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁloglikelihood__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁloglikelihood__mutmut_orig(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_1(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = None
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_2(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(None)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_3(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = None

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_4(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(None, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_5(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, None)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_6(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_7(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(
            p,
        )

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_8(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = None

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_9(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids * np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_10(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(None)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_11(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = None
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_12(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) / np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_13(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p / (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_14(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 * (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_15(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (2.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_16(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) / sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_17(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(None) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_18(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 / np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_19(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(3 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_20(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(None)
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_21(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) * (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_22(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(+(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_23(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z * 2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_24(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**3) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_25(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 / sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_26(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (3 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_27(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1 * 2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_28(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**3))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_29(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = None

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_30(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            / np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_31(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            / (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_32(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 + p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_33(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (2 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_34(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 * (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_35(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (2.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_36(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) / sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_37(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p) * (1.0 / (np.sqrt(None) * sigma2_comp)) * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_38(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 / np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_39(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(3 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_40(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (1 - p) * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp)) * np.exp(None)

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_41(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) * (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_42(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(+(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_43(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z * 2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_44(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**3) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_45(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 / sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_46(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (3 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_47(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp * 2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_48(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**3))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_49(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = None
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_50(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 - comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_51(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = None

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_52(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(None, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_53(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, None)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_54(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_55(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(
            mixture_density,
        )

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_56(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1.0)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_57(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = None
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_58(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) - np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_59(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 / np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_60(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = +0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_61(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -1.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_62(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(None) + np.log(mixture_density)
        return ll

    def xǁMixtureNormalǁloglikelihood__mutmut_63(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(None)
        return ll

    xǁMixtureNormalǁloglikelihood__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁloglikelihood__mutmut_1": xǁMixtureNormalǁloglikelihood__mutmut_1,
        "xǁMixtureNormalǁloglikelihood__mutmut_2": xǁMixtureNormalǁloglikelihood__mutmut_2,
        "xǁMixtureNormalǁloglikelihood__mutmut_3": xǁMixtureNormalǁloglikelihood__mutmut_3,
        "xǁMixtureNormalǁloglikelihood__mutmut_4": xǁMixtureNormalǁloglikelihood__mutmut_4,
        "xǁMixtureNormalǁloglikelihood__mutmut_5": xǁMixtureNormalǁloglikelihood__mutmut_5,
        "xǁMixtureNormalǁloglikelihood__mutmut_6": xǁMixtureNormalǁloglikelihood__mutmut_6,
        "xǁMixtureNormalǁloglikelihood__mutmut_7": xǁMixtureNormalǁloglikelihood__mutmut_7,
        "xǁMixtureNormalǁloglikelihood__mutmut_8": xǁMixtureNormalǁloglikelihood__mutmut_8,
        "xǁMixtureNormalǁloglikelihood__mutmut_9": xǁMixtureNormalǁloglikelihood__mutmut_9,
        "xǁMixtureNormalǁloglikelihood__mutmut_10": xǁMixtureNormalǁloglikelihood__mutmut_10,
        "xǁMixtureNormalǁloglikelihood__mutmut_11": xǁMixtureNormalǁloglikelihood__mutmut_11,
        "xǁMixtureNormalǁloglikelihood__mutmut_12": xǁMixtureNormalǁloglikelihood__mutmut_12,
        "xǁMixtureNormalǁloglikelihood__mutmut_13": xǁMixtureNormalǁloglikelihood__mutmut_13,
        "xǁMixtureNormalǁloglikelihood__mutmut_14": xǁMixtureNormalǁloglikelihood__mutmut_14,
        "xǁMixtureNormalǁloglikelihood__mutmut_15": xǁMixtureNormalǁloglikelihood__mutmut_15,
        "xǁMixtureNormalǁloglikelihood__mutmut_16": xǁMixtureNormalǁloglikelihood__mutmut_16,
        "xǁMixtureNormalǁloglikelihood__mutmut_17": xǁMixtureNormalǁloglikelihood__mutmut_17,
        "xǁMixtureNormalǁloglikelihood__mutmut_18": xǁMixtureNormalǁloglikelihood__mutmut_18,
        "xǁMixtureNormalǁloglikelihood__mutmut_19": xǁMixtureNormalǁloglikelihood__mutmut_19,
        "xǁMixtureNormalǁloglikelihood__mutmut_20": xǁMixtureNormalǁloglikelihood__mutmut_20,
        "xǁMixtureNormalǁloglikelihood__mutmut_21": xǁMixtureNormalǁloglikelihood__mutmut_21,
        "xǁMixtureNormalǁloglikelihood__mutmut_22": xǁMixtureNormalǁloglikelihood__mutmut_22,
        "xǁMixtureNormalǁloglikelihood__mutmut_23": xǁMixtureNormalǁloglikelihood__mutmut_23,
        "xǁMixtureNormalǁloglikelihood__mutmut_24": xǁMixtureNormalǁloglikelihood__mutmut_24,
        "xǁMixtureNormalǁloglikelihood__mutmut_25": xǁMixtureNormalǁloglikelihood__mutmut_25,
        "xǁMixtureNormalǁloglikelihood__mutmut_26": xǁMixtureNormalǁloglikelihood__mutmut_26,
        "xǁMixtureNormalǁloglikelihood__mutmut_27": xǁMixtureNormalǁloglikelihood__mutmut_27,
        "xǁMixtureNormalǁloglikelihood__mutmut_28": xǁMixtureNormalǁloglikelihood__mutmut_28,
        "xǁMixtureNormalǁloglikelihood__mutmut_29": xǁMixtureNormalǁloglikelihood__mutmut_29,
        "xǁMixtureNormalǁloglikelihood__mutmut_30": xǁMixtureNormalǁloglikelihood__mutmut_30,
        "xǁMixtureNormalǁloglikelihood__mutmut_31": xǁMixtureNormalǁloglikelihood__mutmut_31,
        "xǁMixtureNormalǁloglikelihood__mutmut_32": xǁMixtureNormalǁloglikelihood__mutmut_32,
        "xǁMixtureNormalǁloglikelihood__mutmut_33": xǁMixtureNormalǁloglikelihood__mutmut_33,
        "xǁMixtureNormalǁloglikelihood__mutmut_34": xǁMixtureNormalǁloglikelihood__mutmut_34,
        "xǁMixtureNormalǁloglikelihood__mutmut_35": xǁMixtureNormalǁloglikelihood__mutmut_35,
        "xǁMixtureNormalǁloglikelihood__mutmut_36": xǁMixtureNormalǁloglikelihood__mutmut_36,
        "xǁMixtureNormalǁloglikelihood__mutmut_37": xǁMixtureNormalǁloglikelihood__mutmut_37,
        "xǁMixtureNormalǁloglikelihood__mutmut_38": xǁMixtureNormalǁloglikelihood__mutmut_38,
        "xǁMixtureNormalǁloglikelihood__mutmut_39": xǁMixtureNormalǁloglikelihood__mutmut_39,
        "xǁMixtureNormalǁloglikelihood__mutmut_40": xǁMixtureNormalǁloglikelihood__mutmut_40,
        "xǁMixtureNormalǁloglikelihood__mutmut_41": xǁMixtureNormalǁloglikelihood__mutmut_41,
        "xǁMixtureNormalǁloglikelihood__mutmut_42": xǁMixtureNormalǁloglikelihood__mutmut_42,
        "xǁMixtureNormalǁloglikelihood__mutmut_43": xǁMixtureNormalǁloglikelihood__mutmut_43,
        "xǁMixtureNormalǁloglikelihood__mutmut_44": xǁMixtureNormalǁloglikelihood__mutmut_44,
        "xǁMixtureNormalǁloglikelihood__mutmut_45": xǁMixtureNormalǁloglikelihood__mutmut_45,
        "xǁMixtureNormalǁloglikelihood__mutmut_46": xǁMixtureNormalǁloglikelihood__mutmut_46,
        "xǁMixtureNormalǁloglikelihood__mutmut_47": xǁMixtureNormalǁloglikelihood__mutmut_47,
        "xǁMixtureNormalǁloglikelihood__mutmut_48": xǁMixtureNormalǁloglikelihood__mutmut_48,
        "xǁMixtureNormalǁloglikelihood__mutmut_49": xǁMixtureNormalǁloglikelihood__mutmut_49,
        "xǁMixtureNormalǁloglikelihood__mutmut_50": xǁMixtureNormalǁloglikelihood__mutmut_50,
        "xǁMixtureNormalǁloglikelihood__mutmut_51": xǁMixtureNormalǁloglikelihood__mutmut_51,
        "xǁMixtureNormalǁloglikelihood__mutmut_52": xǁMixtureNormalǁloglikelihood__mutmut_52,
        "xǁMixtureNormalǁloglikelihood__mutmut_53": xǁMixtureNormalǁloglikelihood__mutmut_53,
        "xǁMixtureNormalǁloglikelihood__mutmut_54": xǁMixtureNormalǁloglikelihood__mutmut_54,
        "xǁMixtureNormalǁloglikelihood__mutmut_55": xǁMixtureNormalǁloglikelihood__mutmut_55,
        "xǁMixtureNormalǁloglikelihood__mutmut_56": xǁMixtureNormalǁloglikelihood__mutmut_56,
        "xǁMixtureNormalǁloglikelihood__mutmut_57": xǁMixtureNormalǁloglikelihood__mutmut_57,
        "xǁMixtureNormalǁloglikelihood__mutmut_58": xǁMixtureNormalǁloglikelihood__mutmut_58,
        "xǁMixtureNormalǁloglikelihood__mutmut_59": xǁMixtureNormalǁloglikelihood__mutmut_59,
        "xǁMixtureNormalǁloglikelihood__mutmut_60": xǁMixtureNormalǁloglikelihood__mutmut_60,
        "xǁMixtureNormalǁloglikelihood__mutmut_61": xǁMixtureNormalǁloglikelihood__mutmut_61,
        "xǁMixtureNormalǁloglikelihood__mutmut_62": xǁMixtureNormalǁloglikelihood__mutmut_62,
        "xǁMixtureNormalǁloglikelihood__mutmut_63": xǁMixtureNormalǁloglikelihood__mutmut_63,
    }
    xǁMixtureNormalǁloglikelihood__mutmut_orig.__name__ = "xǁMixtureNormalǁloglikelihood"

    def ppf(self, q: float) -> float:
        args = [q]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁppf__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁppf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁppf__mutmut_orig(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_1(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) + q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_2(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(None) - q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_3(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = None  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_4(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(None, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_5(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, None, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_6(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, None)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_7(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(-50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_8(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_9(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
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

    def xǁMixtureNormalǁppf__mutmut_10(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, +50.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_11(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -51.0, 50.0)  # type: ignore[assignment]
        return result

    def xǁMixtureNormalǁppf__mutmut_12(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, 51.0)  # type: ignore[assignment]
        return result

    xǁMixtureNormalǁppf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁppf__mutmut_1": xǁMixtureNormalǁppf__mutmut_1,
        "xǁMixtureNormalǁppf__mutmut_2": xǁMixtureNormalǁppf__mutmut_2,
        "xǁMixtureNormalǁppf__mutmut_3": xǁMixtureNormalǁppf__mutmut_3,
        "xǁMixtureNormalǁppf__mutmut_4": xǁMixtureNormalǁppf__mutmut_4,
        "xǁMixtureNormalǁppf__mutmut_5": xǁMixtureNormalǁppf__mutmut_5,
        "xǁMixtureNormalǁppf__mutmut_6": xǁMixtureNormalǁppf__mutmut_6,
        "xǁMixtureNormalǁppf__mutmut_7": xǁMixtureNormalǁppf__mutmut_7,
        "xǁMixtureNormalǁppf__mutmut_8": xǁMixtureNormalǁppf__mutmut_8,
        "xǁMixtureNormalǁppf__mutmut_9": xǁMixtureNormalǁppf__mutmut_9,
        "xǁMixtureNormalǁppf__mutmut_10": xǁMixtureNormalǁppf__mutmut_10,
        "xǁMixtureNormalǁppf__mutmut_11": xǁMixtureNormalǁppf__mutmut_11,
        "xǁMixtureNormalǁppf__mutmut_12": xǁMixtureNormalǁppf__mutmut_12,
    }
    xǁMixtureNormalǁppf__mutmut_orig.__name__ = "xǁMixtureNormalǁppf"

    def cdf(self, x: float) -> float:
        args = [x]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁcdf__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁcdf__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁcdf__mutmut_orig(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_1(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = None
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_2(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = None

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_3(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(None, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_4(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, None)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_5(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_6(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(
            p,
        )

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_7(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(None)

    def xǁMixtureNormalǁcdf__mutmut_8(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) - (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_9(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p / stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_10(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(None, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_11(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=None) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_12(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_13(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p
            * stats.norm.cdf(
                x,
            )
            + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_14(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) / stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_15(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 + p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_16(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (2 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_17(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(None, scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_18(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=None))

    def xǁMixtureNormalǁcdf__mutmut_19(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(scale=sigma2_comp)
        )

    def xǁMixtureNormalǁcdf__mutmut_20(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1)
            + (1 - p)
            * stats.norm.cdf(
                x,
            )
        )

    xǁMixtureNormalǁcdf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁcdf__mutmut_1": xǁMixtureNormalǁcdf__mutmut_1,
        "xǁMixtureNormalǁcdf__mutmut_2": xǁMixtureNormalǁcdf__mutmut_2,
        "xǁMixtureNormalǁcdf__mutmut_3": xǁMixtureNormalǁcdf__mutmut_3,
        "xǁMixtureNormalǁcdf__mutmut_4": xǁMixtureNormalǁcdf__mutmut_4,
        "xǁMixtureNormalǁcdf__mutmut_5": xǁMixtureNormalǁcdf__mutmut_5,
        "xǁMixtureNormalǁcdf__mutmut_6": xǁMixtureNormalǁcdf__mutmut_6,
        "xǁMixtureNormalǁcdf__mutmut_7": xǁMixtureNormalǁcdf__mutmut_7,
        "xǁMixtureNormalǁcdf__mutmut_8": xǁMixtureNormalǁcdf__mutmut_8,
        "xǁMixtureNormalǁcdf__mutmut_9": xǁMixtureNormalǁcdf__mutmut_9,
        "xǁMixtureNormalǁcdf__mutmut_10": xǁMixtureNormalǁcdf__mutmut_10,
        "xǁMixtureNormalǁcdf__mutmut_11": xǁMixtureNormalǁcdf__mutmut_11,
        "xǁMixtureNormalǁcdf__mutmut_12": xǁMixtureNormalǁcdf__mutmut_12,
        "xǁMixtureNormalǁcdf__mutmut_13": xǁMixtureNormalǁcdf__mutmut_13,
        "xǁMixtureNormalǁcdf__mutmut_14": xǁMixtureNormalǁcdf__mutmut_14,
        "xǁMixtureNormalǁcdf__mutmut_15": xǁMixtureNormalǁcdf__mutmut_15,
        "xǁMixtureNormalǁcdf__mutmut_16": xǁMixtureNormalǁcdf__mutmut_16,
        "xǁMixtureNormalǁcdf__mutmut_17": xǁMixtureNormalǁcdf__mutmut_17,
        "xǁMixtureNormalǁcdf__mutmut_18": xǁMixtureNormalǁcdf__mutmut_18,
        "xǁMixtureNormalǁcdf__mutmut_19": xǁMixtureNormalǁcdf__mutmut_19,
        "xǁMixtureNormalǁcdf__mutmut_20": xǁMixtureNormalǁcdf__mutmut_20,
    }
    xǁMixtureNormalǁcdf__mutmut_orig.__name__ = "xǁMixtureNormalǁcdf"

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        args = [n, rng, dist_params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁsimulate__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁsimulate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁsimulate__mutmut_orig(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_1(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = None
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_2(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(None)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_3(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = None

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_4(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(None, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_5(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, None)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_6(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_7(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(
            p,
        )

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_8(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = None
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_9(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=None) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_10(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) <= p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_11(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = None
        return z

    def xǁMixtureNormalǁsimulate__mutmut_12(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            None,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_13(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            None,
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_14(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            None,
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_15(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_16(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_17(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_18(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(None, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_19(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, None, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_20(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=None),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_21(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_22(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_23(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(
                0,
                sigma1,
            ),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_24(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(1, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_25(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(None, sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_26(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, None, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_27(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=None),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_28(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(sigma2_comp, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_29(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, size=n),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_30(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(
                0,
                sigma2_comp,
            ),
        )
        return z

    def xǁMixtureNormalǁsimulate__mutmut_31(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(1, sigma2_comp, size=n),
        )
        return z

    xǁMixtureNormalǁsimulate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁsimulate__mutmut_1": xǁMixtureNormalǁsimulate__mutmut_1,
        "xǁMixtureNormalǁsimulate__mutmut_2": xǁMixtureNormalǁsimulate__mutmut_2,
        "xǁMixtureNormalǁsimulate__mutmut_3": xǁMixtureNormalǁsimulate__mutmut_3,
        "xǁMixtureNormalǁsimulate__mutmut_4": xǁMixtureNormalǁsimulate__mutmut_4,
        "xǁMixtureNormalǁsimulate__mutmut_5": xǁMixtureNormalǁsimulate__mutmut_5,
        "xǁMixtureNormalǁsimulate__mutmut_6": xǁMixtureNormalǁsimulate__mutmut_6,
        "xǁMixtureNormalǁsimulate__mutmut_7": xǁMixtureNormalǁsimulate__mutmut_7,
        "xǁMixtureNormalǁsimulate__mutmut_8": xǁMixtureNormalǁsimulate__mutmut_8,
        "xǁMixtureNormalǁsimulate__mutmut_9": xǁMixtureNormalǁsimulate__mutmut_9,
        "xǁMixtureNormalǁsimulate__mutmut_10": xǁMixtureNormalǁsimulate__mutmut_10,
        "xǁMixtureNormalǁsimulate__mutmut_11": xǁMixtureNormalǁsimulate__mutmut_11,
        "xǁMixtureNormalǁsimulate__mutmut_12": xǁMixtureNormalǁsimulate__mutmut_12,
        "xǁMixtureNormalǁsimulate__mutmut_13": xǁMixtureNormalǁsimulate__mutmut_13,
        "xǁMixtureNormalǁsimulate__mutmut_14": xǁMixtureNormalǁsimulate__mutmut_14,
        "xǁMixtureNormalǁsimulate__mutmut_15": xǁMixtureNormalǁsimulate__mutmut_15,
        "xǁMixtureNormalǁsimulate__mutmut_16": xǁMixtureNormalǁsimulate__mutmut_16,
        "xǁMixtureNormalǁsimulate__mutmut_17": xǁMixtureNormalǁsimulate__mutmut_17,
        "xǁMixtureNormalǁsimulate__mutmut_18": xǁMixtureNormalǁsimulate__mutmut_18,
        "xǁMixtureNormalǁsimulate__mutmut_19": xǁMixtureNormalǁsimulate__mutmut_19,
        "xǁMixtureNormalǁsimulate__mutmut_20": xǁMixtureNormalǁsimulate__mutmut_20,
        "xǁMixtureNormalǁsimulate__mutmut_21": xǁMixtureNormalǁsimulate__mutmut_21,
        "xǁMixtureNormalǁsimulate__mutmut_22": xǁMixtureNormalǁsimulate__mutmut_22,
        "xǁMixtureNormalǁsimulate__mutmut_23": xǁMixtureNormalǁsimulate__mutmut_23,
        "xǁMixtureNormalǁsimulate__mutmut_24": xǁMixtureNormalǁsimulate__mutmut_24,
        "xǁMixtureNormalǁsimulate__mutmut_25": xǁMixtureNormalǁsimulate__mutmut_25,
        "xǁMixtureNormalǁsimulate__mutmut_26": xǁMixtureNormalǁsimulate__mutmut_26,
        "xǁMixtureNormalǁsimulate__mutmut_27": xǁMixtureNormalǁsimulate__mutmut_27,
        "xǁMixtureNormalǁsimulate__mutmut_28": xǁMixtureNormalǁsimulate__mutmut_28,
        "xǁMixtureNormalǁsimulate__mutmut_29": xǁMixtureNormalǁsimulate__mutmut_29,
        "xǁMixtureNormalǁsimulate__mutmut_30": xǁMixtureNormalǁsimulate__mutmut_30,
        "xǁMixtureNormalǁsimulate__mutmut_31": xǁMixtureNormalǁsimulate__mutmut_31,
    }
    xǁMixtureNormalǁsimulate__mutmut_orig.__name__ = "xǁMixtureNormalǁsimulate"

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) != 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 1:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = None
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = None
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 1
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is not None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = None
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 * (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 2.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 - np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (2.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(None))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(+unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx = 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx -= 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 2
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_17(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is not None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_18(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = None
        return constrained

    def xǁMixtureNormalǁtransform_params__mutmut_19(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(None)
        return constrained

    xǁMixtureNormalǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁtransform_params__mutmut_1": xǁMixtureNormalǁtransform_params__mutmut_1,
        "xǁMixtureNormalǁtransform_params__mutmut_2": xǁMixtureNormalǁtransform_params__mutmut_2,
        "xǁMixtureNormalǁtransform_params__mutmut_3": xǁMixtureNormalǁtransform_params__mutmut_3,
        "xǁMixtureNormalǁtransform_params__mutmut_4": xǁMixtureNormalǁtransform_params__mutmut_4,
        "xǁMixtureNormalǁtransform_params__mutmut_5": xǁMixtureNormalǁtransform_params__mutmut_5,
        "xǁMixtureNormalǁtransform_params__mutmut_6": xǁMixtureNormalǁtransform_params__mutmut_6,
        "xǁMixtureNormalǁtransform_params__mutmut_7": xǁMixtureNormalǁtransform_params__mutmut_7,
        "xǁMixtureNormalǁtransform_params__mutmut_8": xǁMixtureNormalǁtransform_params__mutmut_8,
        "xǁMixtureNormalǁtransform_params__mutmut_9": xǁMixtureNormalǁtransform_params__mutmut_9,
        "xǁMixtureNormalǁtransform_params__mutmut_10": xǁMixtureNormalǁtransform_params__mutmut_10,
        "xǁMixtureNormalǁtransform_params__mutmut_11": xǁMixtureNormalǁtransform_params__mutmut_11,
        "xǁMixtureNormalǁtransform_params__mutmut_12": xǁMixtureNormalǁtransform_params__mutmut_12,
        "xǁMixtureNormalǁtransform_params__mutmut_13": xǁMixtureNormalǁtransform_params__mutmut_13,
        "xǁMixtureNormalǁtransform_params__mutmut_14": xǁMixtureNormalǁtransform_params__mutmut_14,
        "xǁMixtureNormalǁtransform_params__mutmut_15": xǁMixtureNormalǁtransform_params__mutmut_15,
        "xǁMixtureNormalǁtransform_params__mutmut_16": xǁMixtureNormalǁtransform_params__mutmut_16,
        "xǁMixtureNormalǁtransform_params__mutmut_17": xǁMixtureNormalǁtransform_params__mutmut_17,
        "xǁMixtureNormalǁtransform_params__mutmut_18": xǁMixtureNormalǁtransform_params__mutmut_18,
        "xǁMixtureNormalǁtransform_params__mutmut_19": xǁMixtureNormalǁtransform_params__mutmut_19,
    }
    xǁMixtureNormalǁtransform_params__mutmut_orig.__name__ = "xǁMixtureNormalǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) != 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 1:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = None
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = None
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 1
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is not None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = None
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(None)
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(None, 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], None, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, None))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(
                np.clip(
                    constrained[idx],
                    1e-6,
                )
            )
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1.000001, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 + 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 2 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1.000001))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = None
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(None)
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p * (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 + p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (2.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx = 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx -= 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 2
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is not None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = None
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_29(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(None)
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_30(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(None, 1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_31(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], None))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_32(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(1e-6))
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_33(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(
                max(
                    constrained[idx],
                )
            )
        return unconstrained

    def xǁMixtureNormalǁuntransform_params__mutmut_34(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1.000001))
        return unconstrained

    xǁMixtureNormalǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁuntransform_params__mutmut_1": xǁMixtureNormalǁuntransform_params__mutmut_1,
        "xǁMixtureNormalǁuntransform_params__mutmut_2": xǁMixtureNormalǁuntransform_params__mutmut_2,
        "xǁMixtureNormalǁuntransform_params__mutmut_3": xǁMixtureNormalǁuntransform_params__mutmut_3,
        "xǁMixtureNormalǁuntransform_params__mutmut_4": xǁMixtureNormalǁuntransform_params__mutmut_4,
        "xǁMixtureNormalǁuntransform_params__mutmut_5": xǁMixtureNormalǁuntransform_params__mutmut_5,
        "xǁMixtureNormalǁuntransform_params__mutmut_6": xǁMixtureNormalǁuntransform_params__mutmut_6,
        "xǁMixtureNormalǁuntransform_params__mutmut_7": xǁMixtureNormalǁuntransform_params__mutmut_7,
        "xǁMixtureNormalǁuntransform_params__mutmut_8": xǁMixtureNormalǁuntransform_params__mutmut_8,
        "xǁMixtureNormalǁuntransform_params__mutmut_9": xǁMixtureNormalǁuntransform_params__mutmut_9,
        "xǁMixtureNormalǁuntransform_params__mutmut_10": xǁMixtureNormalǁuntransform_params__mutmut_10,
        "xǁMixtureNormalǁuntransform_params__mutmut_11": xǁMixtureNormalǁuntransform_params__mutmut_11,
        "xǁMixtureNormalǁuntransform_params__mutmut_12": xǁMixtureNormalǁuntransform_params__mutmut_12,
        "xǁMixtureNormalǁuntransform_params__mutmut_13": xǁMixtureNormalǁuntransform_params__mutmut_13,
        "xǁMixtureNormalǁuntransform_params__mutmut_14": xǁMixtureNormalǁuntransform_params__mutmut_14,
        "xǁMixtureNormalǁuntransform_params__mutmut_15": xǁMixtureNormalǁuntransform_params__mutmut_15,
        "xǁMixtureNormalǁuntransform_params__mutmut_16": xǁMixtureNormalǁuntransform_params__mutmut_16,
        "xǁMixtureNormalǁuntransform_params__mutmut_17": xǁMixtureNormalǁuntransform_params__mutmut_17,
        "xǁMixtureNormalǁuntransform_params__mutmut_18": xǁMixtureNormalǁuntransform_params__mutmut_18,
        "xǁMixtureNormalǁuntransform_params__mutmut_19": xǁMixtureNormalǁuntransform_params__mutmut_19,
        "xǁMixtureNormalǁuntransform_params__mutmut_20": xǁMixtureNormalǁuntransform_params__mutmut_20,
        "xǁMixtureNormalǁuntransform_params__mutmut_21": xǁMixtureNormalǁuntransform_params__mutmut_21,
        "xǁMixtureNormalǁuntransform_params__mutmut_22": xǁMixtureNormalǁuntransform_params__mutmut_22,
        "xǁMixtureNormalǁuntransform_params__mutmut_23": xǁMixtureNormalǁuntransform_params__mutmut_23,
        "xǁMixtureNormalǁuntransform_params__mutmut_24": xǁMixtureNormalǁuntransform_params__mutmut_24,
        "xǁMixtureNormalǁuntransform_params__mutmut_25": xǁMixtureNormalǁuntransform_params__mutmut_25,
        "xǁMixtureNormalǁuntransform_params__mutmut_26": xǁMixtureNormalǁuntransform_params__mutmut_26,
        "xǁMixtureNormalǁuntransform_params__mutmut_27": xǁMixtureNormalǁuntransform_params__mutmut_27,
        "xǁMixtureNormalǁuntransform_params__mutmut_28": xǁMixtureNormalǁuntransform_params__mutmut_28,
        "xǁMixtureNormalǁuntransform_params__mutmut_29": xǁMixtureNormalǁuntransform_params__mutmut_29,
        "xǁMixtureNormalǁuntransform_params__mutmut_30": xǁMixtureNormalǁuntransform_params__mutmut_30,
        "xǁMixtureNormalǁuntransform_params__mutmut_31": xǁMixtureNormalǁuntransform_params__mutmut_31,
        "xǁMixtureNormalǁuntransform_params__mutmut_32": xǁMixtureNormalǁuntransform_params__mutmut_32,
        "xǁMixtureNormalǁuntransform_params__mutmut_33": xǁMixtureNormalǁuntransform_params__mutmut_33,
        "xǁMixtureNormalǁuntransform_params__mutmut_34": xǁMixtureNormalǁuntransform_params__mutmut_34,
    }
    xǁMixtureNormalǁuntransform_params__mutmut_orig.__name__ = "xǁMixtureNormalǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMixtureNormalǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁMixtureNormalǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMixtureNormalǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = None
        if self._fixed_p is None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is not None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append(None)
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((1.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((0.01, 1.99))
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is not None:
            bnds.append((0.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append(None)
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append((1.01, 5.0))
        return bnds

    def xǁMixtureNormalǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 6.0))
        return bnds

    xǁMixtureNormalǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMixtureNormalǁbounds__mutmut_1": xǁMixtureNormalǁbounds__mutmut_1,
        "xǁMixtureNormalǁbounds__mutmut_2": xǁMixtureNormalǁbounds__mutmut_2,
        "xǁMixtureNormalǁbounds__mutmut_3": xǁMixtureNormalǁbounds__mutmut_3,
        "xǁMixtureNormalǁbounds__mutmut_4": xǁMixtureNormalǁbounds__mutmut_4,
        "xǁMixtureNormalǁbounds__mutmut_5": xǁMixtureNormalǁbounds__mutmut_5,
        "xǁMixtureNormalǁbounds__mutmut_6": xǁMixtureNormalǁbounds__mutmut_6,
        "xǁMixtureNormalǁbounds__mutmut_7": xǁMixtureNormalǁbounds__mutmut_7,
        "xǁMixtureNormalǁbounds__mutmut_8": xǁMixtureNormalǁbounds__mutmut_8,
        "xǁMixtureNormalǁbounds__mutmut_9": xǁMixtureNormalǁbounds__mutmut_9,
    }
    xǁMixtureNormalǁbounds__mutmut_orig.__name__ = "xǁMixtureNormalǁbounds"
