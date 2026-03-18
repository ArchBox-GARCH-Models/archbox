"""GARCH(p,q) volatility model - Bollerslev (1986)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel
from archbox.utils.validation import validate_positive_integer

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


class GARCH(VolatilityModel):
    """GARCH(p,q) model.

    sigma^2_t = omega + sum_{i=1}^q alpha_i * eps^2_{t-i}
                      + sum_{j=1}^p beta_j * sigma^2_{t-j}

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of GARCH (lagged variance) terms. Default 1.
    q : int
        Number of ARCH (lagged squared residual) terms. Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution: 'normal'.

    Examples
    --------
    >>> from archbox import GARCH
    >>> from archbox.datasets import load_dataset
    >>> sp500 = load_dataset('sp500')
    >>> model = GARCH(sp500['returns'], p=1, q=1)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    volatility_process: str = "GARCH"

    def __init__(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        args = [endog, p, q, mean, dist]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        p: int = 2,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        p: int = 1,
        q: int = 2,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = None
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(None, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, None)
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer("p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(
            p,
        )
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "XXpXX")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_13(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "P")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_14(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = None
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_15(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(None, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_16(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, None)
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_17(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer("q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_18(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(
            q,
        )
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_19(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "XXqXX")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_20(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "Q")
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_21(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(None, mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_22(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=None, dist=dist)

    def xǁGARCHǁ__init____mutmut_23(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=None)

    def xǁGARCHǁ__init____mutmut_24(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(mean=mean, dist=dist)

    def xǁGARCHǁ__init____mutmut_25(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, dist=dist)

    def xǁGARCHǁ__init____mutmut_26(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(
            endog,
            mean=mean,
        )

    xǁGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHǁ__init____mutmut_1": xǁGARCHǁ__init____mutmut_1,
        "xǁGARCHǁ__init____mutmut_2": xǁGARCHǁ__init____mutmut_2,
        "xǁGARCHǁ__init____mutmut_3": xǁGARCHǁ__init____mutmut_3,
        "xǁGARCHǁ__init____mutmut_4": xǁGARCHǁ__init____mutmut_4,
        "xǁGARCHǁ__init____mutmut_5": xǁGARCHǁ__init____mutmut_5,
        "xǁGARCHǁ__init____mutmut_6": xǁGARCHǁ__init____mutmut_6,
        "xǁGARCHǁ__init____mutmut_7": xǁGARCHǁ__init____mutmut_7,
        "xǁGARCHǁ__init____mutmut_8": xǁGARCHǁ__init____mutmut_8,
        "xǁGARCHǁ__init____mutmut_9": xǁGARCHǁ__init____mutmut_9,
        "xǁGARCHǁ__init____mutmut_10": xǁGARCHǁ__init____mutmut_10,
        "xǁGARCHǁ__init____mutmut_11": xǁGARCHǁ__init____mutmut_11,
        "xǁGARCHǁ__init____mutmut_12": xǁGARCHǁ__init____mutmut_12,
        "xǁGARCHǁ__init____mutmut_13": xǁGARCHǁ__init____mutmut_13,
        "xǁGARCHǁ__init____mutmut_14": xǁGARCHǁ__init____mutmut_14,
        "xǁGARCHǁ__init____mutmut_15": xǁGARCHǁ__init____mutmut_15,
        "xǁGARCHǁ__init____mutmut_16": xǁGARCHǁ__init____mutmut_16,
        "xǁGARCHǁ__init____mutmut_17": xǁGARCHǁ__init____mutmut_17,
        "xǁGARCHǁ__init____mutmut_18": xǁGARCHǁ__init____mutmut_18,
        "xǁGARCHǁ__init____mutmut_19": xǁGARCHǁ__init____mutmut_19,
        "xǁGARCHǁ__init____mutmut_20": xǁGARCHǁ__init____mutmut_20,
        "xǁGARCHǁ__init____mutmut_21": xǁGARCHǁ__init____mutmut_21,
        "xǁGARCHǁ__init____mutmut_22": xǁGARCHǁ__init____mutmut_22,
        "xǁGARCHǁ__init____mutmut_23": xǁGARCHǁ__init____mutmut_23,
        "xǁGARCHǁ__init____mutmut_24": xǁGARCHǁ__init____mutmut_24,
        "xǁGARCHǁ__init____mutmut_25": xǁGARCHǁ__init____mutmut_25,
        "xǁGARCHǁ__init____mutmut_26": xǁGARCHǁ__init____mutmut_26,
    }
    xǁGARCHǁ__init____mutmut_orig.__name__ = "xǁGARCHǁ__init__"

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = None
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[1]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = None
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[2 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 - self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 2 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = None

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 - self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[2 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q - self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 - self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 2 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = None
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = None

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(None)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = None
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(None, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, None, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, None, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, None, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, None, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, None, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, None, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, None)

    def xǁGARCHǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, omega, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, alphas, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, betas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, self.p, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.q, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, backcast)

    def xǁGARCHǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(
            resids,
            sigma2,
            omega,
            alphas,
            betas,
            self.p,
            self.q,
        )

    xǁGARCHǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHǁ_variance_recursion__mutmut_1": xǁGARCHǁ_variance_recursion__mutmut_1,
        "xǁGARCHǁ_variance_recursion__mutmut_2": xǁGARCHǁ_variance_recursion__mutmut_2,
        "xǁGARCHǁ_variance_recursion__mutmut_3": xǁGARCHǁ_variance_recursion__mutmut_3,
        "xǁGARCHǁ_variance_recursion__mutmut_4": xǁGARCHǁ_variance_recursion__mutmut_4,
        "xǁGARCHǁ_variance_recursion__mutmut_5": xǁGARCHǁ_variance_recursion__mutmut_5,
        "xǁGARCHǁ_variance_recursion__mutmut_6": xǁGARCHǁ_variance_recursion__mutmut_6,
        "xǁGARCHǁ_variance_recursion__mutmut_7": xǁGARCHǁ_variance_recursion__mutmut_7,
        "xǁGARCHǁ_variance_recursion__mutmut_8": xǁGARCHǁ_variance_recursion__mutmut_8,
        "xǁGARCHǁ_variance_recursion__mutmut_9": xǁGARCHǁ_variance_recursion__mutmut_9,
        "xǁGARCHǁ_variance_recursion__mutmut_10": xǁGARCHǁ_variance_recursion__mutmut_10,
        "xǁGARCHǁ_variance_recursion__mutmut_11": xǁGARCHǁ_variance_recursion__mutmut_11,
        "xǁGARCHǁ_variance_recursion__mutmut_12": xǁGARCHǁ_variance_recursion__mutmut_12,
        "xǁGARCHǁ_variance_recursion__mutmut_13": xǁGARCHǁ_variance_recursion__mutmut_13,
        "xǁGARCHǁ_variance_recursion__mutmut_14": xǁGARCHǁ_variance_recursion__mutmut_14,
        "xǁGARCHǁ_variance_recursion__mutmut_15": xǁGARCHǁ_variance_recursion__mutmut_15,
        "xǁGARCHǁ_variance_recursion__mutmut_16": xǁGARCHǁ_variance_recursion__mutmut_16,
        "xǁGARCHǁ_variance_recursion__mutmut_17": xǁGARCHǁ_variance_recursion__mutmut_17,
        "xǁGARCHǁ_variance_recursion__mutmut_18": xǁGARCHǁ_variance_recursion__mutmut_18,
        "xǁGARCHǁ_variance_recursion__mutmut_19": xǁGARCHǁ_variance_recursion__mutmut_19,
        "xǁGARCHǁ_variance_recursion__mutmut_20": xǁGARCHǁ_variance_recursion__mutmut_20,
        "xǁGARCHǁ_variance_recursion__mutmut_21": xǁGARCHǁ_variance_recursion__mutmut_21,
        "xǁGARCHǁ_variance_recursion__mutmut_22": xǁGARCHǁ_variance_recursion__mutmut_22,
        "xǁGARCHǁ_variance_recursion__mutmut_23": xǁGARCHǁ_variance_recursion__mutmut_23,
        "xǁGARCHǁ_variance_recursion__mutmut_24": xǁGARCHǁ_variance_recursion__mutmut_24,
        "xǁGARCHǁ_variance_recursion__mutmut_25": xǁGARCHǁ_variance_recursion__mutmut_25,
        "xǁGARCHǁ_variance_recursion__mutmut_26": xǁGARCHǁ_variance_recursion__mutmut_26,
        "xǁGARCHǁ_variance_recursion__mutmut_27": xǁGARCHǁ_variance_recursion__mutmut_27,
        "xǁGARCHǁ_variance_recursion__mutmut_28": xǁGARCHǁ_variance_recursion__mutmut_28,
        "xǁGARCHǁ_variance_recursion__mutmut_29": xǁGARCHǁ_variance_recursion__mutmut_29,
        "xǁGARCHǁ_variance_recursion__mutmut_30": xǁGARCHǁ_variance_recursion__mutmut_30,
        "xǁGARCHǁ_variance_recursion__mutmut_31": xǁGARCHǁ_variance_recursion__mutmut_31,
        "xǁGARCHǁ_variance_recursion__mutmut_32": xǁGARCHǁ_variance_recursion__mutmut_32,
    }
    xǁGARCHǁ_variance_recursion__mutmut_orig.__name__ = "xǁGARCHǁ_variance_recursion"

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = None
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[1]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = None
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[2]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = None
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 - self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = None
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 - beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega - alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha / eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps * 2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**3 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta / sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(None)

    def xǁGARCHǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(None, 1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, None))

    def xǁGARCHǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(1e-12))

    def xǁGARCHǁ_one_step_variance__mutmut_19(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(
            max(
                sigma2,
            )
        )

    def xǁGARCHǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1.000000000001))

    xǁGARCHǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHǁ_one_step_variance__mutmut_1": xǁGARCHǁ_one_step_variance__mutmut_1,
        "xǁGARCHǁ_one_step_variance__mutmut_2": xǁGARCHǁ_one_step_variance__mutmut_2,
        "xǁGARCHǁ_one_step_variance__mutmut_3": xǁGARCHǁ_one_step_variance__mutmut_3,
        "xǁGARCHǁ_one_step_variance__mutmut_4": xǁGARCHǁ_one_step_variance__mutmut_4,
        "xǁGARCHǁ_one_step_variance__mutmut_5": xǁGARCHǁ_one_step_variance__mutmut_5,
        "xǁGARCHǁ_one_step_variance__mutmut_6": xǁGARCHǁ_one_step_variance__mutmut_6,
        "xǁGARCHǁ_one_step_variance__mutmut_7": xǁGARCHǁ_one_step_variance__mutmut_7,
        "xǁGARCHǁ_one_step_variance__mutmut_8": xǁGARCHǁ_one_step_variance__mutmut_8,
        "xǁGARCHǁ_one_step_variance__mutmut_9": xǁGARCHǁ_one_step_variance__mutmut_9,
        "xǁGARCHǁ_one_step_variance__mutmut_10": xǁGARCHǁ_one_step_variance__mutmut_10,
        "xǁGARCHǁ_one_step_variance__mutmut_11": xǁGARCHǁ_one_step_variance__mutmut_11,
        "xǁGARCHǁ_one_step_variance__mutmut_12": xǁGARCHǁ_one_step_variance__mutmut_12,
        "xǁGARCHǁ_one_step_variance__mutmut_13": xǁGARCHǁ_one_step_variance__mutmut_13,
        "xǁGARCHǁ_one_step_variance__mutmut_14": xǁGARCHǁ_one_step_variance__mutmut_14,
        "xǁGARCHǁ_one_step_variance__mutmut_15": xǁGARCHǁ_one_step_variance__mutmut_15,
        "xǁGARCHǁ_one_step_variance__mutmut_16": xǁGARCHǁ_one_step_variance__mutmut_16,
        "xǁGARCHǁ_one_step_variance__mutmut_17": xǁGARCHǁ_one_step_variance__mutmut_17,
        "xǁGARCHǁ_one_step_variance__mutmut_18": xǁGARCHǁ_one_step_variance__mutmut_18,
        "xǁGARCHǁ_one_step_variance__mutmut_19": xǁGARCHǁ_one_step_variance__mutmut_19,
        "xǁGARCHǁ_one_step_variance__mutmut_20": xǁGARCHǁ_one_step_variance__mutmut_20,
    }
    xǁGARCHǁ_one_step_variance__mutmut_orig.__name__ = "xǁGARCHǁ_one_step_variance"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameters via variance targeting.

        Sets alpha=0.08, beta=0.88, and derives omega from
        the sample variance.
        """
        target_var = float(np.var(self.endog))
        alpha_init = 0.08
        beta_init = 0.88
        omega_init = target_var * (1 - alpha_init * self.q - beta_init * self.p)
        omega_init = max(omega_init, 1e-10)
        return np.array([omega_init] + [alpha_init] * self.q + [beta_init] * self.p)

    @property
    def param_names(self) -> list[str]:
        """Parameter names: omega, alpha[1], ..., beta[1], ..."""
        names = ["omega"]
        names.extend(f"alpha[{i + 1}]" for i in range(self.q))
        names.extend(f"beta[{j + 1}]" for j in range(self.p))
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = None
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(None)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = None

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[1] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(None)

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(None, -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], None, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, None))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(-50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(
            np.clip(
                unconstrained[0],
                -50.0,
            )
        )

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[1], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], +50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -51.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 51.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = None  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_17(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 * (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_18(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 2.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_19(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 - np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_20(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (2.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_21(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(None))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_22(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(+unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_23(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[2:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_24(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = None
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_25(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(None)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_26(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total > 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_27(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 1.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_28(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = None
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_29(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw / (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_30(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 * total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_31(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (1.9999 / total)
        constrained[1:] = raw

        return constrained

    def xǁGARCHǁtransform_params__mutmut_32(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = None

        return constrained

    def xǁGARCHǁtransform_params__mutmut_33(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[2:] = raw

        return constrained

    xǁGARCHǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHǁtransform_params__mutmut_1": xǁGARCHǁtransform_params__mutmut_1,
        "xǁGARCHǁtransform_params__mutmut_2": xǁGARCHǁtransform_params__mutmut_2,
        "xǁGARCHǁtransform_params__mutmut_3": xǁGARCHǁtransform_params__mutmut_3,
        "xǁGARCHǁtransform_params__mutmut_4": xǁGARCHǁtransform_params__mutmut_4,
        "xǁGARCHǁtransform_params__mutmut_5": xǁGARCHǁtransform_params__mutmut_5,
        "xǁGARCHǁtransform_params__mutmut_6": xǁGARCHǁtransform_params__mutmut_6,
        "xǁGARCHǁtransform_params__mutmut_7": xǁGARCHǁtransform_params__mutmut_7,
        "xǁGARCHǁtransform_params__mutmut_8": xǁGARCHǁtransform_params__mutmut_8,
        "xǁGARCHǁtransform_params__mutmut_9": xǁGARCHǁtransform_params__mutmut_9,
        "xǁGARCHǁtransform_params__mutmut_10": xǁGARCHǁtransform_params__mutmut_10,
        "xǁGARCHǁtransform_params__mutmut_11": xǁGARCHǁtransform_params__mutmut_11,
        "xǁGARCHǁtransform_params__mutmut_12": xǁGARCHǁtransform_params__mutmut_12,
        "xǁGARCHǁtransform_params__mutmut_13": xǁGARCHǁtransform_params__mutmut_13,
        "xǁGARCHǁtransform_params__mutmut_14": xǁGARCHǁtransform_params__mutmut_14,
        "xǁGARCHǁtransform_params__mutmut_15": xǁGARCHǁtransform_params__mutmut_15,
        "xǁGARCHǁtransform_params__mutmut_16": xǁGARCHǁtransform_params__mutmut_16,
        "xǁGARCHǁtransform_params__mutmut_17": xǁGARCHǁtransform_params__mutmut_17,
        "xǁGARCHǁtransform_params__mutmut_18": xǁGARCHǁtransform_params__mutmut_18,
        "xǁGARCHǁtransform_params__mutmut_19": xǁGARCHǁtransform_params__mutmut_19,
        "xǁGARCHǁtransform_params__mutmut_20": xǁGARCHǁtransform_params__mutmut_20,
        "xǁGARCHǁtransform_params__mutmut_21": xǁGARCHǁtransform_params__mutmut_21,
        "xǁGARCHǁtransform_params__mutmut_22": xǁGARCHǁtransform_params__mutmut_22,
        "xǁGARCHǁtransform_params__mutmut_23": xǁGARCHǁtransform_params__mutmut_23,
        "xǁGARCHǁtransform_params__mutmut_24": xǁGARCHǁtransform_params__mutmut_24,
        "xǁGARCHǁtransform_params__mutmut_25": xǁGARCHǁtransform_params__mutmut_25,
        "xǁGARCHǁtransform_params__mutmut_26": xǁGARCHǁtransform_params__mutmut_26,
        "xǁGARCHǁtransform_params__mutmut_27": xǁGARCHǁtransform_params__mutmut_27,
        "xǁGARCHǁtransform_params__mutmut_28": xǁGARCHǁtransform_params__mutmut_28,
        "xǁGARCHǁtransform_params__mutmut_29": xǁGARCHǁtransform_params__mutmut_29,
        "xǁGARCHǁtransform_params__mutmut_30": xǁGARCHǁtransform_params__mutmut_30,
        "xǁGARCHǁtransform_params__mutmut_31": xǁGARCHǁtransform_params__mutmut_31,
        "xǁGARCHǁtransform_params__mutmut_32": xǁGARCHǁtransform_params__mutmut_32,
        "xǁGARCHǁtransform_params__mutmut_33": xǁGARCHǁtransform_params__mutmut_33,
    }
    xǁGARCHǁtransform_params__mutmut_orig.__name__ = "xǁGARCHǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = None
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(None)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = None  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[1] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(None)  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[1])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = None
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(None, 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], None, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, None)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(
            constrained[1:],
            1e-8,
        )
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[2:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1.00000001, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 + 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 2.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1.00000001)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = None
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[2:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(None)
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab * (1.0 - ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 + ab))
        return unconstrained

    def xǁGARCHǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (2.0 - ab))
        return unconstrained

    xǁGARCHǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHǁuntransform_params__mutmut_1": xǁGARCHǁuntransform_params__mutmut_1,
        "xǁGARCHǁuntransform_params__mutmut_2": xǁGARCHǁuntransform_params__mutmut_2,
        "xǁGARCHǁuntransform_params__mutmut_3": xǁGARCHǁuntransform_params__mutmut_3,
        "xǁGARCHǁuntransform_params__mutmut_4": xǁGARCHǁuntransform_params__mutmut_4,
        "xǁGARCHǁuntransform_params__mutmut_5": xǁGARCHǁuntransform_params__mutmut_5,
        "xǁGARCHǁuntransform_params__mutmut_6": xǁGARCHǁuntransform_params__mutmut_6,
        "xǁGARCHǁuntransform_params__mutmut_7": xǁGARCHǁuntransform_params__mutmut_7,
        "xǁGARCHǁuntransform_params__mutmut_8": xǁGARCHǁuntransform_params__mutmut_8,
        "xǁGARCHǁuntransform_params__mutmut_9": xǁGARCHǁuntransform_params__mutmut_9,
        "xǁGARCHǁuntransform_params__mutmut_10": xǁGARCHǁuntransform_params__mutmut_10,
        "xǁGARCHǁuntransform_params__mutmut_11": xǁGARCHǁuntransform_params__mutmut_11,
        "xǁGARCHǁuntransform_params__mutmut_12": xǁGARCHǁuntransform_params__mutmut_12,
        "xǁGARCHǁuntransform_params__mutmut_13": xǁGARCHǁuntransform_params__mutmut_13,
        "xǁGARCHǁuntransform_params__mutmut_14": xǁGARCHǁuntransform_params__mutmut_14,
        "xǁGARCHǁuntransform_params__mutmut_15": xǁGARCHǁuntransform_params__mutmut_15,
        "xǁGARCHǁuntransform_params__mutmut_16": xǁGARCHǁuntransform_params__mutmut_16,
        "xǁGARCHǁuntransform_params__mutmut_17": xǁGARCHǁuntransform_params__mutmut_17,
        "xǁGARCHǁuntransform_params__mutmut_18": xǁGARCHǁuntransform_params__mutmut_18,
        "xǁGARCHǁuntransform_params__mutmut_19": xǁGARCHǁuntransform_params__mutmut_19,
        "xǁGARCHǁuntransform_params__mutmut_20": xǁGARCHǁuntransform_params__mutmut_20,
        "xǁGARCHǁuntransform_params__mutmut_21": xǁGARCHǁuntransform_params__mutmut_21,
        "xǁGARCHǁuntransform_params__mutmut_22": xǁGARCHǁuntransform_params__mutmut_22,
        "xǁGARCHǁuntransform_params__mutmut_23": xǁGARCHǁuntransform_params__mutmut_23,
        "xǁGARCHǁuntransform_params__mutmut_24": xǁGARCHǁuntransform_params__mutmut_24,
    }
    xǁGARCHǁuntransform_params__mutmut_orig.__name__ = "xǁGARCHǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = None  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1.000000000001, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 11.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend(None)  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((1.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 2.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(None))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend(None)  # betas
        return b

    def xǁGARCHǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((1.0, 1.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_10(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 2.0) for _ in range(self.p))  # betas
        return b

    def xǁGARCHǁbounds__mutmut_11(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(None))  # betas
        return b

    xǁGARCHǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHǁbounds__mutmut_1": xǁGARCHǁbounds__mutmut_1,
        "xǁGARCHǁbounds__mutmut_2": xǁGARCHǁbounds__mutmut_2,
        "xǁGARCHǁbounds__mutmut_3": xǁGARCHǁbounds__mutmut_3,
        "xǁGARCHǁbounds__mutmut_4": xǁGARCHǁbounds__mutmut_4,
        "xǁGARCHǁbounds__mutmut_5": xǁGARCHǁbounds__mutmut_5,
        "xǁGARCHǁbounds__mutmut_6": xǁGARCHǁbounds__mutmut_6,
        "xǁGARCHǁbounds__mutmut_7": xǁGARCHǁbounds__mutmut_7,
        "xǁGARCHǁbounds__mutmut_8": xǁGARCHǁbounds__mutmut_8,
        "xǁGARCHǁbounds__mutmut_9": xǁGARCHǁbounds__mutmut_9,
        "xǁGARCHǁbounds__mutmut_10": xǁGARCHǁbounds__mutmut_10,
        "xǁGARCHǁbounds__mutmut_11": xǁGARCHǁbounds__mutmut_11,
    }
    xǁGARCHǁbounds__mutmut_orig.__name__ = "xǁGARCHǁbounds"

    @property
    def num_params(self) -> int:
        """Number of parameters: 1 + q + p."""
        return 1 + self.q + self.p

    def __repr__(self) -> str:
        """Return string representation of the GARCH model."""
        return f"GARCH(p={self.p}, q={self.q}, nobs={self.nobs})"
