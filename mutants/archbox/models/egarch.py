"""EGARCH - Exponential GARCH model (Nelson, 1991).

log(sigma^2_t) = omega + alpha * |z_{t-1}| + gamma * z_{t-1} + beta * log(sigma^2_{t-1})

onde z_t = eps_t / sigma_t (residuo padronizado).
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


class EGARCH(VolatilityModel):
    """Exponential GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of lagged log-variance terms (beta). Default 1.
    q : int
        Number of lagged shock terms (alpha, gamma). Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution: 'normal', 'studentt', etc.
    """

    volatility_process = "EGARCH"

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
            object.__getattribute__(self, "xǁEGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁEGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        p: int = 2,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        p: int = 1,
        q: int = 2,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = None
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = None
        super().__init__(endog, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(None, mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=None, dist=dist)

    def xǁEGARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=None)

    def xǁEGARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(mean=mean, dist=dist)

    def xǁEGARCHǁ__init____mutmut_13(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, dist=dist)

    def xǁEGARCHǁ__init____mutmut_14(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize EGARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(
            endog,
            mean=mean,
        )

    xǁEGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEGARCHǁ__init____mutmut_1": xǁEGARCHǁ__init____mutmut_1,
        "xǁEGARCHǁ__init____mutmut_2": xǁEGARCHǁ__init____mutmut_2,
        "xǁEGARCHǁ__init____mutmut_3": xǁEGARCHǁ__init____mutmut_3,
        "xǁEGARCHǁ__init____mutmut_4": xǁEGARCHǁ__init____mutmut_4,
        "xǁEGARCHǁ__init____mutmut_5": xǁEGARCHǁ__init____mutmut_5,
        "xǁEGARCHǁ__init____mutmut_6": xǁEGARCHǁ__init____mutmut_6,
        "xǁEGARCHǁ__init____mutmut_7": xǁEGARCHǁ__init____mutmut_7,
        "xǁEGARCHǁ__init____mutmut_8": xǁEGARCHǁ__init____mutmut_8,
        "xǁEGARCHǁ__init____mutmut_9": xǁEGARCHǁ__init____mutmut_9,
        "xǁEGARCHǁ__init____mutmut_10": xǁEGARCHǁ__init____mutmut_10,
        "xǁEGARCHǁ__init____mutmut_11": xǁEGARCHǁ__init____mutmut_11,
        "xǁEGARCHǁ__init____mutmut_12": xǁEGARCHǁ__init____mutmut_12,
        "xǁEGARCHǁ__init____mutmut_13": xǁEGARCHǁ__init____mutmut_13,
        "xǁEGARCHǁ__init____mutmut_14": xǁEGARCHǁ__init____mutmut_14,
    }
    xǁEGARCHǁ__init____mutmut_orig.__name__ = "xǁEGARCHǁ__init__"

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEGARCHǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁEGARCHǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEGARCHǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = None
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = None
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(None)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = None

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(None)

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(None, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, None))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(
            max(
                backcast,
            )
        )

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1.000000000001))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(None):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = None
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(None):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = None
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 + j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t + 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 2 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] = betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] -= betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] / (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag > 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 1 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(None):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = None
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 + i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t + 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 2 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag > 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 1:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = None
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(None)
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(None))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = None
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] * max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_58(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(None, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_59(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, None)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_60(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_61(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(
                        prev_sigma,
                    )
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_62(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1.000001)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_63(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = None
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_64(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 1.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_65(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] = alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_66(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] -= alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_67(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] / (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_68(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) + np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_69(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(None) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_70(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(None))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_71(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 * np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_72(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(3.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_73(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] = gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_74(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] -= gammas[i] * z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_75(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] / z

        sigma2 = np.exp(log_sigma2)
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_76(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = None
        return sigma2

    def xǁEGARCHǁ_variance_recursion__mutmut_77(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via EGARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals (eps_t = r_t - mu).
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

        nobs = len(resids)
        log_sigma2 = np.empty(nobs)
        log_backcast = np.log(max(backcast, 1e-12))

        for t in range(nobs):
            log_sigma2[t] = omega
            for j in range(self.p):
                lag = t - 1 - j
                log_sigma2[t] += betas[j] * (log_sigma2[lag] if lag >= 0 else log_backcast)
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    prev_sigma = np.sqrt(np.exp(log_sigma2[lag]))
                    z = resids[lag] / max(prev_sigma, 1e-6)
                else:
                    z = 0.0
                log_sigma2[t] += alphas[i] * (np.abs(z) - np.sqrt(2.0 / np.pi))
                log_sigma2[t] += gammas[i] * z

        sigma2 = np.exp(None)
        return sigma2

    xǁEGARCHǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEGARCHǁ_variance_recursion__mutmut_1": xǁEGARCHǁ_variance_recursion__mutmut_1,
        "xǁEGARCHǁ_variance_recursion__mutmut_2": xǁEGARCHǁ_variance_recursion__mutmut_2,
        "xǁEGARCHǁ_variance_recursion__mutmut_3": xǁEGARCHǁ_variance_recursion__mutmut_3,
        "xǁEGARCHǁ_variance_recursion__mutmut_4": xǁEGARCHǁ_variance_recursion__mutmut_4,
        "xǁEGARCHǁ_variance_recursion__mutmut_5": xǁEGARCHǁ_variance_recursion__mutmut_5,
        "xǁEGARCHǁ_variance_recursion__mutmut_6": xǁEGARCHǁ_variance_recursion__mutmut_6,
        "xǁEGARCHǁ_variance_recursion__mutmut_7": xǁEGARCHǁ_variance_recursion__mutmut_7,
        "xǁEGARCHǁ_variance_recursion__mutmut_8": xǁEGARCHǁ_variance_recursion__mutmut_8,
        "xǁEGARCHǁ_variance_recursion__mutmut_9": xǁEGARCHǁ_variance_recursion__mutmut_9,
        "xǁEGARCHǁ_variance_recursion__mutmut_10": xǁEGARCHǁ_variance_recursion__mutmut_10,
        "xǁEGARCHǁ_variance_recursion__mutmut_11": xǁEGARCHǁ_variance_recursion__mutmut_11,
        "xǁEGARCHǁ_variance_recursion__mutmut_12": xǁEGARCHǁ_variance_recursion__mutmut_12,
        "xǁEGARCHǁ_variance_recursion__mutmut_13": xǁEGARCHǁ_variance_recursion__mutmut_13,
        "xǁEGARCHǁ_variance_recursion__mutmut_14": xǁEGARCHǁ_variance_recursion__mutmut_14,
        "xǁEGARCHǁ_variance_recursion__mutmut_15": xǁEGARCHǁ_variance_recursion__mutmut_15,
        "xǁEGARCHǁ_variance_recursion__mutmut_16": xǁEGARCHǁ_variance_recursion__mutmut_16,
        "xǁEGARCHǁ_variance_recursion__mutmut_17": xǁEGARCHǁ_variance_recursion__mutmut_17,
        "xǁEGARCHǁ_variance_recursion__mutmut_18": xǁEGARCHǁ_variance_recursion__mutmut_18,
        "xǁEGARCHǁ_variance_recursion__mutmut_19": xǁEGARCHǁ_variance_recursion__mutmut_19,
        "xǁEGARCHǁ_variance_recursion__mutmut_20": xǁEGARCHǁ_variance_recursion__mutmut_20,
        "xǁEGARCHǁ_variance_recursion__mutmut_21": xǁEGARCHǁ_variance_recursion__mutmut_21,
        "xǁEGARCHǁ_variance_recursion__mutmut_22": xǁEGARCHǁ_variance_recursion__mutmut_22,
        "xǁEGARCHǁ_variance_recursion__mutmut_23": xǁEGARCHǁ_variance_recursion__mutmut_23,
        "xǁEGARCHǁ_variance_recursion__mutmut_24": xǁEGARCHǁ_variance_recursion__mutmut_24,
        "xǁEGARCHǁ_variance_recursion__mutmut_25": xǁEGARCHǁ_variance_recursion__mutmut_25,
        "xǁEGARCHǁ_variance_recursion__mutmut_26": xǁEGARCHǁ_variance_recursion__mutmut_26,
        "xǁEGARCHǁ_variance_recursion__mutmut_27": xǁEGARCHǁ_variance_recursion__mutmut_27,
        "xǁEGARCHǁ_variance_recursion__mutmut_28": xǁEGARCHǁ_variance_recursion__mutmut_28,
        "xǁEGARCHǁ_variance_recursion__mutmut_29": xǁEGARCHǁ_variance_recursion__mutmut_29,
        "xǁEGARCHǁ_variance_recursion__mutmut_30": xǁEGARCHǁ_variance_recursion__mutmut_30,
        "xǁEGARCHǁ_variance_recursion__mutmut_31": xǁEGARCHǁ_variance_recursion__mutmut_31,
        "xǁEGARCHǁ_variance_recursion__mutmut_32": xǁEGARCHǁ_variance_recursion__mutmut_32,
        "xǁEGARCHǁ_variance_recursion__mutmut_33": xǁEGARCHǁ_variance_recursion__mutmut_33,
        "xǁEGARCHǁ_variance_recursion__mutmut_34": xǁEGARCHǁ_variance_recursion__mutmut_34,
        "xǁEGARCHǁ_variance_recursion__mutmut_35": xǁEGARCHǁ_variance_recursion__mutmut_35,
        "xǁEGARCHǁ_variance_recursion__mutmut_36": xǁEGARCHǁ_variance_recursion__mutmut_36,
        "xǁEGARCHǁ_variance_recursion__mutmut_37": xǁEGARCHǁ_variance_recursion__mutmut_37,
        "xǁEGARCHǁ_variance_recursion__mutmut_38": xǁEGARCHǁ_variance_recursion__mutmut_38,
        "xǁEGARCHǁ_variance_recursion__mutmut_39": xǁEGARCHǁ_variance_recursion__mutmut_39,
        "xǁEGARCHǁ_variance_recursion__mutmut_40": xǁEGARCHǁ_variance_recursion__mutmut_40,
        "xǁEGARCHǁ_variance_recursion__mutmut_41": xǁEGARCHǁ_variance_recursion__mutmut_41,
        "xǁEGARCHǁ_variance_recursion__mutmut_42": xǁEGARCHǁ_variance_recursion__mutmut_42,
        "xǁEGARCHǁ_variance_recursion__mutmut_43": xǁEGARCHǁ_variance_recursion__mutmut_43,
        "xǁEGARCHǁ_variance_recursion__mutmut_44": xǁEGARCHǁ_variance_recursion__mutmut_44,
        "xǁEGARCHǁ_variance_recursion__mutmut_45": xǁEGARCHǁ_variance_recursion__mutmut_45,
        "xǁEGARCHǁ_variance_recursion__mutmut_46": xǁEGARCHǁ_variance_recursion__mutmut_46,
        "xǁEGARCHǁ_variance_recursion__mutmut_47": xǁEGARCHǁ_variance_recursion__mutmut_47,
        "xǁEGARCHǁ_variance_recursion__mutmut_48": xǁEGARCHǁ_variance_recursion__mutmut_48,
        "xǁEGARCHǁ_variance_recursion__mutmut_49": xǁEGARCHǁ_variance_recursion__mutmut_49,
        "xǁEGARCHǁ_variance_recursion__mutmut_50": xǁEGARCHǁ_variance_recursion__mutmut_50,
        "xǁEGARCHǁ_variance_recursion__mutmut_51": xǁEGARCHǁ_variance_recursion__mutmut_51,
        "xǁEGARCHǁ_variance_recursion__mutmut_52": xǁEGARCHǁ_variance_recursion__mutmut_52,
        "xǁEGARCHǁ_variance_recursion__mutmut_53": xǁEGARCHǁ_variance_recursion__mutmut_53,
        "xǁEGARCHǁ_variance_recursion__mutmut_54": xǁEGARCHǁ_variance_recursion__mutmut_54,
        "xǁEGARCHǁ_variance_recursion__mutmut_55": xǁEGARCHǁ_variance_recursion__mutmut_55,
        "xǁEGARCHǁ_variance_recursion__mutmut_56": xǁEGARCHǁ_variance_recursion__mutmut_56,
        "xǁEGARCHǁ_variance_recursion__mutmut_57": xǁEGARCHǁ_variance_recursion__mutmut_57,
        "xǁEGARCHǁ_variance_recursion__mutmut_58": xǁEGARCHǁ_variance_recursion__mutmut_58,
        "xǁEGARCHǁ_variance_recursion__mutmut_59": xǁEGARCHǁ_variance_recursion__mutmut_59,
        "xǁEGARCHǁ_variance_recursion__mutmut_60": xǁEGARCHǁ_variance_recursion__mutmut_60,
        "xǁEGARCHǁ_variance_recursion__mutmut_61": xǁEGARCHǁ_variance_recursion__mutmut_61,
        "xǁEGARCHǁ_variance_recursion__mutmut_62": xǁEGARCHǁ_variance_recursion__mutmut_62,
        "xǁEGARCHǁ_variance_recursion__mutmut_63": xǁEGARCHǁ_variance_recursion__mutmut_63,
        "xǁEGARCHǁ_variance_recursion__mutmut_64": xǁEGARCHǁ_variance_recursion__mutmut_64,
        "xǁEGARCHǁ_variance_recursion__mutmut_65": xǁEGARCHǁ_variance_recursion__mutmut_65,
        "xǁEGARCHǁ_variance_recursion__mutmut_66": xǁEGARCHǁ_variance_recursion__mutmut_66,
        "xǁEGARCHǁ_variance_recursion__mutmut_67": xǁEGARCHǁ_variance_recursion__mutmut_67,
        "xǁEGARCHǁ_variance_recursion__mutmut_68": xǁEGARCHǁ_variance_recursion__mutmut_68,
        "xǁEGARCHǁ_variance_recursion__mutmut_69": xǁEGARCHǁ_variance_recursion__mutmut_69,
        "xǁEGARCHǁ_variance_recursion__mutmut_70": xǁEGARCHǁ_variance_recursion__mutmut_70,
        "xǁEGARCHǁ_variance_recursion__mutmut_71": xǁEGARCHǁ_variance_recursion__mutmut_71,
        "xǁEGARCHǁ_variance_recursion__mutmut_72": xǁEGARCHǁ_variance_recursion__mutmut_72,
        "xǁEGARCHǁ_variance_recursion__mutmut_73": xǁEGARCHǁ_variance_recursion__mutmut_73,
        "xǁEGARCHǁ_variance_recursion__mutmut_74": xǁEGARCHǁ_variance_recursion__mutmut_74,
        "xǁEGARCHǁ_variance_recursion__mutmut_75": xǁEGARCHǁ_variance_recursion__mutmut_75,
        "xǁEGARCHǁ_variance_recursion__mutmut_76": xǁEGARCHǁ_variance_recursion__mutmut_76,
        "xǁEGARCHǁ_variance_recursion__mutmut_77": xǁEGARCHǁ_variance_recursion__mutmut_77,
    }
    xǁEGARCHǁ_variance_recursion__mutmut_orig.__name__ = "xǁEGARCHǁ_variance_recursion"

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEGARCHǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁEGARCHǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEGARCHǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = None
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[1]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = None
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[2]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = None
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 - self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[2 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = None

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 - 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[2 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 / self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 3 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = None
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(None)
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(None, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, None))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(
            max(
                sigma2_prev,
            )
        )
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_19(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1.000000000001))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = None
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_21(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps * max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_22(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(None, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_23(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, None)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_24(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_25(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(
            sigma_prev,
        )
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_26(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1.000001)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_27(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = None
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_28(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            - beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_29(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            - gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_30(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            - alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_31(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha / (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_32(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) + np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_33(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(None) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_34(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(None))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_35(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 * np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_36(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(3.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_37(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma / z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_38(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta / np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_39(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi)) + gamma * z + beta * np.log(None)
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_40(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(None, 1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_41(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, None))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_42(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(1e-12))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_43(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta
            * np.log(
                max(
                    sigma2_prev,
                )
            )
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_44(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1.000000000001))
        )
        return float(np.exp(log_sigma2))

    def xǁEGARCHǁ_one_step_variance__mutmut_45(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(None)

    def xǁEGARCHǁ_one_step_variance__mutmut_46(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock value eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance sigma^2_{t-1}.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t given eps_{t-1} and sigma^2_{t-1}.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        sigma_prev = np.sqrt(max(sigma2_prev, 1e-12))
        z = eps / max(sigma_prev, 1e-6)
        log_sigma2 = (
            omega
            + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi))
            + gamma * z
            + beta * np.log(max(sigma2_prev, 1e-12))
        )
        return float(np.exp(None))

    xǁEGARCHǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEGARCHǁ_one_step_variance__mutmut_1": xǁEGARCHǁ_one_step_variance__mutmut_1,
        "xǁEGARCHǁ_one_step_variance__mutmut_2": xǁEGARCHǁ_one_step_variance__mutmut_2,
        "xǁEGARCHǁ_one_step_variance__mutmut_3": xǁEGARCHǁ_one_step_variance__mutmut_3,
        "xǁEGARCHǁ_one_step_variance__mutmut_4": xǁEGARCHǁ_one_step_variance__mutmut_4,
        "xǁEGARCHǁ_one_step_variance__mutmut_5": xǁEGARCHǁ_one_step_variance__mutmut_5,
        "xǁEGARCHǁ_one_step_variance__mutmut_6": xǁEGARCHǁ_one_step_variance__mutmut_6,
        "xǁEGARCHǁ_one_step_variance__mutmut_7": xǁEGARCHǁ_one_step_variance__mutmut_7,
        "xǁEGARCHǁ_one_step_variance__mutmut_8": xǁEGARCHǁ_one_step_variance__mutmut_8,
        "xǁEGARCHǁ_one_step_variance__mutmut_9": xǁEGARCHǁ_one_step_variance__mutmut_9,
        "xǁEGARCHǁ_one_step_variance__mutmut_10": xǁEGARCHǁ_one_step_variance__mutmut_10,
        "xǁEGARCHǁ_one_step_variance__mutmut_11": xǁEGARCHǁ_one_step_variance__mutmut_11,
        "xǁEGARCHǁ_one_step_variance__mutmut_12": xǁEGARCHǁ_one_step_variance__mutmut_12,
        "xǁEGARCHǁ_one_step_variance__mutmut_13": xǁEGARCHǁ_one_step_variance__mutmut_13,
        "xǁEGARCHǁ_one_step_variance__mutmut_14": xǁEGARCHǁ_one_step_variance__mutmut_14,
        "xǁEGARCHǁ_one_step_variance__mutmut_15": xǁEGARCHǁ_one_step_variance__mutmut_15,
        "xǁEGARCHǁ_one_step_variance__mutmut_16": xǁEGARCHǁ_one_step_variance__mutmut_16,
        "xǁEGARCHǁ_one_step_variance__mutmut_17": xǁEGARCHǁ_one_step_variance__mutmut_17,
        "xǁEGARCHǁ_one_step_variance__mutmut_18": xǁEGARCHǁ_one_step_variance__mutmut_18,
        "xǁEGARCHǁ_one_step_variance__mutmut_19": xǁEGARCHǁ_one_step_variance__mutmut_19,
        "xǁEGARCHǁ_one_step_variance__mutmut_20": xǁEGARCHǁ_one_step_variance__mutmut_20,
        "xǁEGARCHǁ_one_step_variance__mutmut_21": xǁEGARCHǁ_one_step_variance__mutmut_21,
        "xǁEGARCHǁ_one_step_variance__mutmut_22": xǁEGARCHǁ_one_step_variance__mutmut_22,
        "xǁEGARCHǁ_one_step_variance__mutmut_23": xǁEGARCHǁ_one_step_variance__mutmut_23,
        "xǁEGARCHǁ_one_step_variance__mutmut_24": xǁEGARCHǁ_one_step_variance__mutmut_24,
        "xǁEGARCHǁ_one_step_variance__mutmut_25": xǁEGARCHǁ_one_step_variance__mutmut_25,
        "xǁEGARCHǁ_one_step_variance__mutmut_26": xǁEGARCHǁ_one_step_variance__mutmut_26,
        "xǁEGARCHǁ_one_step_variance__mutmut_27": xǁEGARCHǁ_one_step_variance__mutmut_27,
        "xǁEGARCHǁ_one_step_variance__mutmut_28": xǁEGARCHǁ_one_step_variance__mutmut_28,
        "xǁEGARCHǁ_one_step_variance__mutmut_29": xǁEGARCHǁ_one_step_variance__mutmut_29,
        "xǁEGARCHǁ_one_step_variance__mutmut_30": xǁEGARCHǁ_one_step_variance__mutmut_30,
        "xǁEGARCHǁ_one_step_variance__mutmut_31": xǁEGARCHǁ_one_step_variance__mutmut_31,
        "xǁEGARCHǁ_one_step_variance__mutmut_32": xǁEGARCHǁ_one_step_variance__mutmut_32,
        "xǁEGARCHǁ_one_step_variance__mutmut_33": xǁEGARCHǁ_one_step_variance__mutmut_33,
        "xǁEGARCHǁ_one_step_variance__mutmut_34": xǁEGARCHǁ_one_step_variance__mutmut_34,
        "xǁEGARCHǁ_one_step_variance__mutmut_35": xǁEGARCHǁ_one_step_variance__mutmut_35,
        "xǁEGARCHǁ_one_step_variance__mutmut_36": xǁEGARCHǁ_one_step_variance__mutmut_36,
        "xǁEGARCHǁ_one_step_variance__mutmut_37": xǁEGARCHǁ_one_step_variance__mutmut_37,
        "xǁEGARCHǁ_one_step_variance__mutmut_38": xǁEGARCHǁ_one_step_variance__mutmut_38,
        "xǁEGARCHǁ_one_step_variance__mutmut_39": xǁEGARCHǁ_one_step_variance__mutmut_39,
        "xǁEGARCHǁ_one_step_variance__mutmut_40": xǁEGARCHǁ_one_step_variance__mutmut_40,
        "xǁEGARCHǁ_one_step_variance__mutmut_41": xǁEGARCHǁ_one_step_variance__mutmut_41,
        "xǁEGARCHǁ_one_step_variance__mutmut_42": xǁEGARCHǁ_one_step_variance__mutmut_42,
        "xǁEGARCHǁ_one_step_variance__mutmut_43": xǁEGARCHǁ_one_step_variance__mutmut_43,
        "xǁEGARCHǁ_one_step_variance__mutmut_44": xǁEGARCHǁ_one_step_variance__mutmut_44,
        "xǁEGARCHǁ_one_step_variance__mutmut_45": xǁEGARCHǁ_one_step_variance__mutmut_45,
        "xǁEGARCHǁ_one_step_variance__mutmut_46": xǁEGARCHǁ_one_step_variance__mutmut_46,
    }
    xǁEGARCHǁ_one_step_variance__mutmut_orig.__name__ = "xǁEGARCHǁ_one_step_variance"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for optimization."""
        omega = np.log(np.var(self.endog)) * 0.05
        alphas = np.full(self.q, 0.1)
        gammas = np.full(self.q, -0.05)
        betas = np.full(self.p, 0.95)
        return np.concatenate([[omega], alphas, gammas, betas])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["omega"]
        names += [f"alpha[{i + 1}]" for i in range(self.q)]
        names += [f"gamma[{i + 1}]" for i in range(self.q)]
        names += [f"beta[{i + 1}]" for i in range(self.p)]
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEGARCHǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁEGARCHǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEGARCHǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = None
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(None):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = None
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 2 * self.q - j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 - 2 * self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 2 + 2 * self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 2 / self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 3 * self.q + j
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = None
        return constrained

    def xǁEGARCHǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        EGARCH has no positivity constraints on omega, alpha, gamma.
        Only |beta| < 1 for stationarity.
        """
        constrained = unconstrained.copy()
        # beta: use tanh to ensure |beta| < 1
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.tanh(None)
        return constrained

    xǁEGARCHǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEGARCHǁtransform_params__mutmut_1": xǁEGARCHǁtransform_params__mutmut_1,
        "xǁEGARCHǁtransform_params__mutmut_2": xǁEGARCHǁtransform_params__mutmut_2,
        "xǁEGARCHǁtransform_params__mutmut_3": xǁEGARCHǁtransform_params__mutmut_3,
        "xǁEGARCHǁtransform_params__mutmut_4": xǁEGARCHǁtransform_params__mutmut_4,
        "xǁEGARCHǁtransform_params__mutmut_5": xǁEGARCHǁtransform_params__mutmut_5,
        "xǁEGARCHǁtransform_params__mutmut_6": xǁEGARCHǁtransform_params__mutmut_6,
        "xǁEGARCHǁtransform_params__mutmut_7": xǁEGARCHǁtransform_params__mutmut_7,
        "xǁEGARCHǁtransform_params__mutmut_8": xǁEGARCHǁtransform_params__mutmut_8,
        "xǁEGARCHǁtransform_params__mutmut_9": xǁEGARCHǁtransform_params__mutmut_9,
        "xǁEGARCHǁtransform_params__mutmut_10": xǁEGARCHǁtransform_params__mutmut_10,
    }
    xǁEGARCHǁtransform_params__mutmut_orig.__name__ = "xǁEGARCHǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEGARCHǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁEGARCHǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEGARCHǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = None
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(None):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = None
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q - j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 - 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 2 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 / self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 3 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = None
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(None)
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(None, -0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], None, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, None))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(-0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(
                np.clip(
                    constrained[idx],
                    -0.9999,
                )
            )
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], +0.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -1.9999, 0.9999))
        return unconstrained

    def xǁEGARCHǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.9999, 1.9999))
        return unconstrained

    xǁEGARCHǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEGARCHǁuntransform_params__mutmut_1": xǁEGARCHǁuntransform_params__mutmut_1,
        "xǁEGARCHǁuntransform_params__mutmut_2": xǁEGARCHǁuntransform_params__mutmut_2,
        "xǁEGARCHǁuntransform_params__mutmut_3": xǁEGARCHǁuntransform_params__mutmut_3,
        "xǁEGARCHǁuntransform_params__mutmut_4": xǁEGARCHǁuntransform_params__mutmut_4,
        "xǁEGARCHǁuntransform_params__mutmut_5": xǁEGARCHǁuntransform_params__mutmut_5,
        "xǁEGARCHǁuntransform_params__mutmut_6": xǁEGARCHǁuntransform_params__mutmut_6,
        "xǁEGARCHǁuntransform_params__mutmut_7": xǁEGARCHǁuntransform_params__mutmut_7,
        "xǁEGARCHǁuntransform_params__mutmut_8": xǁEGARCHǁuntransform_params__mutmut_8,
        "xǁEGARCHǁuntransform_params__mutmut_9": xǁEGARCHǁuntransform_params__mutmut_9,
        "xǁEGARCHǁuntransform_params__mutmut_10": xǁEGARCHǁuntransform_params__mutmut_10,
        "xǁEGARCHǁuntransform_params__mutmut_11": xǁEGARCHǁuntransform_params__mutmut_11,
        "xǁEGARCHǁuntransform_params__mutmut_12": xǁEGARCHǁuntransform_params__mutmut_12,
        "xǁEGARCHǁuntransform_params__mutmut_13": xǁEGARCHǁuntransform_params__mutmut_13,
        "xǁEGARCHǁuntransform_params__mutmut_14": xǁEGARCHǁuntransform_params__mutmut_14,
        "xǁEGARCHǁuntransform_params__mutmut_15": xǁEGARCHǁuntransform_params__mutmut_15,
        "xǁEGARCHǁuntransform_params__mutmut_16": xǁEGARCHǁuntransform_params__mutmut_16,
        "xǁEGARCHǁuntransform_params__mutmut_17": xǁEGARCHǁuntransform_params__mutmut_17,
        "xǁEGARCHǁuntransform_params__mutmut_18": xǁEGARCHǁuntransform_params__mutmut_18,
        "xǁEGARCHǁuntransform_params__mutmut_19": xǁEGARCHǁuntransform_params__mutmut_19,
    }
    xǁEGARCHǁuntransform_params__mutmut_orig.__name__ = "xǁEGARCHǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEGARCHǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁEGARCHǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEGARCHǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = None
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append(None)
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((+np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(None):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append(None)
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((+np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(None):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append(None)
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((+np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_10(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(None):
            bnds.append((-0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_11(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append(None)
        return bnds

    def xǁEGARCHǁbounds__mutmut_12(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((+0.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_13(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-1.9999, 0.9999))
        return bnds

    def xǁEGARCHǁbounds__mutmut_14(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer."""
        bnds: list[tuple[float, float]] = []
        # omega: unconstrained
        bnds.append((-np.inf, np.inf))
        # alphas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # gammas: unconstrained
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas: (-1, 1)
        for _ in range(self.p):
            bnds.append((-0.9999, 1.9999))
        return bnds

    xǁEGARCHǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEGARCHǁbounds__mutmut_1": xǁEGARCHǁbounds__mutmut_1,
        "xǁEGARCHǁbounds__mutmut_2": xǁEGARCHǁbounds__mutmut_2,
        "xǁEGARCHǁbounds__mutmut_3": xǁEGARCHǁbounds__mutmut_3,
        "xǁEGARCHǁbounds__mutmut_4": xǁEGARCHǁbounds__mutmut_4,
        "xǁEGARCHǁbounds__mutmut_5": xǁEGARCHǁbounds__mutmut_5,
        "xǁEGARCHǁbounds__mutmut_6": xǁEGARCHǁbounds__mutmut_6,
        "xǁEGARCHǁbounds__mutmut_7": xǁEGARCHǁbounds__mutmut_7,
        "xǁEGARCHǁbounds__mutmut_8": xǁEGARCHǁbounds__mutmut_8,
        "xǁEGARCHǁbounds__mutmut_9": xǁEGARCHǁbounds__mutmut_9,
        "xǁEGARCHǁbounds__mutmut_10": xǁEGARCHǁbounds__mutmut_10,
        "xǁEGARCHǁbounds__mutmut_11": xǁEGARCHǁbounds__mutmut_11,
        "xǁEGARCHǁbounds__mutmut_12": xǁEGARCHǁbounds__mutmut_12,
        "xǁEGARCHǁbounds__mutmut_13": xǁEGARCHǁbounds__mutmut_13,
        "xǁEGARCHǁbounds__mutmut_14": xǁEGARCHǁbounds__mutmut_14,
    }
    xǁEGARCHǁbounds__mutmut_orig.__name__ = "xǁEGARCHǁbounds"

    @property
    def num_params(self) -> int:
        """Number of model parameters."""
        return 1 + 2 * self.q + self.p
