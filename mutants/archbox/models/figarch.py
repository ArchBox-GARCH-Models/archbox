"""FIGARCH - Fractionally Integrated GARCH (Baillie, Bollerslev & Mikkelsen, 1996).

(1 - beta(L)) * sigma^2_t = omega + [1 - beta(L) - phi(L)(1-L)^d] * eps^2_t

Long memory in variance with fractional differencing parameter d.
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


def _fractional_coefficients(d: float, n_lags: int) -> NDArray[np.float64]:
    args = [d, n_lags]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x__fractional_coefficients__mutmut_orig,
        x__fractional_coefficients__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x__fractional_coefficients__mutmut_orig(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_1(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = None
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_2(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(None)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_3(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags != 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_4(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 1:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_5(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = None
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_6(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[1] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_7(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(None, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_8(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, None):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_9(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_10(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(
        1,
    ):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_11(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(2, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_12(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = None
    return coeffs


def x__fractional_coefficients__mutmut_13(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) * (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_14(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] / (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_15(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k + 1] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_16(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 2] * (k - d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_17(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k + d) / (k + 1)
    return coeffs


def x__fractional_coefficients__mutmut_18(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k - 1)
    return coeffs


def x__fractional_coefficients__mutmut_19(d: float, n_lags: int) -> NDArray[np.float64]:
    """Compute coefficients delta_k of the fractional differencing operator.

    The expansion is (1-L)^d = 1 - sum_{k=1}^{inf} delta_k L^k,
    where delta_k > 0 for 0 < d < 1.

    Parameters
    ----------
    d : float
        Fractional differencing parameter, 0 < d < 1.
    n_lags : int
        Number of lags for the truncated expansion.

    Returns
    -------
    ndarray
        Coefficients delta_1, delta_2, ..., delta_{n_lags} (0-indexed).
    """
    coeffs = np.zeros(n_lags)
    if n_lags == 0:
        return coeffs
    coeffs[0] = d
    for k in range(1, n_lags):
        coeffs[k] = coeffs[k - 1] * (k - d) / (k + 2)
    return coeffs


x__fractional_coefficients__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x__fractional_coefficients__mutmut_1": x__fractional_coefficients__mutmut_1,
    "x__fractional_coefficients__mutmut_2": x__fractional_coefficients__mutmut_2,
    "x__fractional_coefficients__mutmut_3": x__fractional_coefficients__mutmut_3,
    "x__fractional_coefficients__mutmut_4": x__fractional_coefficients__mutmut_4,
    "x__fractional_coefficients__mutmut_5": x__fractional_coefficients__mutmut_5,
    "x__fractional_coefficients__mutmut_6": x__fractional_coefficients__mutmut_6,
    "x__fractional_coefficients__mutmut_7": x__fractional_coefficients__mutmut_7,
    "x__fractional_coefficients__mutmut_8": x__fractional_coefficients__mutmut_8,
    "x__fractional_coefficients__mutmut_9": x__fractional_coefficients__mutmut_9,
    "x__fractional_coefficients__mutmut_10": x__fractional_coefficients__mutmut_10,
    "x__fractional_coefficients__mutmut_11": x__fractional_coefficients__mutmut_11,
    "x__fractional_coefficients__mutmut_12": x__fractional_coefficients__mutmut_12,
    "x__fractional_coefficients__mutmut_13": x__fractional_coefficients__mutmut_13,
    "x__fractional_coefficients__mutmut_14": x__fractional_coefficients__mutmut_14,
    "x__fractional_coefficients__mutmut_15": x__fractional_coefficients__mutmut_15,
    "x__fractional_coefficients__mutmut_16": x__fractional_coefficients__mutmut_16,
    "x__fractional_coefficients__mutmut_17": x__fractional_coefficients__mutmut_17,
    "x__fractional_coefficients__mutmut_18": x__fractional_coefficients__mutmut_18,
    "x__fractional_coefficients__mutmut_19": x__fractional_coefficients__mutmut_19,
}
x__fractional_coefficients__mutmut_orig.__name__ = "x__fractional_coefficients"


class FIGARCH(VolatilityModel):
    """Fractionally Integrated GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    truncation_lag : int
        Number of lags for the truncated fractional expansion. Default 1000.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "FIGARCH"

    def __init__(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        args = [endog, truncation_lag, mean, dist]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁFIGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁFIGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁFIGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        truncation_lag: int = 1001,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = None
        super().__init__(endog, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(None, mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=None, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, mean=mean, dist=None)

    def xǁFIGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(mean=mean, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(endog, dist=dist)

    def xǁFIGARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        truncation_lag: int = 1000,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize FIGARCH model with truncation lag and options."""
        self.truncation_lag = truncation_lag
        super().__init__(
            endog,
            mean=mean,
        )

    xǁFIGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁFIGARCHǁ__init____mutmut_1": xǁFIGARCHǁ__init____mutmut_1,
        "xǁFIGARCHǁ__init____mutmut_2": xǁFIGARCHǁ__init____mutmut_2,
        "xǁFIGARCHǁ__init____mutmut_3": xǁFIGARCHǁ__init____mutmut_3,
        "xǁFIGARCHǁ__init____mutmut_4": xǁFIGARCHǁ__init____mutmut_4,
        "xǁFIGARCHǁ__init____mutmut_5": xǁFIGARCHǁ__init____mutmut_5,
        "xǁFIGARCHǁ__init____mutmut_6": xǁFIGARCHǁ__init____mutmut_6,
        "xǁFIGARCHǁ__init____mutmut_7": xǁFIGARCHǁ__init____mutmut_7,
        "xǁFIGARCHǁ__init____mutmut_8": xǁFIGARCHǁ__init____mutmut_8,
        "xǁFIGARCHǁ__init____mutmut_9": xǁFIGARCHǁ__init____mutmut_9,
        "xǁFIGARCHǁ__init____mutmut_10": xǁFIGARCHǁ__init____mutmut_10,
        "xǁFIGARCHǁ__init____mutmut_11": xǁFIGARCHǁ__init____mutmut_11,
        "xǁFIGARCHǁ__init____mutmut_12": xǁFIGARCHǁ__init____mutmut_12,
    }
    xǁFIGARCHǁ__init____mutmut_orig.__name__ = "xǁFIGARCHǁ__init__"

    def _compute_lambda_coefficients(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        args = [phi, d, beta, n_lags]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_orig"),
            object.__getattribute__(self, "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_orig(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_1(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = None

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_2(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(None, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_3(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, None)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_4(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_5(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(
            d,
        )

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_6(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = None
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_7(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(None)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_8(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = None
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_9(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[1] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_10(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta - d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_11(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi + beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_12(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(None, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_13(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, None):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_14(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_15(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(
            1,
        ):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_16(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(2, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_17(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = None

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_18(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] + phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_19(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] - delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_20(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta / lam[k - 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_21(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k + 1] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_22(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 2] + delta[k] - phi * delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_23(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi / delta[k - 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_24(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k + 1]

        return lam

    def xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_25(
        self, phi: float, d: float, beta: float, n_lags: int
    ) -> NDArray[np.float64]:
        """Compute the FIGARCH lambda coefficients for variance recursion.

        The FIGARCH variance can be written as:
        sigma^2_t = omega/(1-beta) + sum_{k=1}^{inf} lambda_k * eps^2_{t-k}

        Parameters
        ----------
        phi : float
            ARCH polynomial parameter.
        d : float
            Fractional differencing parameter.
        beta : float
            GARCH parameter.
        n_lags : int
            Truncation lag.

        Returns
        -------
        ndarray
            Lambda coefficients (0-indexed: lam[k] = lambda_{k+1}).
        """
        delta = _fractional_coefficients(d, n_lags)

        lam = np.zeros(n_lags)
        # lambda_1 = phi - beta + d
        lam[0] = phi - beta + d
        for k in range(1, n_lags):
            # lambda_{k+1} = beta * lambda_k + delta_{k+1} - phi * delta_k
            lam[k] = beta * lam[k - 1] + delta[k] - phi * delta[k - 2]

        return lam

    xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_1": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_1,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_2": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_2,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_3": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_3,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_4": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_4,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_5": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_5,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_6": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_6,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_7": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_7,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_8": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_8,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_9": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_9,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_10": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_10,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_11": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_11,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_12": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_12,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_13": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_13,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_14": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_14,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_15": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_15,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_16": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_16,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_17": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_17,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_18": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_18,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_19": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_19,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_20": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_20,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_21": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_21,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_22": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_22,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_23": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_23,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_24": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_24,
        "xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_25": xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_25,
    }
    xǁFIGARCHǁ_compute_lambda_coefficients__mutmut_orig.__name__ = (
        "xǁFIGARCHǁ_compute_lambda_coefficients"
    )

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁFIGARCHǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁFIGARCHǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁFIGARCHǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = None
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[2]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = None
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[3]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = None

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[4]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = None
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = None

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(None, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, None)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(
            self.truncation_lag,
        )

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = None

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(None, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, None, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, None, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, None)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(
            phi,
            d,
            beta,
        )

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = None
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(None)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = None

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega * (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 + beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (2.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(None) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 + beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(2.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) >= 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1.0000000001 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(None):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = None
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(None):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(None, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, None)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(
                min(
                    t,
                )
            ):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = None
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] * 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 + k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t + 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 2 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 3 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 + k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t + 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 2 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k > 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 1 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] = lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] -= lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] / eps2
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = None

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(None, 1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_58(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], None)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_59(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(1e-12)

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_60(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(
                sigma2[t],
            )

        return sigma2

    def xǁFIGARCHǁ_variance_recursion__mutmut_61(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via FIGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, phi, d, beta]
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
        phi = params[1]
        d = params[2]
        beta = params[3]

        nobs = len(resids)
        n_lags = min(self.truncation_lag, nobs)

        lam = self._compute_lambda_coefficients(phi, d, beta, n_lags)

        sigma2 = np.empty(nobs)
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega

        for t in range(nobs):
            sigma2[t] = omega_star
            for k in range(min(t, n_lags)):
                eps2 = resids[t - 1 - k] ** 2 if t - 1 - k >= 0 else backcast
                sigma2[t] += lam[k] * eps2
            sigma2[t] = max(sigma2[t], 1.000000000001)

        return sigma2

    xǁFIGARCHǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁFIGARCHǁ_variance_recursion__mutmut_1": xǁFIGARCHǁ_variance_recursion__mutmut_1,
        "xǁFIGARCHǁ_variance_recursion__mutmut_2": xǁFIGARCHǁ_variance_recursion__mutmut_2,
        "xǁFIGARCHǁ_variance_recursion__mutmut_3": xǁFIGARCHǁ_variance_recursion__mutmut_3,
        "xǁFIGARCHǁ_variance_recursion__mutmut_4": xǁFIGARCHǁ_variance_recursion__mutmut_4,
        "xǁFIGARCHǁ_variance_recursion__mutmut_5": xǁFIGARCHǁ_variance_recursion__mutmut_5,
        "xǁFIGARCHǁ_variance_recursion__mutmut_6": xǁFIGARCHǁ_variance_recursion__mutmut_6,
        "xǁFIGARCHǁ_variance_recursion__mutmut_7": xǁFIGARCHǁ_variance_recursion__mutmut_7,
        "xǁFIGARCHǁ_variance_recursion__mutmut_8": xǁFIGARCHǁ_variance_recursion__mutmut_8,
        "xǁFIGARCHǁ_variance_recursion__mutmut_9": xǁFIGARCHǁ_variance_recursion__mutmut_9,
        "xǁFIGARCHǁ_variance_recursion__mutmut_10": xǁFIGARCHǁ_variance_recursion__mutmut_10,
        "xǁFIGARCHǁ_variance_recursion__mutmut_11": xǁFIGARCHǁ_variance_recursion__mutmut_11,
        "xǁFIGARCHǁ_variance_recursion__mutmut_12": xǁFIGARCHǁ_variance_recursion__mutmut_12,
        "xǁFIGARCHǁ_variance_recursion__mutmut_13": xǁFIGARCHǁ_variance_recursion__mutmut_13,
        "xǁFIGARCHǁ_variance_recursion__mutmut_14": xǁFIGARCHǁ_variance_recursion__mutmut_14,
        "xǁFIGARCHǁ_variance_recursion__mutmut_15": xǁFIGARCHǁ_variance_recursion__mutmut_15,
        "xǁFIGARCHǁ_variance_recursion__mutmut_16": xǁFIGARCHǁ_variance_recursion__mutmut_16,
        "xǁFIGARCHǁ_variance_recursion__mutmut_17": xǁFIGARCHǁ_variance_recursion__mutmut_17,
        "xǁFIGARCHǁ_variance_recursion__mutmut_18": xǁFIGARCHǁ_variance_recursion__mutmut_18,
        "xǁFIGARCHǁ_variance_recursion__mutmut_19": xǁFIGARCHǁ_variance_recursion__mutmut_19,
        "xǁFIGARCHǁ_variance_recursion__mutmut_20": xǁFIGARCHǁ_variance_recursion__mutmut_20,
        "xǁFIGARCHǁ_variance_recursion__mutmut_21": xǁFIGARCHǁ_variance_recursion__mutmut_21,
        "xǁFIGARCHǁ_variance_recursion__mutmut_22": xǁFIGARCHǁ_variance_recursion__mutmut_22,
        "xǁFIGARCHǁ_variance_recursion__mutmut_23": xǁFIGARCHǁ_variance_recursion__mutmut_23,
        "xǁFIGARCHǁ_variance_recursion__mutmut_24": xǁFIGARCHǁ_variance_recursion__mutmut_24,
        "xǁFIGARCHǁ_variance_recursion__mutmut_25": xǁFIGARCHǁ_variance_recursion__mutmut_25,
        "xǁFIGARCHǁ_variance_recursion__mutmut_26": xǁFIGARCHǁ_variance_recursion__mutmut_26,
        "xǁFIGARCHǁ_variance_recursion__mutmut_27": xǁFIGARCHǁ_variance_recursion__mutmut_27,
        "xǁFIGARCHǁ_variance_recursion__mutmut_28": xǁFIGARCHǁ_variance_recursion__mutmut_28,
        "xǁFIGARCHǁ_variance_recursion__mutmut_29": xǁFIGARCHǁ_variance_recursion__mutmut_29,
        "xǁFIGARCHǁ_variance_recursion__mutmut_30": xǁFIGARCHǁ_variance_recursion__mutmut_30,
        "xǁFIGARCHǁ_variance_recursion__mutmut_31": xǁFIGARCHǁ_variance_recursion__mutmut_31,
        "xǁFIGARCHǁ_variance_recursion__mutmut_32": xǁFIGARCHǁ_variance_recursion__mutmut_32,
        "xǁFIGARCHǁ_variance_recursion__mutmut_33": xǁFIGARCHǁ_variance_recursion__mutmut_33,
        "xǁFIGARCHǁ_variance_recursion__mutmut_34": xǁFIGARCHǁ_variance_recursion__mutmut_34,
        "xǁFIGARCHǁ_variance_recursion__mutmut_35": xǁFIGARCHǁ_variance_recursion__mutmut_35,
        "xǁFIGARCHǁ_variance_recursion__mutmut_36": xǁFIGARCHǁ_variance_recursion__mutmut_36,
        "xǁFIGARCHǁ_variance_recursion__mutmut_37": xǁFIGARCHǁ_variance_recursion__mutmut_37,
        "xǁFIGARCHǁ_variance_recursion__mutmut_38": xǁFIGARCHǁ_variance_recursion__mutmut_38,
        "xǁFIGARCHǁ_variance_recursion__mutmut_39": xǁFIGARCHǁ_variance_recursion__mutmut_39,
        "xǁFIGARCHǁ_variance_recursion__mutmut_40": xǁFIGARCHǁ_variance_recursion__mutmut_40,
        "xǁFIGARCHǁ_variance_recursion__mutmut_41": xǁFIGARCHǁ_variance_recursion__mutmut_41,
        "xǁFIGARCHǁ_variance_recursion__mutmut_42": xǁFIGARCHǁ_variance_recursion__mutmut_42,
        "xǁFIGARCHǁ_variance_recursion__mutmut_43": xǁFIGARCHǁ_variance_recursion__mutmut_43,
        "xǁFIGARCHǁ_variance_recursion__mutmut_44": xǁFIGARCHǁ_variance_recursion__mutmut_44,
        "xǁFIGARCHǁ_variance_recursion__mutmut_45": xǁFIGARCHǁ_variance_recursion__mutmut_45,
        "xǁFIGARCHǁ_variance_recursion__mutmut_46": xǁFIGARCHǁ_variance_recursion__mutmut_46,
        "xǁFIGARCHǁ_variance_recursion__mutmut_47": xǁFIGARCHǁ_variance_recursion__mutmut_47,
        "xǁFIGARCHǁ_variance_recursion__mutmut_48": xǁFIGARCHǁ_variance_recursion__mutmut_48,
        "xǁFIGARCHǁ_variance_recursion__mutmut_49": xǁFIGARCHǁ_variance_recursion__mutmut_49,
        "xǁFIGARCHǁ_variance_recursion__mutmut_50": xǁFIGARCHǁ_variance_recursion__mutmut_50,
        "xǁFIGARCHǁ_variance_recursion__mutmut_51": xǁFIGARCHǁ_variance_recursion__mutmut_51,
        "xǁFIGARCHǁ_variance_recursion__mutmut_52": xǁFIGARCHǁ_variance_recursion__mutmut_52,
        "xǁFIGARCHǁ_variance_recursion__mutmut_53": xǁFIGARCHǁ_variance_recursion__mutmut_53,
        "xǁFIGARCHǁ_variance_recursion__mutmut_54": xǁFIGARCHǁ_variance_recursion__mutmut_54,
        "xǁFIGARCHǁ_variance_recursion__mutmut_55": xǁFIGARCHǁ_variance_recursion__mutmut_55,
        "xǁFIGARCHǁ_variance_recursion__mutmut_56": xǁFIGARCHǁ_variance_recursion__mutmut_56,
        "xǁFIGARCHǁ_variance_recursion__mutmut_57": xǁFIGARCHǁ_variance_recursion__mutmut_57,
        "xǁFIGARCHǁ_variance_recursion__mutmut_58": xǁFIGARCHǁ_variance_recursion__mutmut_58,
        "xǁFIGARCHǁ_variance_recursion__mutmut_59": xǁFIGARCHǁ_variance_recursion__mutmut_59,
        "xǁFIGARCHǁ_variance_recursion__mutmut_60": xǁFIGARCHǁ_variance_recursion__mutmut_60,
        "xǁFIGARCHǁ_variance_recursion__mutmut_61": xǁFIGARCHǁ_variance_recursion__mutmut_61,
    }
    xǁFIGARCHǁ_variance_recursion__mutmut_orig.__name__ = "xǁFIGARCHǁ_variance_recursion"

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁFIGARCHǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁFIGARCHǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁFIGARCHǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = None
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[1]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = None
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[4]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = None
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega * (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 + beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (2.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(None) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 + beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(2.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) >= 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1.0000000001 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = None
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[2]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = None
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[3]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = None
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_19(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta - d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi + beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_21(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = None
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_22(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star - lam1 * eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_23(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 / eps**2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_24(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps * 2
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_25(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**3
        return float(max(sigma2, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_26(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(None)

    def xǁFIGARCHǁ_one_step_variance__mutmut_27(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(None, 1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_28(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, None))

    def xǁFIGARCHǁ_one_step_variance__mutmut_29(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(1e-12))

    def xǁFIGARCHǁ_one_step_variance__mutmut_30(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(
            max(
                sigma2,
            )
        )

    def xǁFIGARCHǁ_one_step_variance__mutmut_31(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance (simplified for news impact)."""
        omega = params[0]
        beta = params[3]
        omega_star = omega / (1.0 - beta) if abs(1.0 - beta) > 1e-10 else omega
        phi = params[1]
        d = params[2]
        lam1 = phi - beta + d
        sigma2 = omega_star + lam1 * eps**2
        return float(max(sigma2, 1.000000000001))

    xǁFIGARCHǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁFIGARCHǁ_one_step_variance__mutmut_1": xǁFIGARCHǁ_one_step_variance__mutmut_1,
        "xǁFIGARCHǁ_one_step_variance__mutmut_2": xǁFIGARCHǁ_one_step_variance__mutmut_2,
        "xǁFIGARCHǁ_one_step_variance__mutmut_3": xǁFIGARCHǁ_one_step_variance__mutmut_3,
        "xǁFIGARCHǁ_one_step_variance__mutmut_4": xǁFIGARCHǁ_one_step_variance__mutmut_4,
        "xǁFIGARCHǁ_one_step_variance__mutmut_5": xǁFIGARCHǁ_one_step_variance__mutmut_5,
        "xǁFIGARCHǁ_one_step_variance__mutmut_6": xǁFIGARCHǁ_one_step_variance__mutmut_6,
        "xǁFIGARCHǁ_one_step_variance__mutmut_7": xǁFIGARCHǁ_one_step_variance__mutmut_7,
        "xǁFIGARCHǁ_one_step_variance__mutmut_8": xǁFIGARCHǁ_one_step_variance__mutmut_8,
        "xǁFIGARCHǁ_one_step_variance__mutmut_9": xǁFIGARCHǁ_one_step_variance__mutmut_9,
        "xǁFIGARCHǁ_one_step_variance__mutmut_10": xǁFIGARCHǁ_one_step_variance__mutmut_10,
        "xǁFIGARCHǁ_one_step_variance__mutmut_11": xǁFIGARCHǁ_one_step_variance__mutmut_11,
        "xǁFIGARCHǁ_one_step_variance__mutmut_12": xǁFIGARCHǁ_one_step_variance__mutmut_12,
        "xǁFIGARCHǁ_one_step_variance__mutmut_13": xǁFIGARCHǁ_one_step_variance__mutmut_13,
        "xǁFIGARCHǁ_one_step_variance__mutmut_14": xǁFIGARCHǁ_one_step_variance__mutmut_14,
        "xǁFIGARCHǁ_one_step_variance__mutmut_15": xǁFIGARCHǁ_one_step_variance__mutmut_15,
        "xǁFIGARCHǁ_one_step_variance__mutmut_16": xǁFIGARCHǁ_one_step_variance__mutmut_16,
        "xǁFIGARCHǁ_one_step_variance__mutmut_17": xǁFIGARCHǁ_one_step_variance__mutmut_17,
        "xǁFIGARCHǁ_one_step_variance__mutmut_18": xǁFIGARCHǁ_one_step_variance__mutmut_18,
        "xǁFIGARCHǁ_one_step_variance__mutmut_19": xǁFIGARCHǁ_one_step_variance__mutmut_19,
        "xǁFIGARCHǁ_one_step_variance__mutmut_20": xǁFIGARCHǁ_one_step_variance__mutmut_20,
        "xǁFIGARCHǁ_one_step_variance__mutmut_21": xǁFIGARCHǁ_one_step_variance__mutmut_21,
        "xǁFIGARCHǁ_one_step_variance__mutmut_22": xǁFIGARCHǁ_one_step_variance__mutmut_22,
        "xǁFIGARCHǁ_one_step_variance__mutmut_23": xǁFIGARCHǁ_one_step_variance__mutmut_23,
        "xǁFIGARCHǁ_one_step_variance__mutmut_24": xǁFIGARCHǁ_one_step_variance__mutmut_24,
        "xǁFIGARCHǁ_one_step_variance__mutmut_25": xǁFIGARCHǁ_one_step_variance__mutmut_25,
        "xǁFIGARCHǁ_one_step_variance__mutmut_26": xǁFIGARCHǁ_one_step_variance__mutmut_26,
        "xǁFIGARCHǁ_one_step_variance__mutmut_27": xǁFIGARCHǁ_one_step_variance__mutmut_27,
        "xǁFIGARCHǁ_one_step_variance__mutmut_28": xǁFIGARCHǁ_one_step_variance__mutmut_28,
        "xǁFIGARCHǁ_one_step_variance__mutmut_29": xǁFIGARCHǁ_one_step_variance__mutmut_29,
        "xǁFIGARCHǁ_one_step_variance__mutmut_30": xǁFIGARCHǁ_one_step_variance__mutmut_30,
        "xǁFIGARCHǁ_one_step_variance__mutmut_31": xǁFIGARCHǁ_one_step_variance__mutmut_31,
    }
    xǁFIGARCHǁ_one_step_variance__mutmut_orig.__name__ = "xǁFIGARCHǁ_one_step_variance"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: [omega, phi, d, beta]."""
        var = np.var(self.endog)
        omega = var * 0.01
        phi = 0.2
        d = 0.4
        beta = 0.3
        return np.array([omega, phi, d, beta])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        return ["omega", "phi", "d", "beta"]

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁFIGARCHǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁFIGARCHǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁFIGARCHǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = None
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = None
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[1] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(None)
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[1])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = None
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[2] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(None)
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[2])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = None
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[3] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 * (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 2.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 - np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (2.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(None))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_17(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(+unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_18(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[3]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_19(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = None
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_20(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[4] = np.tanh(unconstrained[3])
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_21(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(None)
        return constrained

    def xǁFIGARCHǁtransform_params__mutmut_22(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # |phi| < 1 via tanh
        constrained[1] = np.tanh(unconstrained[1])
        # 0 < d < 1 via sigmoid
        constrained[2] = 1.0 / (1.0 + np.exp(-unconstrained[2]))
        # |beta| < 1 via tanh
        constrained[3] = np.tanh(unconstrained[4])
        return constrained

    xǁFIGARCHǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁFIGARCHǁtransform_params__mutmut_1": xǁFIGARCHǁtransform_params__mutmut_1,
        "xǁFIGARCHǁtransform_params__mutmut_2": xǁFIGARCHǁtransform_params__mutmut_2,
        "xǁFIGARCHǁtransform_params__mutmut_3": xǁFIGARCHǁtransform_params__mutmut_3,
        "xǁFIGARCHǁtransform_params__mutmut_4": xǁFIGARCHǁtransform_params__mutmut_4,
        "xǁFIGARCHǁtransform_params__mutmut_5": xǁFIGARCHǁtransform_params__mutmut_5,
        "xǁFIGARCHǁtransform_params__mutmut_6": xǁFIGARCHǁtransform_params__mutmut_6,
        "xǁFIGARCHǁtransform_params__mutmut_7": xǁFIGARCHǁtransform_params__mutmut_7,
        "xǁFIGARCHǁtransform_params__mutmut_8": xǁFIGARCHǁtransform_params__mutmut_8,
        "xǁFIGARCHǁtransform_params__mutmut_9": xǁFIGARCHǁtransform_params__mutmut_9,
        "xǁFIGARCHǁtransform_params__mutmut_10": xǁFIGARCHǁtransform_params__mutmut_10,
        "xǁFIGARCHǁtransform_params__mutmut_11": xǁFIGARCHǁtransform_params__mutmut_11,
        "xǁFIGARCHǁtransform_params__mutmut_12": xǁFIGARCHǁtransform_params__mutmut_12,
        "xǁFIGARCHǁtransform_params__mutmut_13": xǁFIGARCHǁtransform_params__mutmut_13,
        "xǁFIGARCHǁtransform_params__mutmut_14": xǁFIGARCHǁtransform_params__mutmut_14,
        "xǁFIGARCHǁtransform_params__mutmut_15": xǁFIGARCHǁtransform_params__mutmut_15,
        "xǁFIGARCHǁtransform_params__mutmut_16": xǁFIGARCHǁtransform_params__mutmut_16,
        "xǁFIGARCHǁtransform_params__mutmut_17": xǁFIGARCHǁtransform_params__mutmut_17,
        "xǁFIGARCHǁtransform_params__mutmut_18": xǁFIGARCHǁtransform_params__mutmut_18,
        "xǁFIGARCHǁtransform_params__mutmut_19": xǁFIGARCHǁtransform_params__mutmut_19,
        "xǁFIGARCHǁtransform_params__mutmut_20": xǁFIGARCHǁtransform_params__mutmut_20,
        "xǁFIGARCHǁtransform_params__mutmut_21": xǁFIGARCHǁtransform_params__mutmut_21,
        "xǁFIGARCHǁtransform_params__mutmut_22": xǁFIGARCHǁtransform_params__mutmut_22,
    }
    xǁFIGARCHǁtransform_params__mutmut_orig.__name__ = "xǁFIGARCHǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁFIGARCHǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁFIGARCHǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁFIGARCHǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = None
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = None
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[1] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(None)
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(None, 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], None))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(
            max(
                constrained[0],
            )
        )
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[1], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1.000000000001))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = None
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[2] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(None)
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(None, -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], None, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, None))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(-0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(
            np.clip(
                constrained[1],
                -0.9999,
            )
        )
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[2], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], +0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -1.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 1.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = None
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(None, 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], None, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, None)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_29(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_30(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(
            constrained[2],
            1e-6,
        )
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_31(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[3], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_32(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1.000001, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_33(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 + 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_34(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 2 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_35(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1.000001)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_36(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = None
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_37(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[3] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_38(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(None)
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_39(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped * (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_40(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 + d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_41(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (2.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_42(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = None
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_43(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[4] = np.arctanh(np.clip(constrained[3], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_44(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(None)
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_45(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(None, -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_46(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], None, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_47(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, None))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_48(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(-0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_49(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_50(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(
            np.clip(
                constrained[3],
                -0.9999,
            )
        )
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_51(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[4], -0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_52(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], +0.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_53(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -1.9999, 0.9999))
        return unconstrained

    def xǁFIGARCHǁuntransform_params__mutmut_54(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # phi
        unconstrained[1] = np.arctanh(np.clip(constrained[1], -0.9999, 0.9999))
        # d
        d_clipped = np.clip(constrained[2], 1e-6, 1 - 1e-6)
        unconstrained[2] = np.log(d_clipped / (1.0 - d_clipped))
        # beta
        unconstrained[3] = np.arctanh(np.clip(constrained[3], -0.9999, 1.9999))
        return unconstrained

    xǁFIGARCHǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁFIGARCHǁuntransform_params__mutmut_1": xǁFIGARCHǁuntransform_params__mutmut_1,
        "xǁFIGARCHǁuntransform_params__mutmut_2": xǁFIGARCHǁuntransform_params__mutmut_2,
        "xǁFIGARCHǁuntransform_params__mutmut_3": xǁFIGARCHǁuntransform_params__mutmut_3,
        "xǁFIGARCHǁuntransform_params__mutmut_4": xǁFIGARCHǁuntransform_params__mutmut_4,
        "xǁFIGARCHǁuntransform_params__mutmut_5": xǁFIGARCHǁuntransform_params__mutmut_5,
        "xǁFIGARCHǁuntransform_params__mutmut_6": xǁFIGARCHǁuntransform_params__mutmut_6,
        "xǁFIGARCHǁuntransform_params__mutmut_7": xǁFIGARCHǁuntransform_params__mutmut_7,
        "xǁFIGARCHǁuntransform_params__mutmut_8": xǁFIGARCHǁuntransform_params__mutmut_8,
        "xǁFIGARCHǁuntransform_params__mutmut_9": xǁFIGARCHǁuntransform_params__mutmut_9,
        "xǁFIGARCHǁuntransform_params__mutmut_10": xǁFIGARCHǁuntransform_params__mutmut_10,
        "xǁFIGARCHǁuntransform_params__mutmut_11": xǁFIGARCHǁuntransform_params__mutmut_11,
        "xǁFIGARCHǁuntransform_params__mutmut_12": xǁFIGARCHǁuntransform_params__mutmut_12,
        "xǁFIGARCHǁuntransform_params__mutmut_13": xǁFIGARCHǁuntransform_params__mutmut_13,
        "xǁFIGARCHǁuntransform_params__mutmut_14": xǁFIGARCHǁuntransform_params__mutmut_14,
        "xǁFIGARCHǁuntransform_params__mutmut_15": xǁFIGARCHǁuntransform_params__mutmut_15,
        "xǁFIGARCHǁuntransform_params__mutmut_16": xǁFIGARCHǁuntransform_params__mutmut_16,
        "xǁFIGARCHǁuntransform_params__mutmut_17": xǁFIGARCHǁuntransform_params__mutmut_17,
        "xǁFIGARCHǁuntransform_params__mutmut_18": xǁFIGARCHǁuntransform_params__mutmut_18,
        "xǁFIGARCHǁuntransform_params__mutmut_19": xǁFIGARCHǁuntransform_params__mutmut_19,
        "xǁFIGARCHǁuntransform_params__mutmut_20": xǁFIGARCHǁuntransform_params__mutmut_20,
        "xǁFIGARCHǁuntransform_params__mutmut_21": xǁFIGARCHǁuntransform_params__mutmut_21,
        "xǁFIGARCHǁuntransform_params__mutmut_22": xǁFIGARCHǁuntransform_params__mutmut_22,
        "xǁFIGARCHǁuntransform_params__mutmut_23": xǁFIGARCHǁuntransform_params__mutmut_23,
        "xǁFIGARCHǁuntransform_params__mutmut_24": xǁFIGARCHǁuntransform_params__mutmut_24,
        "xǁFIGARCHǁuntransform_params__mutmut_25": xǁFIGARCHǁuntransform_params__mutmut_25,
        "xǁFIGARCHǁuntransform_params__mutmut_26": xǁFIGARCHǁuntransform_params__mutmut_26,
        "xǁFIGARCHǁuntransform_params__mutmut_27": xǁFIGARCHǁuntransform_params__mutmut_27,
        "xǁFIGARCHǁuntransform_params__mutmut_28": xǁFIGARCHǁuntransform_params__mutmut_28,
        "xǁFIGARCHǁuntransform_params__mutmut_29": xǁFIGARCHǁuntransform_params__mutmut_29,
        "xǁFIGARCHǁuntransform_params__mutmut_30": xǁFIGARCHǁuntransform_params__mutmut_30,
        "xǁFIGARCHǁuntransform_params__mutmut_31": xǁFIGARCHǁuntransform_params__mutmut_31,
        "xǁFIGARCHǁuntransform_params__mutmut_32": xǁFIGARCHǁuntransform_params__mutmut_32,
        "xǁFIGARCHǁuntransform_params__mutmut_33": xǁFIGARCHǁuntransform_params__mutmut_33,
        "xǁFIGARCHǁuntransform_params__mutmut_34": xǁFIGARCHǁuntransform_params__mutmut_34,
        "xǁFIGARCHǁuntransform_params__mutmut_35": xǁFIGARCHǁuntransform_params__mutmut_35,
        "xǁFIGARCHǁuntransform_params__mutmut_36": xǁFIGARCHǁuntransform_params__mutmut_36,
        "xǁFIGARCHǁuntransform_params__mutmut_37": xǁFIGARCHǁuntransform_params__mutmut_37,
        "xǁFIGARCHǁuntransform_params__mutmut_38": xǁFIGARCHǁuntransform_params__mutmut_38,
        "xǁFIGARCHǁuntransform_params__mutmut_39": xǁFIGARCHǁuntransform_params__mutmut_39,
        "xǁFIGARCHǁuntransform_params__mutmut_40": xǁFIGARCHǁuntransform_params__mutmut_40,
        "xǁFIGARCHǁuntransform_params__mutmut_41": xǁFIGARCHǁuntransform_params__mutmut_41,
        "xǁFIGARCHǁuntransform_params__mutmut_42": xǁFIGARCHǁuntransform_params__mutmut_42,
        "xǁFIGARCHǁuntransform_params__mutmut_43": xǁFIGARCHǁuntransform_params__mutmut_43,
        "xǁFIGARCHǁuntransform_params__mutmut_44": xǁFIGARCHǁuntransform_params__mutmut_44,
        "xǁFIGARCHǁuntransform_params__mutmut_45": xǁFIGARCHǁuntransform_params__mutmut_45,
        "xǁFIGARCHǁuntransform_params__mutmut_46": xǁFIGARCHǁuntransform_params__mutmut_46,
        "xǁFIGARCHǁuntransform_params__mutmut_47": xǁFIGARCHǁuntransform_params__mutmut_47,
        "xǁFIGARCHǁuntransform_params__mutmut_48": xǁFIGARCHǁuntransform_params__mutmut_48,
        "xǁFIGARCHǁuntransform_params__mutmut_49": xǁFIGARCHǁuntransform_params__mutmut_49,
        "xǁFIGARCHǁuntransform_params__mutmut_50": xǁFIGARCHǁuntransform_params__mutmut_50,
        "xǁFIGARCHǁuntransform_params__mutmut_51": xǁFIGARCHǁuntransform_params__mutmut_51,
        "xǁFIGARCHǁuntransform_params__mutmut_52": xǁFIGARCHǁuntransform_params__mutmut_52,
        "xǁFIGARCHǁuntransform_params__mutmut_53": xǁFIGARCHǁuntransform_params__mutmut_53,
        "xǁFIGARCHǁuntransform_params__mutmut_54": xǁFIGARCHǁuntransform_params__mutmut_54,
    }
    xǁFIGARCHǁuntransform_params__mutmut_orig.__name__ = "xǁFIGARCHǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁFIGARCHǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁFIGARCHǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁFIGARCHǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1.000000000001, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (+0.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-1.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 1.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (1.001, 0.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (0.001, 1.999),  # 0 < d < 1
            (-0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (+0.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-1.999, 0.999),  # |beta| < 1
        ]

    def xǁFIGARCHǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (-0.999, 0.999),  # |phi| < 1
            (0.001, 0.999),  # 0 < d < 1
            (-0.999, 1.999),  # |beta| < 1
        ]

    xǁFIGARCHǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁFIGARCHǁbounds__mutmut_1": xǁFIGARCHǁbounds__mutmut_1,
        "xǁFIGARCHǁbounds__mutmut_2": xǁFIGARCHǁbounds__mutmut_2,
        "xǁFIGARCHǁbounds__mutmut_3": xǁFIGARCHǁbounds__mutmut_3,
        "xǁFIGARCHǁbounds__mutmut_4": xǁFIGARCHǁbounds__mutmut_4,
        "xǁFIGARCHǁbounds__mutmut_5": xǁFIGARCHǁbounds__mutmut_5,
        "xǁFIGARCHǁbounds__mutmut_6": xǁFIGARCHǁbounds__mutmut_6,
        "xǁFIGARCHǁbounds__mutmut_7": xǁFIGARCHǁbounds__mutmut_7,
        "xǁFIGARCHǁbounds__mutmut_8": xǁFIGARCHǁbounds__mutmut_8,
        "xǁFIGARCHǁbounds__mutmut_9": xǁFIGARCHǁbounds__mutmut_9,
    }
    xǁFIGARCHǁbounds__mutmut_orig.__name__ = "xǁFIGARCHǁbounds"

    @property
    def num_params(self) -> int:
        """Number of parameters: omega, phi, d, beta."""
        return 4
