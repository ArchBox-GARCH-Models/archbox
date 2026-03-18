"""IGARCH - Integrated GARCH model (Engle & Bollerslev, 1986).

sigma^2_t = omega + alpha * eps^2_{t-1} + (1 - alpha) * sigma^2_{t-1}

Persistencia = 1 (alpha + beta = 1, beta = 1 - alpha).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel

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


class IGARCH(VolatilityModel):
    """Integrated GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.

    Notes
    -----
    IGARCH(1,1) has persistence = 1 (alpha + beta = 1).
    beta = 1 - alpha is enforced internally.
    The unconditional variance does not exist (infinite),
    but forecasts are still finite.
    """

    volatility_process = "IGARCH"

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        args = [endog, mean, dist]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁIGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁIGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁIGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = None
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 2
        self.q = 1
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = None
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 2
        super().__init__(endog, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(None, mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=None, dist=dist)

    def xǁIGARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, mean=mean, dist=None)

    def xǁIGARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(mean=mean, dist=dist)

    def xǁIGARCHǁ__init____mutmut_13(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(endog, dist=dist)

    def xǁIGARCHǁ__init____mutmut_14(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize IGARCH model with options."""
        self.p = 1
        self.q = 1
        super().__init__(
            endog,
            mean=mean,
        )

    xǁIGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁIGARCHǁ__init____mutmut_1": xǁIGARCHǁ__init____mutmut_1,
        "xǁIGARCHǁ__init____mutmut_2": xǁIGARCHǁ__init____mutmut_2,
        "xǁIGARCHǁ__init____mutmut_3": xǁIGARCHǁ__init____mutmut_3,
        "xǁIGARCHǁ__init____mutmut_4": xǁIGARCHǁ__init____mutmut_4,
        "xǁIGARCHǁ__init____mutmut_5": xǁIGARCHǁ__init____mutmut_5,
        "xǁIGARCHǁ__init____mutmut_6": xǁIGARCHǁ__init____mutmut_6,
        "xǁIGARCHǁ__init____mutmut_7": xǁIGARCHǁ__init____mutmut_7,
        "xǁIGARCHǁ__init____mutmut_8": xǁIGARCHǁ__init____mutmut_8,
        "xǁIGARCHǁ__init____mutmut_9": xǁIGARCHǁ__init____mutmut_9,
        "xǁIGARCHǁ__init____mutmut_10": xǁIGARCHǁ__init____mutmut_10,
        "xǁIGARCHǁ__init____mutmut_11": xǁIGARCHǁ__init____mutmut_11,
        "xǁIGARCHǁ__init____mutmut_12": xǁIGARCHǁ__init____mutmut_12,
        "xǁIGARCHǁ__init____mutmut_13": xǁIGARCHǁ__init____mutmut_13,
        "xǁIGARCHǁ__init____mutmut_14": xǁIGARCHǁ__init____mutmut_14,
    }
    xǁIGARCHǁ__init____mutmut_orig.__name__ = "xǁIGARCHǁ__init__"

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁIGARCHǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁIGARCHǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁIGARCHǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = None
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[1]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = None
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[2]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = None

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 + alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 2.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = None
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = None

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(None)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(None):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t != 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 1:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = None
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast - beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega - alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha / backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta / backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = None
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 - beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega - alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha / resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] * 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t + 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 2] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 3 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta / sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t + 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 2]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = None

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(None, 1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], None)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(1e-12)

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(
                sigma2[t],
            )

        return sigma2

    def xǁIGARCHǁ_variance_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via IGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha]. beta = 1 - alpha enforced internally.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series.
        """
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            if t == 0:
                sigma2[t] = omega + alpha * backcast + beta * backcast
            else:
                sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
            sigma2[t] = max(sigma2[t], 1.000000000001)

        return sigma2

    xǁIGARCHǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁIGARCHǁ_variance_recursion__mutmut_1": xǁIGARCHǁ_variance_recursion__mutmut_1,
        "xǁIGARCHǁ_variance_recursion__mutmut_2": xǁIGARCHǁ_variance_recursion__mutmut_2,
        "xǁIGARCHǁ_variance_recursion__mutmut_3": xǁIGARCHǁ_variance_recursion__mutmut_3,
        "xǁIGARCHǁ_variance_recursion__mutmut_4": xǁIGARCHǁ_variance_recursion__mutmut_4,
        "xǁIGARCHǁ_variance_recursion__mutmut_5": xǁIGARCHǁ_variance_recursion__mutmut_5,
        "xǁIGARCHǁ_variance_recursion__mutmut_6": xǁIGARCHǁ_variance_recursion__mutmut_6,
        "xǁIGARCHǁ_variance_recursion__mutmut_7": xǁIGARCHǁ_variance_recursion__mutmut_7,
        "xǁIGARCHǁ_variance_recursion__mutmut_8": xǁIGARCHǁ_variance_recursion__mutmut_8,
        "xǁIGARCHǁ_variance_recursion__mutmut_9": xǁIGARCHǁ_variance_recursion__mutmut_9,
        "xǁIGARCHǁ_variance_recursion__mutmut_10": xǁIGARCHǁ_variance_recursion__mutmut_10,
        "xǁIGARCHǁ_variance_recursion__mutmut_11": xǁIGARCHǁ_variance_recursion__mutmut_11,
        "xǁIGARCHǁ_variance_recursion__mutmut_12": xǁIGARCHǁ_variance_recursion__mutmut_12,
        "xǁIGARCHǁ_variance_recursion__mutmut_13": xǁIGARCHǁ_variance_recursion__mutmut_13,
        "xǁIGARCHǁ_variance_recursion__mutmut_14": xǁIGARCHǁ_variance_recursion__mutmut_14,
        "xǁIGARCHǁ_variance_recursion__mutmut_15": xǁIGARCHǁ_variance_recursion__mutmut_15,
        "xǁIGARCHǁ_variance_recursion__mutmut_16": xǁIGARCHǁ_variance_recursion__mutmut_16,
        "xǁIGARCHǁ_variance_recursion__mutmut_17": xǁIGARCHǁ_variance_recursion__mutmut_17,
        "xǁIGARCHǁ_variance_recursion__mutmut_18": xǁIGARCHǁ_variance_recursion__mutmut_18,
        "xǁIGARCHǁ_variance_recursion__mutmut_19": xǁIGARCHǁ_variance_recursion__mutmut_19,
        "xǁIGARCHǁ_variance_recursion__mutmut_20": xǁIGARCHǁ_variance_recursion__mutmut_20,
        "xǁIGARCHǁ_variance_recursion__mutmut_21": xǁIGARCHǁ_variance_recursion__mutmut_21,
        "xǁIGARCHǁ_variance_recursion__mutmut_22": xǁIGARCHǁ_variance_recursion__mutmut_22,
        "xǁIGARCHǁ_variance_recursion__mutmut_23": xǁIGARCHǁ_variance_recursion__mutmut_23,
        "xǁIGARCHǁ_variance_recursion__mutmut_24": xǁIGARCHǁ_variance_recursion__mutmut_24,
        "xǁIGARCHǁ_variance_recursion__mutmut_25": xǁIGARCHǁ_variance_recursion__mutmut_25,
        "xǁIGARCHǁ_variance_recursion__mutmut_26": xǁIGARCHǁ_variance_recursion__mutmut_26,
        "xǁIGARCHǁ_variance_recursion__mutmut_27": xǁIGARCHǁ_variance_recursion__mutmut_27,
        "xǁIGARCHǁ_variance_recursion__mutmut_28": xǁIGARCHǁ_variance_recursion__mutmut_28,
        "xǁIGARCHǁ_variance_recursion__mutmut_29": xǁIGARCHǁ_variance_recursion__mutmut_29,
        "xǁIGARCHǁ_variance_recursion__mutmut_30": xǁIGARCHǁ_variance_recursion__mutmut_30,
        "xǁIGARCHǁ_variance_recursion__mutmut_31": xǁIGARCHǁ_variance_recursion__mutmut_31,
        "xǁIGARCHǁ_variance_recursion__mutmut_32": xǁIGARCHǁ_variance_recursion__mutmut_32,
        "xǁIGARCHǁ_variance_recursion__mutmut_33": xǁIGARCHǁ_variance_recursion__mutmut_33,
        "xǁIGARCHǁ_variance_recursion__mutmut_34": xǁIGARCHǁ_variance_recursion__mutmut_34,
        "xǁIGARCHǁ_variance_recursion__mutmut_35": xǁIGARCHǁ_variance_recursion__mutmut_35,
    }
    xǁIGARCHǁ_variance_recursion__mutmut_orig.__name__ = "xǁIGARCHǁ_variance_recursion"

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁIGARCHǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁIGARCHǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁIGARCHǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = None
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[1]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = None
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[2]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = None
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 + alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 2.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = None
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 - beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega - alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha / eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps * 2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**3 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta / sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(None)

    def xǁIGARCHǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(None, 1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, None))

    def xǁIGARCHǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(1e-12))

    def xǁIGARCHǁ_one_step_variance__mutmut_19(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(
            max(
                sigma2,
            )
        )

    def xǁIGARCHǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = 1.0 - alpha
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1.000000000001))

    xǁIGARCHǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁIGARCHǁ_one_step_variance__mutmut_1": xǁIGARCHǁ_one_step_variance__mutmut_1,
        "xǁIGARCHǁ_one_step_variance__mutmut_2": xǁIGARCHǁ_one_step_variance__mutmut_2,
        "xǁIGARCHǁ_one_step_variance__mutmut_3": xǁIGARCHǁ_one_step_variance__mutmut_3,
        "xǁIGARCHǁ_one_step_variance__mutmut_4": xǁIGARCHǁ_one_step_variance__mutmut_4,
        "xǁIGARCHǁ_one_step_variance__mutmut_5": xǁIGARCHǁ_one_step_variance__mutmut_5,
        "xǁIGARCHǁ_one_step_variance__mutmut_6": xǁIGARCHǁ_one_step_variance__mutmut_6,
        "xǁIGARCHǁ_one_step_variance__mutmut_7": xǁIGARCHǁ_one_step_variance__mutmut_7,
        "xǁIGARCHǁ_one_step_variance__mutmut_8": xǁIGARCHǁ_one_step_variance__mutmut_8,
        "xǁIGARCHǁ_one_step_variance__mutmut_9": xǁIGARCHǁ_one_step_variance__mutmut_9,
        "xǁIGARCHǁ_one_step_variance__mutmut_10": xǁIGARCHǁ_one_step_variance__mutmut_10,
        "xǁIGARCHǁ_one_step_variance__mutmut_11": xǁIGARCHǁ_one_step_variance__mutmut_11,
        "xǁIGARCHǁ_one_step_variance__mutmut_12": xǁIGARCHǁ_one_step_variance__mutmut_12,
        "xǁIGARCHǁ_one_step_variance__mutmut_13": xǁIGARCHǁ_one_step_variance__mutmut_13,
        "xǁIGARCHǁ_one_step_variance__mutmut_14": xǁIGARCHǁ_one_step_variance__mutmut_14,
        "xǁIGARCHǁ_one_step_variance__mutmut_15": xǁIGARCHǁ_one_step_variance__mutmut_15,
        "xǁIGARCHǁ_one_step_variance__mutmut_16": xǁIGARCHǁ_one_step_variance__mutmut_16,
        "xǁIGARCHǁ_one_step_variance__mutmut_17": xǁIGARCHǁ_one_step_variance__mutmut_17,
        "xǁIGARCHǁ_one_step_variance__mutmut_18": xǁIGARCHǁ_one_step_variance__mutmut_18,
        "xǁIGARCHǁ_one_step_variance__mutmut_19": xǁIGARCHǁ_one_step_variance__mutmut_19,
        "xǁIGARCHǁ_one_step_variance__mutmut_20": xǁIGARCHǁ_one_step_variance__mutmut_20,
    }
    xǁIGARCHǁ_one_step_variance__mutmut_orig.__name__ = "xǁIGARCHǁ_one_step_variance"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        var = np.var(self.endog)
        omega = var * 0.005
        alpha = 0.05
        return np.array([omega, alpha])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        return ["omega", "alpha"]

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁIGARCHǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁIGARCHǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁIGARCHǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = None
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = None
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[1] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(None)
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[1])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = None
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 * (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 2.0 / (1.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 - np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (2.0 + np.exp(-unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(None))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(+unconstrained[1]))
        return constrained

    def xǁIGARCHǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, 0 < alpha < 1.
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # 0 < alpha < 1 via sigmoid
        constrained[1] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        return constrained

    xǁIGARCHǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁIGARCHǁtransform_params__mutmut_1": xǁIGARCHǁtransform_params__mutmut_1,
        "xǁIGARCHǁtransform_params__mutmut_2": xǁIGARCHǁtransform_params__mutmut_2,
        "xǁIGARCHǁtransform_params__mutmut_3": xǁIGARCHǁtransform_params__mutmut_3,
        "xǁIGARCHǁtransform_params__mutmut_4": xǁIGARCHǁtransform_params__mutmut_4,
        "xǁIGARCHǁtransform_params__mutmut_5": xǁIGARCHǁtransform_params__mutmut_5,
        "xǁIGARCHǁtransform_params__mutmut_6": xǁIGARCHǁtransform_params__mutmut_6,
        "xǁIGARCHǁtransform_params__mutmut_7": xǁIGARCHǁtransform_params__mutmut_7,
        "xǁIGARCHǁtransform_params__mutmut_8": xǁIGARCHǁtransform_params__mutmut_8,
        "xǁIGARCHǁtransform_params__mutmut_9": xǁIGARCHǁtransform_params__mutmut_9,
        "xǁIGARCHǁtransform_params__mutmut_10": xǁIGARCHǁtransform_params__mutmut_10,
        "xǁIGARCHǁtransform_params__mutmut_11": xǁIGARCHǁtransform_params__mutmut_11,
        "xǁIGARCHǁtransform_params__mutmut_12": xǁIGARCHǁtransform_params__mutmut_12,
        "xǁIGARCHǁtransform_params__mutmut_13": xǁIGARCHǁtransform_params__mutmut_13,
        "xǁIGARCHǁtransform_params__mutmut_14": xǁIGARCHǁtransform_params__mutmut_14,
    }
    xǁIGARCHǁtransform_params__mutmut_orig.__name__ = "xǁIGARCHǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁIGARCHǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁIGARCHǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁIGARCHǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = None
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = None
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[1] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(None)
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(None, 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], None))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(
            max(
                constrained[0],
            )
        )
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[1], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1.000000000001))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = None
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(None, 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], None, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, None)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(
            constrained[1],
            1e-6,
        )
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1.000001, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 + 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 2 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1.000001)
        unconstrained[1] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = None
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(alpha_clipped / (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(None)
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped * (1.0 - alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (1.0 + alpha_clipped))
        return unconstrained

    def xǁIGARCHǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # inverse sigmoid
        alpha_clipped = np.clip(constrained[1], 1e-6, 1 - 1e-6)
        unconstrained[1] = np.log(alpha_clipped / (2.0 - alpha_clipped))
        return unconstrained

    xǁIGARCHǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁIGARCHǁuntransform_params__mutmut_1": xǁIGARCHǁuntransform_params__mutmut_1,
        "xǁIGARCHǁuntransform_params__mutmut_2": xǁIGARCHǁuntransform_params__mutmut_2,
        "xǁIGARCHǁuntransform_params__mutmut_3": xǁIGARCHǁuntransform_params__mutmut_3,
        "xǁIGARCHǁuntransform_params__mutmut_4": xǁIGARCHǁuntransform_params__mutmut_4,
        "xǁIGARCHǁuntransform_params__mutmut_5": xǁIGARCHǁuntransform_params__mutmut_5,
        "xǁIGARCHǁuntransform_params__mutmut_6": xǁIGARCHǁuntransform_params__mutmut_6,
        "xǁIGARCHǁuntransform_params__mutmut_7": xǁIGARCHǁuntransform_params__mutmut_7,
        "xǁIGARCHǁuntransform_params__mutmut_8": xǁIGARCHǁuntransform_params__mutmut_8,
        "xǁIGARCHǁuntransform_params__mutmut_9": xǁIGARCHǁuntransform_params__mutmut_9,
        "xǁIGARCHǁuntransform_params__mutmut_10": xǁIGARCHǁuntransform_params__mutmut_10,
        "xǁIGARCHǁuntransform_params__mutmut_11": xǁIGARCHǁuntransform_params__mutmut_11,
        "xǁIGARCHǁuntransform_params__mutmut_12": xǁIGARCHǁuntransform_params__mutmut_12,
        "xǁIGARCHǁuntransform_params__mutmut_13": xǁIGARCHǁuntransform_params__mutmut_13,
        "xǁIGARCHǁuntransform_params__mutmut_14": xǁIGARCHǁuntransform_params__mutmut_14,
        "xǁIGARCHǁuntransform_params__mutmut_15": xǁIGARCHǁuntransform_params__mutmut_15,
        "xǁIGARCHǁuntransform_params__mutmut_16": xǁIGARCHǁuntransform_params__mutmut_16,
        "xǁIGARCHǁuntransform_params__mutmut_17": xǁIGARCHǁuntransform_params__mutmut_17,
        "xǁIGARCHǁuntransform_params__mutmut_18": xǁIGARCHǁuntransform_params__mutmut_18,
        "xǁIGARCHǁuntransform_params__mutmut_19": xǁIGARCHǁuntransform_params__mutmut_19,
        "xǁIGARCHǁuntransform_params__mutmut_20": xǁIGARCHǁuntransform_params__mutmut_20,
        "xǁIGARCHǁuntransform_params__mutmut_21": xǁIGARCHǁuntransform_params__mutmut_21,
        "xǁIGARCHǁuntransform_params__mutmut_22": xǁIGARCHǁuntransform_params__mutmut_22,
        "xǁIGARCHǁuntransform_params__mutmut_23": xǁIGARCHǁuntransform_params__mutmut_23,
        "xǁIGARCHǁuntransform_params__mutmut_24": xǁIGARCHǁuntransform_params__mutmut_24,
        "xǁIGARCHǁuntransform_params__mutmut_25": xǁIGARCHǁuntransform_params__mutmut_25,
        "xǁIGARCHǁuntransform_params__mutmut_26": xǁIGARCHǁuntransform_params__mutmut_26,
        "xǁIGARCHǁuntransform_params__mutmut_27": xǁIGARCHǁuntransform_params__mutmut_27,
        "xǁIGARCHǁuntransform_params__mutmut_28": xǁIGARCHǁuntransform_params__mutmut_28,
    }
    xǁIGARCHǁuntransform_params__mutmut_orig.__name__ = "xǁIGARCHǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁIGARCHǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁIGARCHǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁIGARCHǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.001, 0.999),  # 0 < alpha < 1
        ]

    def xǁIGARCHǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1.000000000001, np.inf),  # omega > 0
            (0.001, 0.999),  # 0 < alpha < 1
        ]

    def xǁIGARCHǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (1.001, 0.999),  # 0 < alpha < 1
        ]

    def xǁIGARCHǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.001, 1.999),  # 0 < alpha < 1
        ]

    xǁIGARCHǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁIGARCHǁbounds__mutmut_1": xǁIGARCHǁbounds__mutmut_1,
        "xǁIGARCHǁbounds__mutmut_2": xǁIGARCHǁbounds__mutmut_2,
        "xǁIGARCHǁbounds__mutmut_3": xǁIGARCHǁbounds__mutmut_3,
    }
    xǁIGARCHǁbounds__mutmut_orig.__name__ = "xǁIGARCHǁbounds"

    @property
    def num_params(self) -> int:
        """Number of model parameters (omega, alpha). beta = 1-alpha is implicit."""
        return 2
