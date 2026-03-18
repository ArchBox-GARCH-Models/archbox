"""APARCH - Asymmetric Power ARCH model (Ding, Granger & Engle, 1993).

sigma^delta_t = omega + alpha * (|eps_{t-1}| - gamma * eps_{t-1})^delta + beta * sigma^delta_{t-1}
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


class APARCH(VolatilityModel):
    """Asymmetric Power ARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of lagged sigma^delta terms (beta). Default 1.
    q : int
        Number of lagged shock terms (alpha, gamma). Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "APARCH"

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
            object.__getattribute__(self, "xǁAPARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁAPARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁAPARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        p: int = 2,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        p: int = 1,
        q: int = 2,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = None
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = None
        super().__init__(endog, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(None, mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=None, dist=dist)

    def xǁAPARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=None)

    def xǁAPARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(mean=mean, dist=dist)

    def xǁAPARCHǁ__init____mutmut_13(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, dist=dist)

    def xǁAPARCHǁ__init____mutmut_14(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize APARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(
            endog,
            mean=mean,
        )

    xǁAPARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁAPARCHǁ__init____mutmut_1": xǁAPARCHǁ__init____mutmut_1,
        "xǁAPARCHǁ__init____mutmut_2": xǁAPARCHǁ__init____mutmut_2,
        "xǁAPARCHǁ__init____mutmut_3": xǁAPARCHǁ__init____mutmut_3,
        "xǁAPARCHǁ__init____mutmut_4": xǁAPARCHǁ__init____mutmut_4,
        "xǁAPARCHǁ__init____mutmut_5": xǁAPARCHǁ__init____mutmut_5,
        "xǁAPARCHǁ__init____mutmut_6": xǁAPARCHǁ__init____mutmut_6,
        "xǁAPARCHǁ__init____mutmut_7": xǁAPARCHǁ__init____mutmut_7,
        "xǁAPARCHǁ__init____mutmut_8": xǁAPARCHǁ__init____mutmut_8,
        "xǁAPARCHǁ__init____mutmut_9": xǁAPARCHǁ__init____mutmut_9,
        "xǁAPARCHǁ__init____mutmut_10": xǁAPARCHǁ__init____mutmut_10,
        "xǁAPARCHǁ__init____mutmut_11": xǁAPARCHǁ__init____mutmut_11,
        "xǁAPARCHǁ__init____mutmut_12": xǁAPARCHǁ__init____mutmut_12,
        "xǁAPARCHǁ__init____mutmut_13": xǁAPARCHǁ__init____mutmut_13,
        "xǁAPARCHǁ__init____mutmut_14": xǁAPARCHǁ__init____mutmut_14,
    }
    xǁAPARCHǁ__init____mutmut_orig.__name__ = "xǁAPARCHǁ__init__"

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPARCHǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁAPARCHǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁAPARCHǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = None
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[1]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = None
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[2 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 - self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 2 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = None
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 - self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[2 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 - 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 2 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 / self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 3 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = None
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 - 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[2 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 / self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 3 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q - self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 - 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 2 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 / self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 3 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = None

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[+1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-2]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = None
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = None
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(None)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = None

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast * (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta * 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 3.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = None

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[1] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(None, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, None):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(
            1,
        ):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(2, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = None
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(None):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = None
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 + i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t + 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 2 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag > 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 1:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = None
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = None
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) * delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) + gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(None) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] / e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] = alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] -= alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] / shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_58(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] = alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_59(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] -= alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_60(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] / backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_61(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(None):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_62(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = None
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_63(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 + j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_64(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t + 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_65(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 2 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_66(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] = betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_67(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] -= betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_68(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] / (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_69(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag > 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_70(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 1 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_71(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = None

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_72(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(None, 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_73(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], None)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_74(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_75(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(
                sigma_delta[t],
            )

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_76(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1.000000000001)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_77(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = None
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_78(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta * (2.0 / delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_79(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (2.0 * delta)
        return sigma2

    def xǁAPARCHǁ_variance_recursion__mutmut_80(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via APARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1..q, gamma_1..q, beta_1..p, delta]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t.
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]
        delta = params[-1]

        nobs = len(resids)
        sigma_delta = np.empty(nobs)
        backcast_delta = backcast ** (delta / 2.0)

        sigma_delta[0] = backcast_delta

        for t in range(1, nobs):
            sigma_delta[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e = resids[lag]
                    shock = (np.abs(e) - gammas[i] * e) ** delta
                    sigma_delta[t] += alphas[i] * shock
                else:
                    sigma_delta[t] += alphas[i] * backcast_delta
            for j in range(self.p):
                lag = t - 1 - j
                sigma_delta[t] += betas[j] * (sigma_delta[lag] if lag >= 0 else backcast_delta)
            sigma_delta[t] = max(sigma_delta[t], 1e-12)

        # Convert sigma^delta to sigma^2
        sigma2 = sigma_delta ** (3.0 / delta)
        return sigma2

    xǁAPARCHǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁAPARCHǁ_variance_recursion__mutmut_1": xǁAPARCHǁ_variance_recursion__mutmut_1,
        "xǁAPARCHǁ_variance_recursion__mutmut_2": xǁAPARCHǁ_variance_recursion__mutmut_2,
        "xǁAPARCHǁ_variance_recursion__mutmut_3": xǁAPARCHǁ_variance_recursion__mutmut_3,
        "xǁAPARCHǁ_variance_recursion__mutmut_4": xǁAPARCHǁ_variance_recursion__mutmut_4,
        "xǁAPARCHǁ_variance_recursion__mutmut_5": xǁAPARCHǁ_variance_recursion__mutmut_5,
        "xǁAPARCHǁ_variance_recursion__mutmut_6": xǁAPARCHǁ_variance_recursion__mutmut_6,
        "xǁAPARCHǁ_variance_recursion__mutmut_7": xǁAPARCHǁ_variance_recursion__mutmut_7,
        "xǁAPARCHǁ_variance_recursion__mutmut_8": xǁAPARCHǁ_variance_recursion__mutmut_8,
        "xǁAPARCHǁ_variance_recursion__mutmut_9": xǁAPARCHǁ_variance_recursion__mutmut_9,
        "xǁAPARCHǁ_variance_recursion__mutmut_10": xǁAPARCHǁ_variance_recursion__mutmut_10,
        "xǁAPARCHǁ_variance_recursion__mutmut_11": xǁAPARCHǁ_variance_recursion__mutmut_11,
        "xǁAPARCHǁ_variance_recursion__mutmut_12": xǁAPARCHǁ_variance_recursion__mutmut_12,
        "xǁAPARCHǁ_variance_recursion__mutmut_13": xǁAPARCHǁ_variance_recursion__mutmut_13,
        "xǁAPARCHǁ_variance_recursion__mutmut_14": xǁAPARCHǁ_variance_recursion__mutmut_14,
        "xǁAPARCHǁ_variance_recursion__mutmut_15": xǁAPARCHǁ_variance_recursion__mutmut_15,
        "xǁAPARCHǁ_variance_recursion__mutmut_16": xǁAPARCHǁ_variance_recursion__mutmut_16,
        "xǁAPARCHǁ_variance_recursion__mutmut_17": xǁAPARCHǁ_variance_recursion__mutmut_17,
        "xǁAPARCHǁ_variance_recursion__mutmut_18": xǁAPARCHǁ_variance_recursion__mutmut_18,
        "xǁAPARCHǁ_variance_recursion__mutmut_19": xǁAPARCHǁ_variance_recursion__mutmut_19,
        "xǁAPARCHǁ_variance_recursion__mutmut_20": xǁAPARCHǁ_variance_recursion__mutmut_20,
        "xǁAPARCHǁ_variance_recursion__mutmut_21": xǁAPARCHǁ_variance_recursion__mutmut_21,
        "xǁAPARCHǁ_variance_recursion__mutmut_22": xǁAPARCHǁ_variance_recursion__mutmut_22,
        "xǁAPARCHǁ_variance_recursion__mutmut_23": xǁAPARCHǁ_variance_recursion__mutmut_23,
        "xǁAPARCHǁ_variance_recursion__mutmut_24": xǁAPARCHǁ_variance_recursion__mutmut_24,
        "xǁAPARCHǁ_variance_recursion__mutmut_25": xǁAPARCHǁ_variance_recursion__mutmut_25,
        "xǁAPARCHǁ_variance_recursion__mutmut_26": xǁAPARCHǁ_variance_recursion__mutmut_26,
        "xǁAPARCHǁ_variance_recursion__mutmut_27": xǁAPARCHǁ_variance_recursion__mutmut_27,
        "xǁAPARCHǁ_variance_recursion__mutmut_28": xǁAPARCHǁ_variance_recursion__mutmut_28,
        "xǁAPARCHǁ_variance_recursion__mutmut_29": xǁAPARCHǁ_variance_recursion__mutmut_29,
        "xǁAPARCHǁ_variance_recursion__mutmut_30": xǁAPARCHǁ_variance_recursion__mutmut_30,
        "xǁAPARCHǁ_variance_recursion__mutmut_31": xǁAPARCHǁ_variance_recursion__mutmut_31,
        "xǁAPARCHǁ_variance_recursion__mutmut_32": xǁAPARCHǁ_variance_recursion__mutmut_32,
        "xǁAPARCHǁ_variance_recursion__mutmut_33": xǁAPARCHǁ_variance_recursion__mutmut_33,
        "xǁAPARCHǁ_variance_recursion__mutmut_34": xǁAPARCHǁ_variance_recursion__mutmut_34,
        "xǁAPARCHǁ_variance_recursion__mutmut_35": xǁAPARCHǁ_variance_recursion__mutmut_35,
        "xǁAPARCHǁ_variance_recursion__mutmut_36": xǁAPARCHǁ_variance_recursion__mutmut_36,
        "xǁAPARCHǁ_variance_recursion__mutmut_37": xǁAPARCHǁ_variance_recursion__mutmut_37,
        "xǁAPARCHǁ_variance_recursion__mutmut_38": xǁAPARCHǁ_variance_recursion__mutmut_38,
        "xǁAPARCHǁ_variance_recursion__mutmut_39": xǁAPARCHǁ_variance_recursion__mutmut_39,
        "xǁAPARCHǁ_variance_recursion__mutmut_40": xǁAPARCHǁ_variance_recursion__mutmut_40,
        "xǁAPARCHǁ_variance_recursion__mutmut_41": xǁAPARCHǁ_variance_recursion__mutmut_41,
        "xǁAPARCHǁ_variance_recursion__mutmut_42": xǁAPARCHǁ_variance_recursion__mutmut_42,
        "xǁAPARCHǁ_variance_recursion__mutmut_43": xǁAPARCHǁ_variance_recursion__mutmut_43,
        "xǁAPARCHǁ_variance_recursion__mutmut_44": xǁAPARCHǁ_variance_recursion__mutmut_44,
        "xǁAPARCHǁ_variance_recursion__mutmut_45": xǁAPARCHǁ_variance_recursion__mutmut_45,
        "xǁAPARCHǁ_variance_recursion__mutmut_46": xǁAPARCHǁ_variance_recursion__mutmut_46,
        "xǁAPARCHǁ_variance_recursion__mutmut_47": xǁAPARCHǁ_variance_recursion__mutmut_47,
        "xǁAPARCHǁ_variance_recursion__mutmut_48": xǁAPARCHǁ_variance_recursion__mutmut_48,
        "xǁAPARCHǁ_variance_recursion__mutmut_49": xǁAPARCHǁ_variance_recursion__mutmut_49,
        "xǁAPARCHǁ_variance_recursion__mutmut_50": xǁAPARCHǁ_variance_recursion__mutmut_50,
        "xǁAPARCHǁ_variance_recursion__mutmut_51": xǁAPARCHǁ_variance_recursion__mutmut_51,
        "xǁAPARCHǁ_variance_recursion__mutmut_52": xǁAPARCHǁ_variance_recursion__mutmut_52,
        "xǁAPARCHǁ_variance_recursion__mutmut_53": xǁAPARCHǁ_variance_recursion__mutmut_53,
        "xǁAPARCHǁ_variance_recursion__mutmut_54": xǁAPARCHǁ_variance_recursion__mutmut_54,
        "xǁAPARCHǁ_variance_recursion__mutmut_55": xǁAPARCHǁ_variance_recursion__mutmut_55,
        "xǁAPARCHǁ_variance_recursion__mutmut_56": xǁAPARCHǁ_variance_recursion__mutmut_56,
        "xǁAPARCHǁ_variance_recursion__mutmut_57": xǁAPARCHǁ_variance_recursion__mutmut_57,
        "xǁAPARCHǁ_variance_recursion__mutmut_58": xǁAPARCHǁ_variance_recursion__mutmut_58,
        "xǁAPARCHǁ_variance_recursion__mutmut_59": xǁAPARCHǁ_variance_recursion__mutmut_59,
        "xǁAPARCHǁ_variance_recursion__mutmut_60": xǁAPARCHǁ_variance_recursion__mutmut_60,
        "xǁAPARCHǁ_variance_recursion__mutmut_61": xǁAPARCHǁ_variance_recursion__mutmut_61,
        "xǁAPARCHǁ_variance_recursion__mutmut_62": xǁAPARCHǁ_variance_recursion__mutmut_62,
        "xǁAPARCHǁ_variance_recursion__mutmut_63": xǁAPARCHǁ_variance_recursion__mutmut_63,
        "xǁAPARCHǁ_variance_recursion__mutmut_64": xǁAPARCHǁ_variance_recursion__mutmut_64,
        "xǁAPARCHǁ_variance_recursion__mutmut_65": xǁAPARCHǁ_variance_recursion__mutmut_65,
        "xǁAPARCHǁ_variance_recursion__mutmut_66": xǁAPARCHǁ_variance_recursion__mutmut_66,
        "xǁAPARCHǁ_variance_recursion__mutmut_67": xǁAPARCHǁ_variance_recursion__mutmut_67,
        "xǁAPARCHǁ_variance_recursion__mutmut_68": xǁAPARCHǁ_variance_recursion__mutmut_68,
        "xǁAPARCHǁ_variance_recursion__mutmut_69": xǁAPARCHǁ_variance_recursion__mutmut_69,
        "xǁAPARCHǁ_variance_recursion__mutmut_70": xǁAPARCHǁ_variance_recursion__mutmut_70,
        "xǁAPARCHǁ_variance_recursion__mutmut_71": xǁAPARCHǁ_variance_recursion__mutmut_71,
        "xǁAPARCHǁ_variance_recursion__mutmut_72": xǁAPARCHǁ_variance_recursion__mutmut_72,
        "xǁAPARCHǁ_variance_recursion__mutmut_73": xǁAPARCHǁ_variance_recursion__mutmut_73,
        "xǁAPARCHǁ_variance_recursion__mutmut_74": xǁAPARCHǁ_variance_recursion__mutmut_74,
        "xǁAPARCHǁ_variance_recursion__mutmut_75": xǁAPARCHǁ_variance_recursion__mutmut_75,
        "xǁAPARCHǁ_variance_recursion__mutmut_76": xǁAPARCHǁ_variance_recursion__mutmut_76,
        "xǁAPARCHǁ_variance_recursion__mutmut_77": xǁAPARCHǁ_variance_recursion__mutmut_77,
        "xǁAPARCHǁ_variance_recursion__mutmut_78": xǁAPARCHǁ_variance_recursion__mutmut_78,
        "xǁAPARCHǁ_variance_recursion__mutmut_79": xǁAPARCHǁ_variance_recursion__mutmut_79,
        "xǁAPARCHǁ_variance_recursion__mutmut_80": xǁAPARCHǁ_variance_recursion__mutmut_80,
    }
    xǁAPARCHǁ_variance_recursion__mutmut_orig.__name__ = "xǁAPARCHǁ_variance_recursion"

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPARCHǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁAPARCHǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁAPARCHǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = None
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[1]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = None
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[2]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = None
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 - self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[2 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = None
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 - 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[2 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 / self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 3 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = None

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[+1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-2]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = None
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev * (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta * 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_19(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 3.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = None
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_21(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) * delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_22(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) + gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_23(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(None) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_24(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma / eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_25(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = None
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_26(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock - beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_27(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega - alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_28(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha / shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_29(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta / sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_30(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = None
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_31(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(None, 1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_32(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, None)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_33(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(1e-12)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_34(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(
            sigma_delta,
        )
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_35(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1.000000000001)
        return float(sigma_delta ** (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_36(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(None)

    def xǁAPARCHǁ_one_step_variance__mutmut_37(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta * (2.0 / delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_38(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (2.0 * delta))

    def xǁAPARCHǁ_one_step_variance__mutmut_39(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]
        delta = params[-1]

        sigma_delta_prev = sigma2_prev ** (delta / 2.0)
        shock = (np.abs(eps) - gamma * eps) ** delta
        sigma_delta = omega + alpha * shock + beta * sigma_delta_prev
        sigma_delta = max(sigma_delta, 1e-12)
        return float(sigma_delta ** (3.0 / delta))

    xǁAPARCHǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁAPARCHǁ_one_step_variance__mutmut_1": xǁAPARCHǁ_one_step_variance__mutmut_1,
        "xǁAPARCHǁ_one_step_variance__mutmut_2": xǁAPARCHǁ_one_step_variance__mutmut_2,
        "xǁAPARCHǁ_one_step_variance__mutmut_3": xǁAPARCHǁ_one_step_variance__mutmut_3,
        "xǁAPARCHǁ_one_step_variance__mutmut_4": xǁAPARCHǁ_one_step_variance__mutmut_4,
        "xǁAPARCHǁ_one_step_variance__mutmut_5": xǁAPARCHǁ_one_step_variance__mutmut_5,
        "xǁAPARCHǁ_one_step_variance__mutmut_6": xǁAPARCHǁ_one_step_variance__mutmut_6,
        "xǁAPARCHǁ_one_step_variance__mutmut_7": xǁAPARCHǁ_one_step_variance__mutmut_7,
        "xǁAPARCHǁ_one_step_variance__mutmut_8": xǁAPARCHǁ_one_step_variance__mutmut_8,
        "xǁAPARCHǁ_one_step_variance__mutmut_9": xǁAPARCHǁ_one_step_variance__mutmut_9,
        "xǁAPARCHǁ_one_step_variance__mutmut_10": xǁAPARCHǁ_one_step_variance__mutmut_10,
        "xǁAPARCHǁ_one_step_variance__mutmut_11": xǁAPARCHǁ_one_step_variance__mutmut_11,
        "xǁAPARCHǁ_one_step_variance__mutmut_12": xǁAPARCHǁ_one_step_variance__mutmut_12,
        "xǁAPARCHǁ_one_step_variance__mutmut_13": xǁAPARCHǁ_one_step_variance__mutmut_13,
        "xǁAPARCHǁ_one_step_variance__mutmut_14": xǁAPARCHǁ_one_step_variance__mutmut_14,
        "xǁAPARCHǁ_one_step_variance__mutmut_15": xǁAPARCHǁ_one_step_variance__mutmut_15,
        "xǁAPARCHǁ_one_step_variance__mutmut_16": xǁAPARCHǁ_one_step_variance__mutmut_16,
        "xǁAPARCHǁ_one_step_variance__mutmut_17": xǁAPARCHǁ_one_step_variance__mutmut_17,
        "xǁAPARCHǁ_one_step_variance__mutmut_18": xǁAPARCHǁ_one_step_variance__mutmut_18,
        "xǁAPARCHǁ_one_step_variance__mutmut_19": xǁAPARCHǁ_one_step_variance__mutmut_19,
        "xǁAPARCHǁ_one_step_variance__mutmut_20": xǁAPARCHǁ_one_step_variance__mutmut_20,
        "xǁAPARCHǁ_one_step_variance__mutmut_21": xǁAPARCHǁ_one_step_variance__mutmut_21,
        "xǁAPARCHǁ_one_step_variance__mutmut_22": xǁAPARCHǁ_one_step_variance__mutmut_22,
        "xǁAPARCHǁ_one_step_variance__mutmut_23": xǁAPARCHǁ_one_step_variance__mutmut_23,
        "xǁAPARCHǁ_one_step_variance__mutmut_24": xǁAPARCHǁ_one_step_variance__mutmut_24,
        "xǁAPARCHǁ_one_step_variance__mutmut_25": xǁAPARCHǁ_one_step_variance__mutmut_25,
        "xǁAPARCHǁ_one_step_variance__mutmut_26": xǁAPARCHǁ_one_step_variance__mutmut_26,
        "xǁAPARCHǁ_one_step_variance__mutmut_27": xǁAPARCHǁ_one_step_variance__mutmut_27,
        "xǁAPARCHǁ_one_step_variance__mutmut_28": xǁAPARCHǁ_one_step_variance__mutmut_28,
        "xǁAPARCHǁ_one_step_variance__mutmut_29": xǁAPARCHǁ_one_step_variance__mutmut_29,
        "xǁAPARCHǁ_one_step_variance__mutmut_30": xǁAPARCHǁ_one_step_variance__mutmut_30,
        "xǁAPARCHǁ_one_step_variance__mutmut_31": xǁAPARCHǁ_one_step_variance__mutmut_31,
        "xǁAPARCHǁ_one_step_variance__mutmut_32": xǁAPARCHǁ_one_step_variance__mutmut_32,
        "xǁAPARCHǁ_one_step_variance__mutmut_33": xǁAPARCHǁ_one_step_variance__mutmut_33,
        "xǁAPARCHǁ_one_step_variance__mutmut_34": xǁAPARCHǁ_one_step_variance__mutmut_34,
        "xǁAPARCHǁ_one_step_variance__mutmut_35": xǁAPARCHǁ_one_step_variance__mutmut_35,
        "xǁAPARCHǁ_one_step_variance__mutmut_36": xǁAPARCHǁ_one_step_variance__mutmut_36,
        "xǁAPARCHǁ_one_step_variance__mutmut_37": xǁAPARCHǁ_one_step_variance__mutmut_37,
        "xǁAPARCHǁ_one_step_variance__mutmut_38": xǁAPARCHǁ_one_step_variance__mutmut_38,
        "xǁAPARCHǁ_one_step_variance__mutmut_39": xǁAPARCHǁ_one_step_variance__mutmut_39,
    }
    xǁAPARCHǁ_one_step_variance__mutmut_orig.__name__ = "xǁAPARCHǁ_one_step_variance"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        var = np.var(self.endog)
        omega = var * 0.01
        alphas = np.full(self.q, 0.05)
        gammas = np.full(self.q, 0.0)
        betas = np.full(self.p, 0.90)
        delta = np.array([2.0])
        return np.concatenate([[omega], alphas, gammas, betas, delta])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["omega"]
        names += [f"alpha[{i + 1}]" for i in range(self.q)]
        names += [f"gamma[{i + 1}]" for i in range(self.q)]
        names += [f"beta[{i + 1}]" for i in range(self.p)]
        names += ["delta"]
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPARCHǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁAPARCHǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁAPARCHǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = None
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = None
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(None, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, None, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, None)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(-20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(
            unconstrained,
            -20.0,
        )
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, +20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -21.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 21.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = None
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[1] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(None)
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[1])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(None):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_17(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = None
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_18(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 - i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_19(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[2 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_20(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(None)
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_21(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 - i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_22(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[2 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_23(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(None):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_24(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = None
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_25(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q - i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_26(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 - self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_27(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 2 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_28(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = None
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_29(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(None)
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_30(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(None):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_31(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = None
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_32(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q - j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_33(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 - 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_34(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 2 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_35(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 / self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_36(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 3 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_37(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = None
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_38(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(None)
        # delta > 0
        constrained[-1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_39(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = None
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_40(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[+1] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_41(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-2] = np.exp(clipped[-1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_42(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(None)
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_43(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[+1])
        return constrained

    def xǁAPARCHǁtransform_params__mutmut_44(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        clipped = np.clip(unconstrained, -20.0, 20.0)
        # omega > 0
        constrained[0] = np.exp(clipped[0])
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(clipped[1 + i])
        # gammas: |gamma| <= 1 via tanh
        for i in range(self.q):
            idx = 1 + self.q + i
            constrained[idx] = np.tanh(unconstrained[idx])
        # betas >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(clipped[idx])
        # delta > 0
        constrained[-1] = np.exp(clipped[-2])
        return constrained

    xǁAPARCHǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁAPARCHǁtransform_params__mutmut_1": xǁAPARCHǁtransform_params__mutmut_1,
        "xǁAPARCHǁtransform_params__mutmut_2": xǁAPARCHǁtransform_params__mutmut_2,
        "xǁAPARCHǁtransform_params__mutmut_3": xǁAPARCHǁtransform_params__mutmut_3,
        "xǁAPARCHǁtransform_params__mutmut_4": xǁAPARCHǁtransform_params__mutmut_4,
        "xǁAPARCHǁtransform_params__mutmut_5": xǁAPARCHǁtransform_params__mutmut_5,
        "xǁAPARCHǁtransform_params__mutmut_6": xǁAPARCHǁtransform_params__mutmut_6,
        "xǁAPARCHǁtransform_params__mutmut_7": xǁAPARCHǁtransform_params__mutmut_7,
        "xǁAPARCHǁtransform_params__mutmut_8": xǁAPARCHǁtransform_params__mutmut_8,
        "xǁAPARCHǁtransform_params__mutmut_9": xǁAPARCHǁtransform_params__mutmut_9,
        "xǁAPARCHǁtransform_params__mutmut_10": xǁAPARCHǁtransform_params__mutmut_10,
        "xǁAPARCHǁtransform_params__mutmut_11": xǁAPARCHǁtransform_params__mutmut_11,
        "xǁAPARCHǁtransform_params__mutmut_12": xǁAPARCHǁtransform_params__mutmut_12,
        "xǁAPARCHǁtransform_params__mutmut_13": xǁAPARCHǁtransform_params__mutmut_13,
        "xǁAPARCHǁtransform_params__mutmut_14": xǁAPARCHǁtransform_params__mutmut_14,
        "xǁAPARCHǁtransform_params__mutmut_15": xǁAPARCHǁtransform_params__mutmut_15,
        "xǁAPARCHǁtransform_params__mutmut_16": xǁAPARCHǁtransform_params__mutmut_16,
        "xǁAPARCHǁtransform_params__mutmut_17": xǁAPARCHǁtransform_params__mutmut_17,
        "xǁAPARCHǁtransform_params__mutmut_18": xǁAPARCHǁtransform_params__mutmut_18,
        "xǁAPARCHǁtransform_params__mutmut_19": xǁAPARCHǁtransform_params__mutmut_19,
        "xǁAPARCHǁtransform_params__mutmut_20": xǁAPARCHǁtransform_params__mutmut_20,
        "xǁAPARCHǁtransform_params__mutmut_21": xǁAPARCHǁtransform_params__mutmut_21,
        "xǁAPARCHǁtransform_params__mutmut_22": xǁAPARCHǁtransform_params__mutmut_22,
        "xǁAPARCHǁtransform_params__mutmut_23": xǁAPARCHǁtransform_params__mutmut_23,
        "xǁAPARCHǁtransform_params__mutmut_24": xǁAPARCHǁtransform_params__mutmut_24,
        "xǁAPARCHǁtransform_params__mutmut_25": xǁAPARCHǁtransform_params__mutmut_25,
        "xǁAPARCHǁtransform_params__mutmut_26": xǁAPARCHǁtransform_params__mutmut_26,
        "xǁAPARCHǁtransform_params__mutmut_27": xǁAPARCHǁtransform_params__mutmut_27,
        "xǁAPARCHǁtransform_params__mutmut_28": xǁAPARCHǁtransform_params__mutmut_28,
        "xǁAPARCHǁtransform_params__mutmut_29": xǁAPARCHǁtransform_params__mutmut_29,
        "xǁAPARCHǁtransform_params__mutmut_30": xǁAPARCHǁtransform_params__mutmut_30,
        "xǁAPARCHǁtransform_params__mutmut_31": xǁAPARCHǁtransform_params__mutmut_31,
        "xǁAPARCHǁtransform_params__mutmut_32": xǁAPARCHǁtransform_params__mutmut_32,
        "xǁAPARCHǁtransform_params__mutmut_33": xǁAPARCHǁtransform_params__mutmut_33,
        "xǁAPARCHǁtransform_params__mutmut_34": xǁAPARCHǁtransform_params__mutmut_34,
        "xǁAPARCHǁtransform_params__mutmut_35": xǁAPARCHǁtransform_params__mutmut_35,
        "xǁAPARCHǁtransform_params__mutmut_36": xǁAPARCHǁtransform_params__mutmut_36,
        "xǁAPARCHǁtransform_params__mutmut_37": xǁAPARCHǁtransform_params__mutmut_37,
        "xǁAPARCHǁtransform_params__mutmut_38": xǁAPARCHǁtransform_params__mutmut_38,
        "xǁAPARCHǁtransform_params__mutmut_39": xǁAPARCHǁtransform_params__mutmut_39,
        "xǁAPARCHǁtransform_params__mutmut_40": xǁAPARCHǁtransform_params__mutmut_40,
        "xǁAPARCHǁtransform_params__mutmut_41": xǁAPARCHǁtransform_params__mutmut_41,
        "xǁAPARCHǁtransform_params__mutmut_42": xǁAPARCHǁtransform_params__mutmut_42,
        "xǁAPARCHǁtransform_params__mutmut_43": xǁAPARCHǁtransform_params__mutmut_43,
        "xǁAPARCHǁtransform_params__mutmut_44": xǁAPARCHǁtransform_params__mutmut_44,
    }
    xǁAPARCHǁtransform_params__mutmut_orig.__name__ = "xǁAPARCHǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPARCHǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁAPARCHǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁAPARCHǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = None
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = None
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[1] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(None)
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(None, 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], None))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_8(
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
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[1], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1.000000000001))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(None):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = None
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 - i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[2 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(None)
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(None, 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], None))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(
                max(
                    constrained[1 + i],
                )
            )
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 - i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[2 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1.000000000001))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(None):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = None
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q - i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 - self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 2 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = None
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_29(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(None)
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_30(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(None, -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_31(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], None, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_32(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, None))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_33(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(-0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_34(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_35(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(
                np.clip(
                    constrained[idx],
                    -0.9999,
                )
            )
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_36(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], +0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_37(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -1.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_38(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 1.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_39(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(None):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_40(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = None
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_41(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q - j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_42(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 - 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_43(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 2 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_44(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 / self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_45(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 3 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_46(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = None
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_47(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(None)
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_48(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(None, 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_49(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], None))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_50(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_51(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(
                max(
                    constrained[idx],
                )
            )
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_52(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1.000000000001))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_53(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = None
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_54(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[+1] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_55(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-2] = np.log(max(constrained[-1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_56(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(None)
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_57(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(None, 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_58(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], None))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_59(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_60(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(
            max(
                constrained[-1],
            )
        )
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_61(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[+1], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_62(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-2], 1e-12))
        return unconstrained

    def xǁAPARCHǁuntransform_params__mutmut_63(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas
        for i in range(self.q):
            idx = 1 + self.q + i
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # delta
        unconstrained[-1] = np.log(max(constrained[-1], 1.000000000001))
        return unconstrained

    xǁAPARCHǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁAPARCHǁuntransform_params__mutmut_1": xǁAPARCHǁuntransform_params__mutmut_1,
        "xǁAPARCHǁuntransform_params__mutmut_2": xǁAPARCHǁuntransform_params__mutmut_2,
        "xǁAPARCHǁuntransform_params__mutmut_3": xǁAPARCHǁuntransform_params__mutmut_3,
        "xǁAPARCHǁuntransform_params__mutmut_4": xǁAPARCHǁuntransform_params__mutmut_4,
        "xǁAPARCHǁuntransform_params__mutmut_5": xǁAPARCHǁuntransform_params__mutmut_5,
        "xǁAPARCHǁuntransform_params__mutmut_6": xǁAPARCHǁuntransform_params__mutmut_6,
        "xǁAPARCHǁuntransform_params__mutmut_7": xǁAPARCHǁuntransform_params__mutmut_7,
        "xǁAPARCHǁuntransform_params__mutmut_8": xǁAPARCHǁuntransform_params__mutmut_8,
        "xǁAPARCHǁuntransform_params__mutmut_9": xǁAPARCHǁuntransform_params__mutmut_9,
        "xǁAPARCHǁuntransform_params__mutmut_10": xǁAPARCHǁuntransform_params__mutmut_10,
        "xǁAPARCHǁuntransform_params__mutmut_11": xǁAPARCHǁuntransform_params__mutmut_11,
        "xǁAPARCHǁuntransform_params__mutmut_12": xǁAPARCHǁuntransform_params__mutmut_12,
        "xǁAPARCHǁuntransform_params__mutmut_13": xǁAPARCHǁuntransform_params__mutmut_13,
        "xǁAPARCHǁuntransform_params__mutmut_14": xǁAPARCHǁuntransform_params__mutmut_14,
        "xǁAPARCHǁuntransform_params__mutmut_15": xǁAPARCHǁuntransform_params__mutmut_15,
        "xǁAPARCHǁuntransform_params__mutmut_16": xǁAPARCHǁuntransform_params__mutmut_16,
        "xǁAPARCHǁuntransform_params__mutmut_17": xǁAPARCHǁuntransform_params__mutmut_17,
        "xǁAPARCHǁuntransform_params__mutmut_18": xǁAPARCHǁuntransform_params__mutmut_18,
        "xǁAPARCHǁuntransform_params__mutmut_19": xǁAPARCHǁuntransform_params__mutmut_19,
        "xǁAPARCHǁuntransform_params__mutmut_20": xǁAPARCHǁuntransform_params__mutmut_20,
        "xǁAPARCHǁuntransform_params__mutmut_21": xǁAPARCHǁuntransform_params__mutmut_21,
        "xǁAPARCHǁuntransform_params__mutmut_22": xǁAPARCHǁuntransform_params__mutmut_22,
        "xǁAPARCHǁuntransform_params__mutmut_23": xǁAPARCHǁuntransform_params__mutmut_23,
        "xǁAPARCHǁuntransform_params__mutmut_24": xǁAPARCHǁuntransform_params__mutmut_24,
        "xǁAPARCHǁuntransform_params__mutmut_25": xǁAPARCHǁuntransform_params__mutmut_25,
        "xǁAPARCHǁuntransform_params__mutmut_26": xǁAPARCHǁuntransform_params__mutmut_26,
        "xǁAPARCHǁuntransform_params__mutmut_27": xǁAPARCHǁuntransform_params__mutmut_27,
        "xǁAPARCHǁuntransform_params__mutmut_28": xǁAPARCHǁuntransform_params__mutmut_28,
        "xǁAPARCHǁuntransform_params__mutmut_29": xǁAPARCHǁuntransform_params__mutmut_29,
        "xǁAPARCHǁuntransform_params__mutmut_30": xǁAPARCHǁuntransform_params__mutmut_30,
        "xǁAPARCHǁuntransform_params__mutmut_31": xǁAPARCHǁuntransform_params__mutmut_31,
        "xǁAPARCHǁuntransform_params__mutmut_32": xǁAPARCHǁuntransform_params__mutmut_32,
        "xǁAPARCHǁuntransform_params__mutmut_33": xǁAPARCHǁuntransform_params__mutmut_33,
        "xǁAPARCHǁuntransform_params__mutmut_34": xǁAPARCHǁuntransform_params__mutmut_34,
        "xǁAPARCHǁuntransform_params__mutmut_35": xǁAPARCHǁuntransform_params__mutmut_35,
        "xǁAPARCHǁuntransform_params__mutmut_36": xǁAPARCHǁuntransform_params__mutmut_36,
        "xǁAPARCHǁuntransform_params__mutmut_37": xǁAPARCHǁuntransform_params__mutmut_37,
        "xǁAPARCHǁuntransform_params__mutmut_38": xǁAPARCHǁuntransform_params__mutmut_38,
        "xǁAPARCHǁuntransform_params__mutmut_39": xǁAPARCHǁuntransform_params__mutmut_39,
        "xǁAPARCHǁuntransform_params__mutmut_40": xǁAPARCHǁuntransform_params__mutmut_40,
        "xǁAPARCHǁuntransform_params__mutmut_41": xǁAPARCHǁuntransform_params__mutmut_41,
        "xǁAPARCHǁuntransform_params__mutmut_42": xǁAPARCHǁuntransform_params__mutmut_42,
        "xǁAPARCHǁuntransform_params__mutmut_43": xǁAPARCHǁuntransform_params__mutmut_43,
        "xǁAPARCHǁuntransform_params__mutmut_44": xǁAPARCHǁuntransform_params__mutmut_44,
        "xǁAPARCHǁuntransform_params__mutmut_45": xǁAPARCHǁuntransform_params__mutmut_45,
        "xǁAPARCHǁuntransform_params__mutmut_46": xǁAPARCHǁuntransform_params__mutmut_46,
        "xǁAPARCHǁuntransform_params__mutmut_47": xǁAPARCHǁuntransform_params__mutmut_47,
        "xǁAPARCHǁuntransform_params__mutmut_48": xǁAPARCHǁuntransform_params__mutmut_48,
        "xǁAPARCHǁuntransform_params__mutmut_49": xǁAPARCHǁuntransform_params__mutmut_49,
        "xǁAPARCHǁuntransform_params__mutmut_50": xǁAPARCHǁuntransform_params__mutmut_50,
        "xǁAPARCHǁuntransform_params__mutmut_51": xǁAPARCHǁuntransform_params__mutmut_51,
        "xǁAPARCHǁuntransform_params__mutmut_52": xǁAPARCHǁuntransform_params__mutmut_52,
        "xǁAPARCHǁuntransform_params__mutmut_53": xǁAPARCHǁuntransform_params__mutmut_53,
        "xǁAPARCHǁuntransform_params__mutmut_54": xǁAPARCHǁuntransform_params__mutmut_54,
        "xǁAPARCHǁuntransform_params__mutmut_55": xǁAPARCHǁuntransform_params__mutmut_55,
        "xǁAPARCHǁuntransform_params__mutmut_56": xǁAPARCHǁuntransform_params__mutmut_56,
        "xǁAPARCHǁuntransform_params__mutmut_57": xǁAPARCHǁuntransform_params__mutmut_57,
        "xǁAPARCHǁuntransform_params__mutmut_58": xǁAPARCHǁuntransform_params__mutmut_58,
        "xǁAPARCHǁuntransform_params__mutmut_59": xǁAPARCHǁuntransform_params__mutmut_59,
        "xǁAPARCHǁuntransform_params__mutmut_60": xǁAPARCHǁuntransform_params__mutmut_60,
        "xǁAPARCHǁuntransform_params__mutmut_61": xǁAPARCHǁuntransform_params__mutmut_61,
        "xǁAPARCHǁuntransform_params__mutmut_62": xǁAPARCHǁuntransform_params__mutmut_62,
        "xǁAPARCHǁuntransform_params__mutmut_63": xǁAPARCHǁuntransform_params__mutmut_63,
    }
    xǁAPARCHǁuntransform_params__mutmut_orig.__name__ = "xǁAPARCHǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPARCHǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁAPARCHǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁAPARCHǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = None
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append(None)
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1.000000000001, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(None):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append(None)
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((1.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(None):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append(None)
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((+0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_10(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-1.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_11(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 1.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_12(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(None):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_13(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append(None)
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_14(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((1.0, np.inf))
        # delta > 0
        bnds.append((0.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_15(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append(None)
        return bnds

    def xǁAPARCHǁbounds__mutmut_16(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((1.01, 10.0))
        return bnds

    def xǁAPARCHǁbounds__mutmut_17(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: |gamma| <= 1
        for _ in range(self.q):
            bnds.append((-0.9999, 0.9999))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        # delta > 0
        bnds.append((0.01, 11.0))
        return bnds

    xǁAPARCHǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁAPARCHǁbounds__mutmut_1": xǁAPARCHǁbounds__mutmut_1,
        "xǁAPARCHǁbounds__mutmut_2": xǁAPARCHǁbounds__mutmut_2,
        "xǁAPARCHǁbounds__mutmut_3": xǁAPARCHǁbounds__mutmut_3,
        "xǁAPARCHǁbounds__mutmut_4": xǁAPARCHǁbounds__mutmut_4,
        "xǁAPARCHǁbounds__mutmut_5": xǁAPARCHǁbounds__mutmut_5,
        "xǁAPARCHǁbounds__mutmut_6": xǁAPARCHǁbounds__mutmut_6,
        "xǁAPARCHǁbounds__mutmut_7": xǁAPARCHǁbounds__mutmut_7,
        "xǁAPARCHǁbounds__mutmut_8": xǁAPARCHǁbounds__mutmut_8,
        "xǁAPARCHǁbounds__mutmut_9": xǁAPARCHǁbounds__mutmut_9,
        "xǁAPARCHǁbounds__mutmut_10": xǁAPARCHǁbounds__mutmut_10,
        "xǁAPARCHǁbounds__mutmut_11": xǁAPARCHǁbounds__mutmut_11,
        "xǁAPARCHǁbounds__mutmut_12": xǁAPARCHǁbounds__mutmut_12,
        "xǁAPARCHǁbounds__mutmut_13": xǁAPARCHǁbounds__mutmut_13,
        "xǁAPARCHǁbounds__mutmut_14": xǁAPARCHǁbounds__mutmut_14,
        "xǁAPARCHǁbounds__mutmut_15": xǁAPARCHǁbounds__mutmut_15,
        "xǁAPARCHǁbounds__mutmut_16": xǁAPARCHǁbounds__mutmut_16,
        "xǁAPARCHǁbounds__mutmut_17": xǁAPARCHǁbounds__mutmut_17,
    }
    xǁAPARCHǁbounds__mutmut_orig.__name__ = "xǁAPARCHǁbounds"

    @property
    def num_params(self) -> int:
        """Number of model parameters: omega + q alphas + q gammas + p betas + delta."""
        return 1 + 2 * self.q + self.p + 1
