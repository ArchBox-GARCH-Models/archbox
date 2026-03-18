"""GJR-GARCH model (Glosten, Jagannathan & Runkle, 1993).

sigma^2_t = omega + (alpha + gamma * I_{t-1}) * eps^2_{t-1} + beta * sigma^2_{t-1}

I_{t-1} = 1 se eps_{t-1} < 0, 0 caso contrario.
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


class GJRGARCH(VolatilityModel):
    """GJR-GARCH (Threshold GARCH) model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of GARCH lags (beta). Default 1.
    q : int
        Number of ARCH lags (alpha, gamma). Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "GJR-GARCH"

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
            object.__getattribute__(self, "xǁGJRGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁGJRGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGJRGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        p: int = 2,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        p: int = 1,
        q: int = 2,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = None
        self.q = q
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = None
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(None, mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=None, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, mean=mean, dist=None)

    def xǁGJRGARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(mean=mean, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_13(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(endog, dist=dist)

    def xǁGJRGARCHǁ__init____mutmut_14(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GJR-GARCH model with lag orders and options."""
        self.p = p
        self.q = q
        super().__init__(
            endog,
            mean=mean,
        )

    xǁGJRGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGJRGARCHǁ__init____mutmut_1": xǁGJRGARCHǁ__init____mutmut_1,
        "xǁGJRGARCHǁ__init____mutmut_2": xǁGJRGARCHǁ__init____mutmut_2,
        "xǁGJRGARCHǁ__init____mutmut_3": xǁGJRGARCHǁ__init____mutmut_3,
        "xǁGJRGARCHǁ__init____mutmut_4": xǁGJRGARCHǁ__init____mutmut_4,
        "xǁGJRGARCHǁ__init____mutmut_5": xǁGJRGARCHǁ__init____mutmut_5,
        "xǁGJRGARCHǁ__init____mutmut_6": xǁGJRGARCHǁ__init____mutmut_6,
        "xǁGJRGARCHǁ__init____mutmut_7": xǁGJRGARCHǁ__init____mutmut_7,
        "xǁGJRGARCHǁ__init____mutmut_8": xǁGJRGARCHǁ__init____mutmut_8,
        "xǁGJRGARCHǁ__init____mutmut_9": xǁGJRGARCHǁ__init____mutmut_9,
        "xǁGJRGARCHǁ__init____mutmut_10": xǁGJRGARCHǁ__init____mutmut_10,
        "xǁGJRGARCHǁ__init____mutmut_11": xǁGJRGARCHǁ__init____mutmut_11,
        "xǁGJRGARCHǁ__init____mutmut_12": xǁGJRGARCHǁ__init____mutmut_12,
        "xǁGJRGARCHǁ__init____mutmut_13": xǁGJRGARCHǁ__init____mutmut_13,
        "xǁGJRGARCHǁ__init____mutmut_14": xǁGJRGARCHǁ__init____mutmut_14,
    }
    xǁGJRGARCHǁ__init____mutmut_orig.__name__ = "xǁGJRGARCHǁ__init__"

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGJRGARCHǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁGJRGARCHǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGJRGARCHǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = None
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[2 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 - self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 2 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = None
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 - self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[2 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 - 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 2 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 / self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 3 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = None

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 - 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[2 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 / self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 3 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q - self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 - 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 2 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 / self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 3 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = None
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = None

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(None)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(None):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = None
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(None):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = None
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 + i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t + 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 2 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag > 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 1:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = None
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] * 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 3
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = None
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 2.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] <= 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 1 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 1.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] = alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] -= alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 - gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] / e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator / e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] / indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] = (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] -= (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) / backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] - 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 / gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 1.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(None):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = None
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_58(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 + j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_59(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t + 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_60(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 2 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_61(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] = betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_62(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] -= betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_63(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] / (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_64(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag > 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_65(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 1 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_66(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = None

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_67(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(None, 1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_68(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], None)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_69(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(1e-12)

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_70(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(
                sigma2[t],
            )

        return sigma2

    def xǁGJRGARCHǁ_variance_recursion__mutmut_71(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via GJR-GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, gamma_1, ..., gamma_q, beta_1, ..., beta_p]
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
        alphas = params[1 : 1 + self.q]
        gammas = params[1 + self.q : 1 + 2 * self.q]
        betas = params[1 + 2 * self.q : 1 + 2 * self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    e2 = resids[lag] ** 2
                    indicator = 1.0 if resids[lag] < 0 else 0.0
                    sigma2[t] += alphas[i] * e2 + gammas[i] * indicator * e2
                else:
                    sigma2[t] += (alphas[i] + 0.5 * gammas[i]) * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1.000000000001)

        return sigma2

    xǁGJRGARCHǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGJRGARCHǁ_variance_recursion__mutmut_1": xǁGJRGARCHǁ_variance_recursion__mutmut_1,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_2": xǁGJRGARCHǁ_variance_recursion__mutmut_2,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_3": xǁGJRGARCHǁ_variance_recursion__mutmut_3,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_4": xǁGJRGARCHǁ_variance_recursion__mutmut_4,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_5": xǁGJRGARCHǁ_variance_recursion__mutmut_5,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_6": xǁGJRGARCHǁ_variance_recursion__mutmut_6,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_7": xǁGJRGARCHǁ_variance_recursion__mutmut_7,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_8": xǁGJRGARCHǁ_variance_recursion__mutmut_8,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_9": xǁGJRGARCHǁ_variance_recursion__mutmut_9,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_10": xǁGJRGARCHǁ_variance_recursion__mutmut_10,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_11": xǁGJRGARCHǁ_variance_recursion__mutmut_11,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_12": xǁGJRGARCHǁ_variance_recursion__mutmut_12,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_13": xǁGJRGARCHǁ_variance_recursion__mutmut_13,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_14": xǁGJRGARCHǁ_variance_recursion__mutmut_14,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_15": xǁGJRGARCHǁ_variance_recursion__mutmut_15,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_16": xǁGJRGARCHǁ_variance_recursion__mutmut_16,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_17": xǁGJRGARCHǁ_variance_recursion__mutmut_17,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_18": xǁGJRGARCHǁ_variance_recursion__mutmut_18,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_19": xǁGJRGARCHǁ_variance_recursion__mutmut_19,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_20": xǁGJRGARCHǁ_variance_recursion__mutmut_20,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_21": xǁGJRGARCHǁ_variance_recursion__mutmut_21,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_22": xǁGJRGARCHǁ_variance_recursion__mutmut_22,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_23": xǁGJRGARCHǁ_variance_recursion__mutmut_23,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_24": xǁGJRGARCHǁ_variance_recursion__mutmut_24,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_25": xǁGJRGARCHǁ_variance_recursion__mutmut_25,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_26": xǁGJRGARCHǁ_variance_recursion__mutmut_26,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_27": xǁGJRGARCHǁ_variance_recursion__mutmut_27,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_28": xǁGJRGARCHǁ_variance_recursion__mutmut_28,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_29": xǁGJRGARCHǁ_variance_recursion__mutmut_29,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_30": xǁGJRGARCHǁ_variance_recursion__mutmut_30,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_31": xǁGJRGARCHǁ_variance_recursion__mutmut_31,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_32": xǁGJRGARCHǁ_variance_recursion__mutmut_32,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_33": xǁGJRGARCHǁ_variance_recursion__mutmut_33,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_34": xǁGJRGARCHǁ_variance_recursion__mutmut_34,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_35": xǁGJRGARCHǁ_variance_recursion__mutmut_35,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_36": xǁGJRGARCHǁ_variance_recursion__mutmut_36,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_37": xǁGJRGARCHǁ_variance_recursion__mutmut_37,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_38": xǁGJRGARCHǁ_variance_recursion__mutmut_38,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_39": xǁGJRGARCHǁ_variance_recursion__mutmut_39,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_40": xǁGJRGARCHǁ_variance_recursion__mutmut_40,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_41": xǁGJRGARCHǁ_variance_recursion__mutmut_41,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_42": xǁGJRGARCHǁ_variance_recursion__mutmut_42,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_43": xǁGJRGARCHǁ_variance_recursion__mutmut_43,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_44": xǁGJRGARCHǁ_variance_recursion__mutmut_44,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_45": xǁGJRGARCHǁ_variance_recursion__mutmut_45,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_46": xǁGJRGARCHǁ_variance_recursion__mutmut_46,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_47": xǁGJRGARCHǁ_variance_recursion__mutmut_47,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_48": xǁGJRGARCHǁ_variance_recursion__mutmut_48,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_49": xǁGJRGARCHǁ_variance_recursion__mutmut_49,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_50": xǁGJRGARCHǁ_variance_recursion__mutmut_50,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_51": xǁGJRGARCHǁ_variance_recursion__mutmut_51,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_52": xǁGJRGARCHǁ_variance_recursion__mutmut_52,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_53": xǁGJRGARCHǁ_variance_recursion__mutmut_53,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_54": xǁGJRGARCHǁ_variance_recursion__mutmut_54,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_55": xǁGJRGARCHǁ_variance_recursion__mutmut_55,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_56": xǁGJRGARCHǁ_variance_recursion__mutmut_56,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_57": xǁGJRGARCHǁ_variance_recursion__mutmut_57,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_58": xǁGJRGARCHǁ_variance_recursion__mutmut_58,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_59": xǁGJRGARCHǁ_variance_recursion__mutmut_59,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_60": xǁGJRGARCHǁ_variance_recursion__mutmut_60,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_61": xǁGJRGARCHǁ_variance_recursion__mutmut_61,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_62": xǁGJRGARCHǁ_variance_recursion__mutmut_62,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_63": xǁGJRGARCHǁ_variance_recursion__mutmut_63,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_64": xǁGJRGARCHǁ_variance_recursion__mutmut_64,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_65": xǁGJRGARCHǁ_variance_recursion__mutmut_65,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_66": xǁGJRGARCHǁ_variance_recursion__mutmut_66,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_67": xǁGJRGARCHǁ_variance_recursion__mutmut_67,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_68": xǁGJRGARCHǁ_variance_recursion__mutmut_68,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_69": xǁGJRGARCHǁ_variance_recursion__mutmut_69,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_70": xǁGJRGARCHǁ_variance_recursion__mutmut_70,
        "xǁGJRGARCHǁ_variance_recursion__mutmut_71": xǁGJRGARCHǁ_variance_recursion__mutmut_71,
    }
    xǁGJRGARCHǁ_variance_recursion__mutmut_orig.__name__ = "xǁGJRGARCHǁ_variance_recursion"

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGJRGARCHǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁGJRGARCHǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGJRGARCHǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = None
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[1]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = None
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[2]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = None
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 - self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[2 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = None

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 - 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[2 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 / self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 3 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = None
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 2.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps <= 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 1 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 1.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = None
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_19(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 - beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega - (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_21(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) / eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_22(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha - gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_23(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma / indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_24(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps * 2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_25(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**3 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_26(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta / sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_27(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(None)

    def xǁGJRGARCHǁ_one_step_variance__mutmut_28(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(None, 1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_29(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, None))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_30(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(1e-12))

    def xǁGJRGARCHǁ_one_step_variance__mutmut_31(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(
            max(
                sigma2,
            )
        )

    def xǁGJRGARCHǁ_one_step_variance__mutmut_32(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve.

        Parameters
        ----------
        eps : float
            Previous shock eps_{t-1}.
        sigma2_prev : float
            Previous conditional variance.
        params : ndarray
            Model parameters.

        Returns
        -------
        float
            sigma^2_t.
        """
        omega = params[0]
        alpha = params[1]
        gamma = params[1 + self.q]
        beta = params[1 + 2 * self.q]

        indicator = 1.0 if eps < 0 else 0.0
        sigma2 = omega + (alpha + gamma * indicator) * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1.000000000001))

    xǁGJRGARCHǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGJRGARCHǁ_one_step_variance__mutmut_1": xǁGJRGARCHǁ_one_step_variance__mutmut_1,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_2": xǁGJRGARCHǁ_one_step_variance__mutmut_2,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_3": xǁGJRGARCHǁ_one_step_variance__mutmut_3,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_4": xǁGJRGARCHǁ_one_step_variance__mutmut_4,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_5": xǁGJRGARCHǁ_one_step_variance__mutmut_5,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_6": xǁGJRGARCHǁ_one_step_variance__mutmut_6,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_7": xǁGJRGARCHǁ_one_step_variance__mutmut_7,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_8": xǁGJRGARCHǁ_one_step_variance__mutmut_8,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_9": xǁGJRGARCHǁ_one_step_variance__mutmut_9,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_10": xǁGJRGARCHǁ_one_step_variance__mutmut_10,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_11": xǁGJRGARCHǁ_one_step_variance__mutmut_11,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_12": xǁGJRGARCHǁ_one_step_variance__mutmut_12,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_13": xǁGJRGARCHǁ_one_step_variance__mutmut_13,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_14": xǁGJRGARCHǁ_one_step_variance__mutmut_14,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_15": xǁGJRGARCHǁ_one_step_variance__mutmut_15,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_16": xǁGJRGARCHǁ_one_step_variance__mutmut_16,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_17": xǁGJRGARCHǁ_one_step_variance__mutmut_17,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_18": xǁGJRGARCHǁ_one_step_variance__mutmut_18,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_19": xǁGJRGARCHǁ_one_step_variance__mutmut_19,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_20": xǁGJRGARCHǁ_one_step_variance__mutmut_20,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_21": xǁGJRGARCHǁ_one_step_variance__mutmut_21,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_22": xǁGJRGARCHǁ_one_step_variance__mutmut_22,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_23": xǁGJRGARCHǁ_one_step_variance__mutmut_23,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_24": xǁGJRGARCHǁ_one_step_variance__mutmut_24,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_25": xǁGJRGARCHǁ_one_step_variance__mutmut_25,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_26": xǁGJRGARCHǁ_one_step_variance__mutmut_26,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_27": xǁGJRGARCHǁ_one_step_variance__mutmut_27,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_28": xǁGJRGARCHǁ_one_step_variance__mutmut_28,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_29": xǁGJRGARCHǁ_one_step_variance__mutmut_29,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_30": xǁGJRGARCHǁ_one_step_variance__mutmut_30,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_31": xǁGJRGARCHǁ_one_step_variance__mutmut_31,
        "xǁGJRGARCHǁ_one_step_variance__mutmut_32": xǁGJRGARCHǁ_one_step_variance__mutmut_32,
    }
    xǁGJRGARCHǁ_one_step_variance__mutmut_orig.__name__ = "xǁGJRGARCHǁ_one_step_variance"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        var = np.var(self.endog)
        omega = var * 0.01
        alphas = np.full(self.q, 0.05)
        gammas = np.full(self.q, 0.04)
        betas = np.full(self.p, 0.90)
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
            object.__getattribute__(self, "xǁGJRGARCHǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGJRGARCHǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGJRGARCHǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = None
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = None
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[1] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(None)
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[1])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(None):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = None
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 - i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[2 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(None)
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 - i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[2 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(None):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = None
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q - j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 - 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_17(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 2 + 2 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_18(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 / self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_19(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 3 * self.q + j
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_20(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = None
        return constrained

    def xǁGJRGARCHǁtransform_params__mutmut_21(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained.

        omega > 0, alpha >= 0, alpha+gamma >= 0, beta >= 0
        """
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(unconstrained[1 + i])
        # gamma: unconstrained (bounds handle alpha+gamma>=0)
        # beta >= 0
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            constrained[idx] = np.exp(None)
        return constrained

    xǁGJRGARCHǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGJRGARCHǁtransform_params__mutmut_1": xǁGJRGARCHǁtransform_params__mutmut_1,
        "xǁGJRGARCHǁtransform_params__mutmut_2": xǁGJRGARCHǁtransform_params__mutmut_2,
        "xǁGJRGARCHǁtransform_params__mutmut_3": xǁGJRGARCHǁtransform_params__mutmut_3,
        "xǁGJRGARCHǁtransform_params__mutmut_4": xǁGJRGARCHǁtransform_params__mutmut_4,
        "xǁGJRGARCHǁtransform_params__mutmut_5": xǁGJRGARCHǁtransform_params__mutmut_5,
        "xǁGJRGARCHǁtransform_params__mutmut_6": xǁGJRGARCHǁtransform_params__mutmut_6,
        "xǁGJRGARCHǁtransform_params__mutmut_7": xǁGJRGARCHǁtransform_params__mutmut_7,
        "xǁGJRGARCHǁtransform_params__mutmut_8": xǁGJRGARCHǁtransform_params__mutmut_8,
        "xǁGJRGARCHǁtransform_params__mutmut_9": xǁGJRGARCHǁtransform_params__mutmut_9,
        "xǁGJRGARCHǁtransform_params__mutmut_10": xǁGJRGARCHǁtransform_params__mutmut_10,
        "xǁGJRGARCHǁtransform_params__mutmut_11": xǁGJRGARCHǁtransform_params__mutmut_11,
        "xǁGJRGARCHǁtransform_params__mutmut_12": xǁGJRGARCHǁtransform_params__mutmut_12,
        "xǁGJRGARCHǁtransform_params__mutmut_13": xǁGJRGARCHǁtransform_params__mutmut_13,
        "xǁGJRGARCHǁtransform_params__mutmut_14": xǁGJRGARCHǁtransform_params__mutmut_14,
        "xǁGJRGARCHǁtransform_params__mutmut_15": xǁGJRGARCHǁtransform_params__mutmut_15,
        "xǁGJRGARCHǁtransform_params__mutmut_16": xǁGJRGARCHǁtransform_params__mutmut_16,
        "xǁGJRGARCHǁtransform_params__mutmut_17": xǁGJRGARCHǁtransform_params__mutmut_17,
        "xǁGJRGARCHǁtransform_params__mutmut_18": xǁGJRGARCHǁtransform_params__mutmut_18,
        "xǁGJRGARCHǁtransform_params__mutmut_19": xǁGJRGARCHǁtransform_params__mutmut_19,
        "xǁGJRGARCHǁtransform_params__mutmut_20": xǁGJRGARCHǁtransform_params__mutmut_20,
        "xǁGJRGARCHǁtransform_params__mutmut_21": xǁGJRGARCHǁtransform_params__mutmut_21,
    }
    xǁGJRGARCHǁtransform_params__mutmut_orig.__name__ = "xǁGJRGARCHǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGJRGARCHǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGJRGARCHǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGJRGARCHǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = None
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = None
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[1] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(None)
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(None, 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], None))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_8(
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
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[1], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1.000000000001))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(None):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = None
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 - i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[2 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(None)
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(None, 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], None))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_19(
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
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 - i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[2 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1.000000000001))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(None):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = None
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q - j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 - 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 2 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 / self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_29(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 3 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_30(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = None
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_31(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(None)
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_32(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(None, 1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_33(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], None))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_34(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(1e-12))
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_35(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(
                max(
                    constrained[idx],
                )
            )
        return unconstrained

    def xǁGJRGARCHǁuntransform_params__mutmut_36(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        # omega
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        # alphas
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        # gammas: stay as-is
        # betas
        for j in range(self.p):
            idx = 1 + 2 * self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1.000000000001))
        return unconstrained

    xǁGJRGARCHǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGJRGARCHǁuntransform_params__mutmut_1": xǁGJRGARCHǁuntransform_params__mutmut_1,
        "xǁGJRGARCHǁuntransform_params__mutmut_2": xǁGJRGARCHǁuntransform_params__mutmut_2,
        "xǁGJRGARCHǁuntransform_params__mutmut_3": xǁGJRGARCHǁuntransform_params__mutmut_3,
        "xǁGJRGARCHǁuntransform_params__mutmut_4": xǁGJRGARCHǁuntransform_params__mutmut_4,
        "xǁGJRGARCHǁuntransform_params__mutmut_5": xǁGJRGARCHǁuntransform_params__mutmut_5,
        "xǁGJRGARCHǁuntransform_params__mutmut_6": xǁGJRGARCHǁuntransform_params__mutmut_6,
        "xǁGJRGARCHǁuntransform_params__mutmut_7": xǁGJRGARCHǁuntransform_params__mutmut_7,
        "xǁGJRGARCHǁuntransform_params__mutmut_8": xǁGJRGARCHǁuntransform_params__mutmut_8,
        "xǁGJRGARCHǁuntransform_params__mutmut_9": xǁGJRGARCHǁuntransform_params__mutmut_9,
        "xǁGJRGARCHǁuntransform_params__mutmut_10": xǁGJRGARCHǁuntransform_params__mutmut_10,
        "xǁGJRGARCHǁuntransform_params__mutmut_11": xǁGJRGARCHǁuntransform_params__mutmut_11,
        "xǁGJRGARCHǁuntransform_params__mutmut_12": xǁGJRGARCHǁuntransform_params__mutmut_12,
        "xǁGJRGARCHǁuntransform_params__mutmut_13": xǁGJRGARCHǁuntransform_params__mutmut_13,
        "xǁGJRGARCHǁuntransform_params__mutmut_14": xǁGJRGARCHǁuntransform_params__mutmut_14,
        "xǁGJRGARCHǁuntransform_params__mutmut_15": xǁGJRGARCHǁuntransform_params__mutmut_15,
        "xǁGJRGARCHǁuntransform_params__mutmut_16": xǁGJRGARCHǁuntransform_params__mutmut_16,
        "xǁGJRGARCHǁuntransform_params__mutmut_17": xǁGJRGARCHǁuntransform_params__mutmut_17,
        "xǁGJRGARCHǁuntransform_params__mutmut_18": xǁGJRGARCHǁuntransform_params__mutmut_18,
        "xǁGJRGARCHǁuntransform_params__mutmut_19": xǁGJRGARCHǁuntransform_params__mutmut_19,
        "xǁGJRGARCHǁuntransform_params__mutmut_20": xǁGJRGARCHǁuntransform_params__mutmut_20,
        "xǁGJRGARCHǁuntransform_params__mutmut_21": xǁGJRGARCHǁuntransform_params__mutmut_21,
        "xǁGJRGARCHǁuntransform_params__mutmut_22": xǁGJRGARCHǁuntransform_params__mutmut_22,
        "xǁGJRGARCHǁuntransform_params__mutmut_23": xǁGJRGARCHǁuntransform_params__mutmut_23,
        "xǁGJRGARCHǁuntransform_params__mutmut_24": xǁGJRGARCHǁuntransform_params__mutmut_24,
        "xǁGJRGARCHǁuntransform_params__mutmut_25": xǁGJRGARCHǁuntransform_params__mutmut_25,
        "xǁGJRGARCHǁuntransform_params__mutmut_26": xǁGJRGARCHǁuntransform_params__mutmut_26,
        "xǁGJRGARCHǁuntransform_params__mutmut_27": xǁGJRGARCHǁuntransform_params__mutmut_27,
        "xǁGJRGARCHǁuntransform_params__mutmut_28": xǁGJRGARCHǁuntransform_params__mutmut_28,
        "xǁGJRGARCHǁuntransform_params__mutmut_29": xǁGJRGARCHǁuntransform_params__mutmut_29,
        "xǁGJRGARCHǁuntransform_params__mutmut_30": xǁGJRGARCHǁuntransform_params__mutmut_30,
        "xǁGJRGARCHǁuntransform_params__mutmut_31": xǁGJRGARCHǁuntransform_params__mutmut_31,
        "xǁGJRGARCHǁuntransform_params__mutmut_32": xǁGJRGARCHǁuntransform_params__mutmut_32,
        "xǁGJRGARCHǁuntransform_params__mutmut_33": xǁGJRGARCHǁuntransform_params__mutmut_33,
        "xǁGJRGARCHǁuntransform_params__mutmut_34": xǁGJRGARCHǁuntransform_params__mutmut_34,
        "xǁGJRGARCHǁuntransform_params__mutmut_35": xǁGJRGARCHǁuntransform_params__mutmut_35,
        "xǁGJRGARCHǁuntransform_params__mutmut_36": xǁGJRGARCHǁuntransform_params__mutmut_36,
    }
    xǁGJRGARCHǁuntransform_params__mutmut_orig.__name__ = "xǁGJRGARCHǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGJRGARCHǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁGJRGARCHǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGJRGARCHǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = None
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append(None)
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1.000000000001, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(None):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append(None)
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((1.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(None):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append(None)
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((+np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_10(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(None):
            bnds.append((0.0, np.inf))
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_11(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append(None)
        return bnds

    def xǁGJRGARCHǁbounds__mutmut_12(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        # omega > 0
        bnds.append((1e-12, np.inf))
        # alphas >= 0
        for _ in range(self.q):
            bnds.append((0.0, np.inf))
        # gammas: alpha+gamma >= 0 => gamma >= -alpha (use wide bounds)
        for _ in range(self.q):
            bnds.append((-np.inf, np.inf))
        # betas >= 0
        for _ in range(self.p):
            bnds.append((1.0, np.inf))
        return bnds

    xǁGJRGARCHǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGJRGARCHǁbounds__mutmut_1": xǁGJRGARCHǁbounds__mutmut_1,
        "xǁGJRGARCHǁbounds__mutmut_2": xǁGJRGARCHǁbounds__mutmut_2,
        "xǁGJRGARCHǁbounds__mutmut_3": xǁGJRGARCHǁbounds__mutmut_3,
        "xǁGJRGARCHǁbounds__mutmut_4": xǁGJRGARCHǁbounds__mutmut_4,
        "xǁGJRGARCHǁbounds__mutmut_5": xǁGJRGARCHǁbounds__mutmut_5,
        "xǁGJRGARCHǁbounds__mutmut_6": xǁGJRGARCHǁbounds__mutmut_6,
        "xǁGJRGARCHǁbounds__mutmut_7": xǁGJRGARCHǁbounds__mutmut_7,
        "xǁGJRGARCHǁbounds__mutmut_8": xǁGJRGARCHǁbounds__mutmut_8,
        "xǁGJRGARCHǁbounds__mutmut_9": xǁGJRGARCHǁbounds__mutmut_9,
        "xǁGJRGARCHǁbounds__mutmut_10": xǁGJRGARCHǁbounds__mutmut_10,
        "xǁGJRGARCHǁbounds__mutmut_11": xǁGJRGARCHǁbounds__mutmut_11,
        "xǁGJRGARCHǁbounds__mutmut_12": xǁGJRGARCHǁbounds__mutmut_12,
    }
    xǁGJRGARCHǁbounds__mutmut_orig.__name__ = "xǁGJRGARCHǁbounds"

    @property
    def num_params(self) -> int:
        """Number of model parameters."""
        return 1 + 2 * self.q + self.p
