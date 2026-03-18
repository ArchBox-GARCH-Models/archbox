"""Component GARCH model (Engle & Lee, 1999).

sigma^2_t = q_t + h_t

q_t = omega + beta_p * (q_{t-1} - omega) + alpha_p * (eps^2_{t-1} - sigma^2_{t-1})
h_t = alpha * (eps^2_{t-1} - q_{t-1}) + beta * h_{t-1}

Decomposes variance into permanent (q_t) and transitory (h_t) components.
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


class ComponentGARCH(VolatilityModel):
    """Component GARCH model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "Component GARCH"

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        args = [endog, mean, dist]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁComponentGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁComponentGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁComponentGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=mean, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=mean, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=mean, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=mean, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=mean, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(None, mean=mean, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=None, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, mean=mean, dist=None)

    def xǁComponentGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(mean=mean, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(endog, dist=dist)

    def xǁComponentGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize Component GARCH model with options."""
        super().__init__(
            endog,
            mean=mean,
        )

    xǁComponentGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁComponentGARCHǁ__init____mutmut_1": xǁComponentGARCHǁ__init____mutmut_1,
        "xǁComponentGARCHǁ__init____mutmut_2": xǁComponentGARCHǁ__init____mutmut_2,
        "xǁComponentGARCHǁ__init____mutmut_3": xǁComponentGARCHǁ__init____mutmut_3,
        "xǁComponentGARCHǁ__init____mutmut_4": xǁComponentGARCHǁ__init____mutmut_4,
        "xǁComponentGARCHǁ__init____mutmut_5": xǁComponentGARCHǁ__init____mutmut_5,
        "xǁComponentGARCHǁ__init____mutmut_6": xǁComponentGARCHǁ__init____mutmut_6,
        "xǁComponentGARCHǁ__init____mutmut_7": xǁComponentGARCHǁ__init____mutmut_7,
        "xǁComponentGARCHǁ__init____mutmut_8": xǁComponentGARCHǁ__init____mutmut_8,
        "xǁComponentGARCHǁ__init____mutmut_9": xǁComponentGARCHǁ__init____mutmut_9,
        "xǁComponentGARCHǁ__init____mutmut_10": xǁComponentGARCHǁ__init____mutmut_10,
    }
    xǁComponentGARCHǁ__init____mutmut_orig.__name__ = "xǁComponentGARCHǁ__init__"

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁComponentGARCHǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁComponentGARCHǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁComponentGARCHǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = None
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[1]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = None
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[2]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = None
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[3]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = None
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[4]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = None

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[5]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = None
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = None
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(None)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = None
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(None)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = None

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(None)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = None  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[1] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = None  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[1] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 1.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = None

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[1] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] - h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[1] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[1]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(None, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, None):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(
            1,
        ):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(2, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = None
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] * 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t + 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 2] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 3
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = None
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) - alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega - beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p / (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] + omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t + 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 2] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p / (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 + sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t + 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 2])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = None
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(None, 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], None)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(
                q[t],
            )
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1.000000000001)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = None
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) - beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha / (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_58(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 + q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_59(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t + 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_60(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 2]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_61(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta / h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_62(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t + 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_63(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 2]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_64(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = None
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_65(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] - h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_66(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = None

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_67(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(None, 1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_68(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], None)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_69(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(1e-12)

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_70(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(
                sigma2[t],
            )

        return sigma2

    def xǁComponentGARCHǁ_variance_recursion__mutmut_71(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via Component GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha, beta, alpha_p, beta_p]
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t = q_t + h_t.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        # Initialize
        q[0] = backcast  # long-run variance
        h[0] = 0.0  # transitory starts at zero
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1.000000000001)

        return sigma2

    xǁComponentGARCHǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁComponentGARCHǁ_variance_recursion__mutmut_1": xǁComponentGARCHǁ_variance_recursion__mutmut_1,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_2": xǁComponentGARCHǁ_variance_recursion__mutmut_2,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_3": xǁComponentGARCHǁ_variance_recursion__mutmut_3,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_4": xǁComponentGARCHǁ_variance_recursion__mutmut_4,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_5": xǁComponentGARCHǁ_variance_recursion__mutmut_5,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_6": xǁComponentGARCHǁ_variance_recursion__mutmut_6,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_7": xǁComponentGARCHǁ_variance_recursion__mutmut_7,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_8": xǁComponentGARCHǁ_variance_recursion__mutmut_8,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_9": xǁComponentGARCHǁ_variance_recursion__mutmut_9,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_10": xǁComponentGARCHǁ_variance_recursion__mutmut_10,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_11": xǁComponentGARCHǁ_variance_recursion__mutmut_11,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_12": xǁComponentGARCHǁ_variance_recursion__mutmut_12,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_13": xǁComponentGARCHǁ_variance_recursion__mutmut_13,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_14": xǁComponentGARCHǁ_variance_recursion__mutmut_14,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_15": xǁComponentGARCHǁ_variance_recursion__mutmut_15,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_16": xǁComponentGARCHǁ_variance_recursion__mutmut_16,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_17": xǁComponentGARCHǁ_variance_recursion__mutmut_17,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_18": xǁComponentGARCHǁ_variance_recursion__mutmut_18,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_19": xǁComponentGARCHǁ_variance_recursion__mutmut_19,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_20": xǁComponentGARCHǁ_variance_recursion__mutmut_20,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_21": xǁComponentGARCHǁ_variance_recursion__mutmut_21,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_22": xǁComponentGARCHǁ_variance_recursion__mutmut_22,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_23": xǁComponentGARCHǁ_variance_recursion__mutmut_23,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_24": xǁComponentGARCHǁ_variance_recursion__mutmut_24,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_25": xǁComponentGARCHǁ_variance_recursion__mutmut_25,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_26": xǁComponentGARCHǁ_variance_recursion__mutmut_26,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_27": xǁComponentGARCHǁ_variance_recursion__mutmut_27,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_28": xǁComponentGARCHǁ_variance_recursion__mutmut_28,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_29": xǁComponentGARCHǁ_variance_recursion__mutmut_29,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_30": xǁComponentGARCHǁ_variance_recursion__mutmut_30,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_31": xǁComponentGARCHǁ_variance_recursion__mutmut_31,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_32": xǁComponentGARCHǁ_variance_recursion__mutmut_32,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_33": xǁComponentGARCHǁ_variance_recursion__mutmut_33,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_34": xǁComponentGARCHǁ_variance_recursion__mutmut_34,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_35": xǁComponentGARCHǁ_variance_recursion__mutmut_35,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_36": xǁComponentGARCHǁ_variance_recursion__mutmut_36,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_37": xǁComponentGARCHǁ_variance_recursion__mutmut_37,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_38": xǁComponentGARCHǁ_variance_recursion__mutmut_38,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_39": xǁComponentGARCHǁ_variance_recursion__mutmut_39,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_40": xǁComponentGARCHǁ_variance_recursion__mutmut_40,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_41": xǁComponentGARCHǁ_variance_recursion__mutmut_41,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_42": xǁComponentGARCHǁ_variance_recursion__mutmut_42,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_43": xǁComponentGARCHǁ_variance_recursion__mutmut_43,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_44": xǁComponentGARCHǁ_variance_recursion__mutmut_44,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_45": xǁComponentGARCHǁ_variance_recursion__mutmut_45,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_46": xǁComponentGARCHǁ_variance_recursion__mutmut_46,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_47": xǁComponentGARCHǁ_variance_recursion__mutmut_47,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_48": xǁComponentGARCHǁ_variance_recursion__mutmut_48,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_49": xǁComponentGARCHǁ_variance_recursion__mutmut_49,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_50": xǁComponentGARCHǁ_variance_recursion__mutmut_50,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_51": xǁComponentGARCHǁ_variance_recursion__mutmut_51,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_52": xǁComponentGARCHǁ_variance_recursion__mutmut_52,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_53": xǁComponentGARCHǁ_variance_recursion__mutmut_53,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_54": xǁComponentGARCHǁ_variance_recursion__mutmut_54,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_55": xǁComponentGARCHǁ_variance_recursion__mutmut_55,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_56": xǁComponentGARCHǁ_variance_recursion__mutmut_56,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_57": xǁComponentGARCHǁ_variance_recursion__mutmut_57,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_58": xǁComponentGARCHǁ_variance_recursion__mutmut_58,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_59": xǁComponentGARCHǁ_variance_recursion__mutmut_59,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_60": xǁComponentGARCHǁ_variance_recursion__mutmut_60,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_61": xǁComponentGARCHǁ_variance_recursion__mutmut_61,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_62": xǁComponentGARCHǁ_variance_recursion__mutmut_62,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_63": xǁComponentGARCHǁ_variance_recursion__mutmut_63,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_64": xǁComponentGARCHǁ_variance_recursion__mutmut_64,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_65": xǁComponentGARCHǁ_variance_recursion__mutmut_65,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_66": xǁComponentGARCHǁ_variance_recursion__mutmut_66,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_67": xǁComponentGARCHǁ_variance_recursion__mutmut_67,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_68": xǁComponentGARCHǁ_variance_recursion__mutmut_68,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_69": xǁComponentGARCHǁ_variance_recursion__mutmut_69,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_70": xǁComponentGARCHǁ_variance_recursion__mutmut_70,
        "xǁComponentGARCHǁ_variance_recursion__mutmut_71": xǁComponentGARCHǁ_variance_recursion__mutmut_71,
    }
    xǁComponentGARCHǁ_variance_recursion__mutmut_orig.__name__ = (
        "xǁComponentGARCHǁ_variance_recursion"
    )

    def variance_decomposition(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁComponentGARCHǁvariance_decomposition__mutmut_orig"),
            object.__getattribute__(
                self, "xǁComponentGARCHǁvariance_decomposition__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁComponentGARCHǁvariance_decomposition__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = None
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[1]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = None
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[2]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = None
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[3]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = None
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[4]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = None

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[5]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = None
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = None
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(None)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = None
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(None)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = None

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(None)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = None
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[1] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = None
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[1] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 1.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = None

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[1] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] - h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[1] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[1]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(None, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, None):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(
            1,
        ):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(2, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = None
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] * 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t + 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_36(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 2] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_37(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 3
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_38(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = None
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_39(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) - alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_40(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega - beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_41(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p / (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_42(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] + omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_43(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t + 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_44(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 2] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_45(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p / (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_46(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 + sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_47(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t + 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_48(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 2])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_49(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = None
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_50(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(None, 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_51(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], None)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_52(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_53(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(
                q[t],
            )
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_54(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1.000000000001)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_55(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = None
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_56(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) - beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_57(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha / (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_58(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 + q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_59(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t + 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_60(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 2]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_61(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta / h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_62(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t + 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_63(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 2]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_64(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = None
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_65(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] - h[t]
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_66(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = None

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_67(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(None, 1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_68(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], None)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_69(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(1e-12)

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_70(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(
                sigma2[t],
            )

        return sigma2, q, h

    def xǁComponentGARCHǁvariance_decomposition__mutmut_71(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute sigma2, q_t (permanent) and h_t (transitory) components.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        resids : ndarray
            Residuals.
        backcast : float
            Initial variance.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (sigma2, q_t, h_t) arrays.
        """
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        nobs = len(resids)
        sigma2 = np.empty(nobs)
        q = np.empty(nobs)
        h = np.empty(nobs)

        q[0] = backcast
        h[0] = 0.0
        sigma2[0] = q[0] + h[0]

        for t in range(1, nobs):
            eps2 = resids[t - 1] ** 2
            q[t] = omega + beta_p * (q[t - 1] - omega) + alpha_p * (eps2 - sigma2[t - 1])
            q[t] = max(q[t], 1e-12)
            h[t] = alpha * (eps2 - q[t - 1]) + beta * h[t - 1]
            sigma2[t] = q[t] + h[t]
            sigma2[t] = max(sigma2[t], 1.000000000001)

        return sigma2, q, h

    xǁComponentGARCHǁvariance_decomposition__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁComponentGARCHǁvariance_decomposition__mutmut_1": xǁComponentGARCHǁvariance_decomposition__mutmut_1,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_2": xǁComponentGARCHǁvariance_decomposition__mutmut_2,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_3": xǁComponentGARCHǁvariance_decomposition__mutmut_3,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_4": xǁComponentGARCHǁvariance_decomposition__mutmut_4,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_5": xǁComponentGARCHǁvariance_decomposition__mutmut_5,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_6": xǁComponentGARCHǁvariance_decomposition__mutmut_6,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_7": xǁComponentGARCHǁvariance_decomposition__mutmut_7,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_8": xǁComponentGARCHǁvariance_decomposition__mutmut_8,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_9": xǁComponentGARCHǁvariance_decomposition__mutmut_9,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_10": xǁComponentGARCHǁvariance_decomposition__mutmut_10,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_11": xǁComponentGARCHǁvariance_decomposition__mutmut_11,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_12": xǁComponentGARCHǁvariance_decomposition__mutmut_12,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_13": xǁComponentGARCHǁvariance_decomposition__mutmut_13,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_14": xǁComponentGARCHǁvariance_decomposition__mutmut_14,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_15": xǁComponentGARCHǁvariance_decomposition__mutmut_15,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_16": xǁComponentGARCHǁvariance_decomposition__mutmut_16,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_17": xǁComponentGARCHǁvariance_decomposition__mutmut_17,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_18": xǁComponentGARCHǁvariance_decomposition__mutmut_18,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_19": xǁComponentGARCHǁvariance_decomposition__mutmut_19,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_20": xǁComponentGARCHǁvariance_decomposition__mutmut_20,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_21": xǁComponentGARCHǁvariance_decomposition__mutmut_21,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_22": xǁComponentGARCHǁvariance_decomposition__mutmut_22,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_23": xǁComponentGARCHǁvariance_decomposition__mutmut_23,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_24": xǁComponentGARCHǁvariance_decomposition__mutmut_24,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_25": xǁComponentGARCHǁvariance_decomposition__mutmut_25,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_26": xǁComponentGARCHǁvariance_decomposition__mutmut_26,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_27": xǁComponentGARCHǁvariance_decomposition__mutmut_27,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_28": xǁComponentGARCHǁvariance_decomposition__mutmut_28,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_29": xǁComponentGARCHǁvariance_decomposition__mutmut_29,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_30": xǁComponentGARCHǁvariance_decomposition__mutmut_30,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_31": xǁComponentGARCHǁvariance_decomposition__mutmut_31,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_32": xǁComponentGARCHǁvariance_decomposition__mutmut_32,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_33": xǁComponentGARCHǁvariance_decomposition__mutmut_33,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_34": xǁComponentGARCHǁvariance_decomposition__mutmut_34,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_35": xǁComponentGARCHǁvariance_decomposition__mutmut_35,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_36": xǁComponentGARCHǁvariance_decomposition__mutmut_36,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_37": xǁComponentGARCHǁvariance_decomposition__mutmut_37,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_38": xǁComponentGARCHǁvariance_decomposition__mutmut_38,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_39": xǁComponentGARCHǁvariance_decomposition__mutmut_39,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_40": xǁComponentGARCHǁvariance_decomposition__mutmut_40,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_41": xǁComponentGARCHǁvariance_decomposition__mutmut_41,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_42": xǁComponentGARCHǁvariance_decomposition__mutmut_42,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_43": xǁComponentGARCHǁvariance_decomposition__mutmut_43,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_44": xǁComponentGARCHǁvariance_decomposition__mutmut_44,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_45": xǁComponentGARCHǁvariance_decomposition__mutmut_45,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_46": xǁComponentGARCHǁvariance_decomposition__mutmut_46,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_47": xǁComponentGARCHǁvariance_decomposition__mutmut_47,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_48": xǁComponentGARCHǁvariance_decomposition__mutmut_48,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_49": xǁComponentGARCHǁvariance_decomposition__mutmut_49,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_50": xǁComponentGARCHǁvariance_decomposition__mutmut_50,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_51": xǁComponentGARCHǁvariance_decomposition__mutmut_51,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_52": xǁComponentGARCHǁvariance_decomposition__mutmut_52,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_53": xǁComponentGARCHǁvariance_decomposition__mutmut_53,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_54": xǁComponentGARCHǁvariance_decomposition__mutmut_54,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_55": xǁComponentGARCHǁvariance_decomposition__mutmut_55,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_56": xǁComponentGARCHǁvariance_decomposition__mutmut_56,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_57": xǁComponentGARCHǁvariance_decomposition__mutmut_57,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_58": xǁComponentGARCHǁvariance_decomposition__mutmut_58,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_59": xǁComponentGARCHǁvariance_decomposition__mutmut_59,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_60": xǁComponentGARCHǁvariance_decomposition__mutmut_60,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_61": xǁComponentGARCHǁvariance_decomposition__mutmut_61,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_62": xǁComponentGARCHǁvariance_decomposition__mutmut_62,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_63": xǁComponentGARCHǁvariance_decomposition__mutmut_63,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_64": xǁComponentGARCHǁvariance_decomposition__mutmut_64,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_65": xǁComponentGARCHǁvariance_decomposition__mutmut_65,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_66": xǁComponentGARCHǁvariance_decomposition__mutmut_66,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_67": xǁComponentGARCHǁvariance_decomposition__mutmut_67,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_68": xǁComponentGARCHǁvariance_decomposition__mutmut_68,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_69": xǁComponentGARCHǁvariance_decomposition__mutmut_69,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_70": xǁComponentGARCHǁvariance_decomposition__mutmut_70,
        "xǁComponentGARCHǁvariance_decomposition__mutmut_71": xǁComponentGARCHǁvariance_decomposition__mutmut_71,
    }
    xǁComponentGARCHǁvariance_decomposition__mutmut_orig.__name__ = (
        "xǁComponentGARCHǁvariance_decomposition"
    )

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁComponentGARCHǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁComponentGARCHǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁComponentGARCHǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = None
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[1]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = None
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[2]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = None
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[3]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = None
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[4]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = None

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[5]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = None
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps * 2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**3
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = None  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = None
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 1.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = None
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) - alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_19(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega - beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p / (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_21(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev + omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_22(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p / (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_23(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 + sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_24(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = None
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_25(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) - beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_26(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha / (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_27(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 + q_prev) + beta * h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_28(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta / h_prev
        return float(max(q + h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_29(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(None)

    def xǁComponentGARCHǁ_one_step_variance__mutmut_30(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(None, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_31(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, None))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_32(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_33(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(
            max(
                q + h,
            )
        )

    def xǁComponentGARCHǁ_one_step_variance__mutmut_34(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q - h, 1e-12))

    def xǁComponentGARCHǁ_one_step_variance__mutmut_35(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2]
        alpha_p = params[3]
        beta_p = params[4]

        eps2 = eps**2
        q_prev = sigma2_prev  # approximation: assume q_{t-1} ~ sigma2_{t-1}
        h_prev = 0.0
        q = omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - sigma2_prev)
        h = alpha * (eps2 - q_prev) + beta * h_prev
        return float(max(q + h, 1.000000000001))

    xǁComponentGARCHǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁComponentGARCHǁ_one_step_variance__mutmut_1": xǁComponentGARCHǁ_one_step_variance__mutmut_1,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_2": xǁComponentGARCHǁ_one_step_variance__mutmut_2,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_3": xǁComponentGARCHǁ_one_step_variance__mutmut_3,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_4": xǁComponentGARCHǁ_one_step_variance__mutmut_4,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_5": xǁComponentGARCHǁ_one_step_variance__mutmut_5,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_6": xǁComponentGARCHǁ_one_step_variance__mutmut_6,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_7": xǁComponentGARCHǁ_one_step_variance__mutmut_7,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_8": xǁComponentGARCHǁ_one_step_variance__mutmut_8,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_9": xǁComponentGARCHǁ_one_step_variance__mutmut_9,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_10": xǁComponentGARCHǁ_one_step_variance__mutmut_10,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_11": xǁComponentGARCHǁ_one_step_variance__mutmut_11,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_12": xǁComponentGARCHǁ_one_step_variance__mutmut_12,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_13": xǁComponentGARCHǁ_one_step_variance__mutmut_13,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_14": xǁComponentGARCHǁ_one_step_variance__mutmut_14,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_15": xǁComponentGARCHǁ_one_step_variance__mutmut_15,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_16": xǁComponentGARCHǁ_one_step_variance__mutmut_16,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_17": xǁComponentGARCHǁ_one_step_variance__mutmut_17,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_18": xǁComponentGARCHǁ_one_step_variance__mutmut_18,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_19": xǁComponentGARCHǁ_one_step_variance__mutmut_19,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_20": xǁComponentGARCHǁ_one_step_variance__mutmut_20,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_21": xǁComponentGARCHǁ_one_step_variance__mutmut_21,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_22": xǁComponentGARCHǁ_one_step_variance__mutmut_22,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_23": xǁComponentGARCHǁ_one_step_variance__mutmut_23,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_24": xǁComponentGARCHǁ_one_step_variance__mutmut_24,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_25": xǁComponentGARCHǁ_one_step_variance__mutmut_25,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_26": xǁComponentGARCHǁ_one_step_variance__mutmut_26,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_27": xǁComponentGARCHǁ_one_step_variance__mutmut_27,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_28": xǁComponentGARCHǁ_one_step_variance__mutmut_28,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_29": xǁComponentGARCHǁ_one_step_variance__mutmut_29,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_30": xǁComponentGARCHǁ_one_step_variance__mutmut_30,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_31": xǁComponentGARCHǁ_one_step_variance__mutmut_31,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_32": xǁComponentGARCHǁ_one_step_variance__mutmut_32,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_33": xǁComponentGARCHǁ_one_step_variance__mutmut_33,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_34": xǁComponentGARCHǁ_one_step_variance__mutmut_34,
        "xǁComponentGARCHǁ_one_step_variance__mutmut_35": xǁComponentGARCHǁ_one_step_variance__mutmut_35,
    }
    xǁComponentGARCHǁ_one_step_variance__mutmut_orig.__name__ = (
        "xǁComponentGARCHǁ_one_step_variance"
    )

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: [omega, alpha, beta, alpha_p, beta_p]."""
        var = np.var(self.endog)
        return np.array([var, 0.05, 0.10, 0.04, 0.98])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        return ["omega", "alpha", "beta", "alpha_p", "beta_p"]

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁComponentGARCHǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁComponentGARCHǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁComponentGARCHǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = None
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = None
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[1] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(None)
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[1])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = None
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[2] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(None)
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[2])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = None
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[3] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(None)
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[3])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = None
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[4] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(None)
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_17(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[4])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_18(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = None
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_19(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[5] = 1.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_20(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 * (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_21(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 2.0 / (1.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_22(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 - np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_23(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (2.0 + np.exp(-unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_24(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(None))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_25(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(+unconstrained[4]))
        return constrained

    def xǁComponentGARCHǁtransform_params__mutmut_26(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0
        constrained[0] = np.exp(unconstrained[0])
        # alpha >= 0
        constrained[1] = np.exp(unconstrained[1])
        # beta >= 0
        constrained[2] = np.exp(unconstrained[2])
        # alpha_p >= 0
        constrained[3] = np.exp(unconstrained[3])
        # 0 < beta_p < 1 via sigmoid
        constrained[4] = 1.0 / (1.0 + np.exp(-unconstrained[5]))
        return constrained

    xǁComponentGARCHǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁComponentGARCHǁtransform_params__mutmut_1": xǁComponentGARCHǁtransform_params__mutmut_1,
        "xǁComponentGARCHǁtransform_params__mutmut_2": xǁComponentGARCHǁtransform_params__mutmut_2,
        "xǁComponentGARCHǁtransform_params__mutmut_3": xǁComponentGARCHǁtransform_params__mutmut_3,
        "xǁComponentGARCHǁtransform_params__mutmut_4": xǁComponentGARCHǁtransform_params__mutmut_4,
        "xǁComponentGARCHǁtransform_params__mutmut_5": xǁComponentGARCHǁtransform_params__mutmut_5,
        "xǁComponentGARCHǁtransform_params__mutmut_6": xǁComponentGARCHǁtransform_params__mutmut_6,
        "xǁComponentGARCHǁtransform_params__mutmut_7": xǁComponentGARCHǁtransform_params__mutmut_7,
        "xǁComponentGARCHǁtransform_params__mutmut_8": xǁComponentGARCHǁtransform_params__mutmut_8,
        "xǁComponentGARCHǁtransform_params__mutmut_9": xǁComponentGARCHǁtransform_params__mutmut_9,
        "xǁComponentGARCHǁtransform_params__mutmut_10": xǁComponentGARCHǁtransform_params__mutmut_10,
        "xǁComponentGARCHǁtransform_params__mutmut_11": xǁComponentGARCHǁtransform_params__mutmut_11,
        "xǁComponentGARCHǁtransform_params__mutmut_12": xǁComponentGARCHǁtransform_params__mutmut_12,
        "xǁComponentGARCHǁtransform_params__mutmut_13": xǁComponentGARCHǁtransform_params__mutmut_13,
        "xǁComponentGARCHǁtransform_params__mutmut_14": xǁComponentGARCHǁtransform_params__mutmut_14,
        "xǁComponentGARCHǁtransform_params__mutmut_15": xǁComponentGARCHǁtransform_params__mutmut_15,
        "xǁComponentGARCHǁtransform_params__mutmut_16": xǁComponentGARCHǁtransform_params__mutmut_16,
        "xǁComponentGARCHǁtransform_params__mutmut_17": xǁComponentGARCHǁtransform_params__mutmut_17,
        "xǁComponentGARCHǁtransform_params__mutmut_18": xǁComponentGARCHǁtransform_params__mutmut_18,
        "xǁComponentGARCHǁtransform_params__mutmut_19": xǁComponentGARCHǁtransform_params__mutmut_19,
        "xǁComponentGARCHǁtransform_params__mutmut_20": xǁComponentGARCHǁtransform_params__mutmut_20,
        "xǁComponentGARCHǁtransform_params__mutmut_21": xǁComponentGARCHǁtransform_params__mutmut_21,
        "xǁComponentGARCHǁtransform_params__mutmut_22": xǁComponentGARCHǁtransform_params__mutmut_22,
        "xǁComponentGARCHǁtransform_params__mutmut_23": xǁComponentGARCHǁtransform_params__mutmut_23,
        "xǁComponentGARCHǁtransform_params__mutmut_24": xǁComponentGARCHǁtransform_params__mutmut_24,
        "xǁComponentGARCHǁtransform_params__mutmut_25": xǁComponentGARCHǁtransform_params__mutmut_25,
        "xǁComponentGARCHǁtransform_params__mutmut_26": xǁComponentGARCHǁtransform_params__mutmut_26,
    }
    xǁComponentGARCHǁtransform_params__mutmut_orig.__name__ = "xǁComponentGARCHǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁComponentGARCHǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁComponentGARCHǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁComponentGARCHǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = None
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = None
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[1] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(None)
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(None, 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], None))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(
            max(
                constrained[0],
            )
        )
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[1], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1.000000000001))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = None
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[2] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(None)
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(None, 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], None))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(
            max(
                constrained[1],
            )
        )
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[2], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1.000000000001))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = None
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[3] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(None)
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(None, 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], None))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(
            max(
                constrained[2],
            )
        )
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[3], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1.000000000001))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_29(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = None
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_30(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[4] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_31(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(None)
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_32(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(None, 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_33(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], None))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_34(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_35(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(
            max(
                constrained[3],
            )
        )
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_36(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[4], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_37(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1.000000000001))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_38(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = None
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_39(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(None, 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_40(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], None, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_41(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, None)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_42(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_43(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_44(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(
            constrained[4],
            1e-6,
        )
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_45(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[5], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_46(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1.000001, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_47(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 + 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_48(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 2 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_49(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1.000001)
        unconstrained[4] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_50(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = None
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_51(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[5] = np.log(bp / (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_52(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(None)
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_53(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp * (1.0 - bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_54(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (1.0 + bp))
        return unconstrained

    def xǁComponentGARCHǁuntransform_params__mutmut_55(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        unconstrained[1] = np.log(max(constrained[1], 1e-12))
        unconstrained[2] = np.log(max(constrained[2], 1e-12))
        unconstrained[3] = np.log(max(constrained[3], 1e-12))
        bp = np.clip(constrained[4], 1e-6, 1 - 1e-6)
        unconstrained[4] = np.log(bp / (2.0 - bp))
        return unconstrained

    xǁComponentGARCHǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁComponentGARCHǁuntransform_params__mutmut_1": xǁComponentGARCHǁuntransform_params__mutmut_1,
        "xǁComponentGARCHǁuntransform_params__mutmut_2": xǁComponentGARCHǁuntransform_params__mutmut_2,
        "xǁComponentGARCHǁuntransform_params__mutmut_3": xǁComponentGARCHǁuntransform_params__mutmut_3,
        "xǁComponentGARCHǁuntransform_params__mutmut_4": xǁComponentGARCHǁuntransform_params__mutmut_4,
        "xǁComponentGARCHǁuntransform_params__mutmut_5": xǁComponentGARCHǁuntransform_params__mutmut_5,
        "xǁComponentGARCHǁuntransform_params__mutmut_6": xǁComponentGARCHǁuntransform_params__mutmut_6,
        "xǁComponentGARCHǁuntransform_params__mutmut_7": xǁComponentGARCHǁuntransform_params__mutmut_7,
        "xǁComponentGARCHǁuntransform_params__mutmut_8": xǁComponentGARCHǁuntransform_params__mutmut_8,
        "xǁComponentGARCHǁuntransform_params__mutmut_9": xǁComponentGARCHǁuntransform_params__mutmut_9,
        "xǁComponentGARCHǁuntransform_params__mutmut_10": xǁComponentGARCHǁuntransform_params__mutmut_10,
        "xǁComponentGARCHǁuntransform_params__mutmut_11": xǁComponentGARCHǁuntransform_params__mutmut_11,
        "xǁComponentGARCHǁuntransform_params__mutmut_12": xǁComponentGARCHǁuntransform_params__mutmut_12,
        "xǁComponentGARCHǁuntransform_params__mutmut_13": xǁComponentGARCHǁuntransform_params__mutmut_13,
        "xǁComponentGARCHǁuntransform_params__mutmut_14": xǁComponentGARCHǁuntransform_params__mutmut_14,
        "xǁComponentGARCHǁuntransform_params__mutmut_15": xǁComponentGARCHǁuntransform_params__mutmut_15,
        "xǁComponentGARCHǁuntransform_params__mutmut_16": xǁComponentGARCHǁuntransform_params__mutmut_16,
        "xǁComponentGARCHǁuntransform_params__mutmut_17": xǁComponentGARCHǁuntransform_params__mutmut_17,
        "xǁComponentGARCHǁuntransform_params__mutmut_18": xǁComponentGARCHǁuntransform_params__mutmut_18,
        "xǁComponentGARCHǁuntransform_params__mutmut_19": xǁComponentGARCHǁuntransform_params__mutmut_19,
        "xǁComponentGARCHǁuntransform_params__mutmut_20": xǁComponentGARCHǁuntransform_params__mutmut_20,
        "xǁComponentGARCHǁuntransform_params__mutmut_21": xǁComponentGARCHǁuntransform_params__mutmut_21,
        "xǁComponentGARCHǁuntransform_params__mutmut_22": xǁComponentGARCHǁuntransform_params__mutmut_22,
        "xǁComponentGARCHǁuntransform_params__mutmut_23": xǁComponentGARCHǁuntransform_params__mutmut_23,
        "xǁComponentGARCHǁuntransform_params__mutmut_24": xǁComponentGARCHǁuntransform_params__mutmut_24,
        "xǁComponentGARCHǁuntransform_params__mutmut_25": xǁComponentGARCHǁuntransform_params__mutmut_25,
        "xǁComponentGARCHǁuntransform_params__mutmut_26": xǁComponentGARCHǁuntransform_params__mutmut_26,
        "xǁComponentGARCHǁuntransform_params__mutmut_27": xǁComponentGARCHǁuntransform_params__mutmut_27,
        "xǁComponentGARCHǁuntransform_params__mutmut_28": xǁComponentGARCHǁuntransform_params__mutmut_28,
        "xǁComponentGARCHǁuntransform_params__mutmut_29": xǁComponentGARCHǁuntransform_params__mutmut_29,
        "xǁComponentGARCHǁuntransform_params__mutmut_30": xǁComponentGARCHǁuntransform_params__mutmut_30,
        "xǁComponentGARCHǁuntransform_params__mutmut_31": xǁComponentGARCHǁuntransform_params__mutmut_31,
        "xǁComponentGARCHǁuntransform_params__mutmut_32": xǁComponentGARCHǁuntransform_params__mutmut_32,
        "xǁComponentGARCHǁuntransform_params__mutmut_33": xǁComponentGARCHǁuntransform_params__mutmut_33,
        "xǁComponentGARCHǁuntransform_params__mutmut_34": xǁComponentGARCHǁuntransform_params__mutmut_34,
        "xǁComponentGARCHǁuntransform_params__mutmut_35": xǁComponentGARCHǁuntransform_params__mutmut_35,
        "xǁComponentGARCHǁuntransform_params__mutmut_36": xǁComponentGARCHǁuntransform_params__mutmut_36,
        "xǁComponentGARCHǁuntransform_params__mutmut_37": xǁComponentGARCHǁuntransform_params__mutmut_37,
        "xǁComponentGARCHǁuntransform_params__mutmut_38": xǁComponentGARCHǁuntransform_params__mutmut_38,
        "xǁComponentGARCHǁuntransform_params__mutmut_39": xǁComponentGARCHǁuntransform_params__mutmut_39,
        "xǁComponentGARCHǁuntransform_params__mutmut_40": xǁComponentGARCHǁuntransform_params__mutmut_40,
        "xǁComponentGARCHǁuntransform_params__mutmut_41": xǁComponentGARCHǁuntransform_params__mutmut_41,
        "xǁComponentGARCHǁuntransform_params__mutmut_42": xǁComponentGARCHǁuntransform_params__mutmut_42,
        "xǁComponentGARCHǁuntransform_params__mutmut_43": xǁComponentGARCHǁuntransform_params__mutmut_43,
        "xǁComponentGARCHǁuntransform_params__mutmut_44": xǁComponentGARCHǁuntransform_params__mutmut_44,
        "xǁComponentGARCHǁuntransform_params__mutmut_45": xǁComponentGARCHǁuntransform_params__mutmut_45,
        "xǁComponentGARCHǁuntransform_params__mutmut_46": xǁComponentGARCHǁuntransform_params__mutmut_46,
        "xǁComponentGARCHǁuntransform_params__mutmut_47": xǁComponentGARCHǁuntransform_params__mutmut_47,
        "xǁComponentGARCHǁuntransform_params__mutmut_48": xǁComponentGARCHǁuntransform_params__mutmut_48,
        "xǁComponentGARCHǁuntransform_params__mutmut_49": xǁComponentGARCHǁuntransform_params__mutmut_49,
        "xǁComponentGARCHǁuntransform_params__mutmut_50": xǁComponentGARCHǁuntransform_params__mutmut_50,
        "xǁComponentGARCHǁuntransform_params__mutmut_51": xǁComponentGARCHǁuntransform_params__mutmut_51,
        "xǁComponentGARCHǁuntransform_params__mutmut_52": xǁComponentGARCHǁuntransform_params__mutmut_52,
        "xǁComponentGARCHǁuntransform_params__mutmut_53": xǁComponentGARCHǁuntransform_params__mutmut_53,
        "xǁComponentGARCHǁuntransform_params__mutmut_54": xǁComponentGARCHǁuntransform_params__mutmut_54,
        "xǁComponentGARCHǁuntransform_params__mutmut_55": xǁComponentGARCHǁuntransform_params__mutmut_55,
    }
    xǁComponentGARCHǁuntransform_params__mutmut_orig.__name__ = (
        "xǁComponentGARCHǁuntransform_params"
    )

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁComponentGARCHǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁComponentGARCHǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁComponentGARCHǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.0, np.inf),  # alpha >= 0
            (0.0, np.inf),  # beta >= 0
            (0.0, np.inf),  # alpha_p >= 0
            (0.001, 0.999),  # 0 < beta_p < 1
        ]

    def xǁComponentGARCHǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1.000000000001, np.inf),  # omega > 0
            (0.0, np.inf),  # alpha >= 0
            (0.0, np.inf),  # beta >= 0
            (0.0, np.inf),  # alpha_p >= 0
            (0.001, 0.999),  # 0 < beta_p < 1
        ]

    def xǁComponentGARCHǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (1.0, np.inf),  # alpha >= 0
            (0.0, np.inf),  # beta >= 0
            (0.0, np.inf),  # alpha_p >= 0
            (0.001, 0.999),  # 0 < beta_p < 1
        ]

    def xǁComponentGARCHǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.0, np.inf),  # alpha >= 0
            (1.0, np.inf),  # beta >= 0
            (0.0, np.inf),  # alpha_p >= 0
            (0.001, 0.999),  # 0 < beta_p < 1
        ]

    def xǁComponentGARCHǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.0, np.inf),  # alpha >= 0
            (0.0, np.inf),  # beta >= 0
            (1.0, np.inf),  # alpha_p >= 0
            (0.001, 0.999),  # 0 < beta_p < 1
        ]

    def xǁComponentGARCHǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.0, np.inf),  # alpha >= 0
            (0.0, np.inf),  # beta >= 0
            (0.0, np.inf),  # alpha_p >= 0
            (1.001, 0.999),  # 0 < beta_p < 1
        ]

    def xǁComponentGARCHǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        return [
            (1e-12, np.inf),  # omega > 0
            (0.0, np.inf),  # alpha >= 0
            (0.0, np.inf),  # beta >= 0
            (0.0, np.inf),  # alpha_p >= 0
            (0.001, 1.999),  # 0 < beta_p < 1
        ]

    xǁComponentGARCHǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁComponentGARCHǁbounds__mutmut_1": xǁComponentGARCHǁbounds__mutmut_1,
        "xǁComponentGARCHǁbounds__mutmut_2": xǁComponentGARCHǁbounds__mutmut_2,
        "xǁComponentGARCHǁbounds__mutmut_3": xǁComponentGARCHǁbounds__mutmut_3,
        "xǁComponentGARCHǁbounds__mutmut_4": xǁComponentGARCHǁbounds__mutmut_4,
        "xǁComponentGARCHǁbounds__mutmut_5": xǁComponentGARCHǁbounds__mutmut_5,
        "xǁComponentGARCHǁbounds__mutmut_6": xǁComponentGARCHǁbounds__mutmut_6,
    }
    xǁComponentGARCHǁbounds__mutmut_orig.__name__ = "xǁComponentGARCHǁbounds"

    @property
    def num_params(self) -> int:
        """Number of parameters: omega, alpha, beta, alpha_p, beta_p."""
        return 5
