"""GARCH-M - GARCH in Mean model (Engle, Lilien & Robins, 1987).

r_t = mu + lambda * f(sigma^2_t) + eps_t
sigma^2_t = omega + alpha * eps^2_{t-1} + beta * sigma^2_{t-1}

The volatility (or variance) enters the mean equation as a risk premium.
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


class GARCHM(VolatilityModel):
    """GARCH-in-Mean model.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of GARCH lags (beta). Default 1.
    q : int
        Number of ARCH lags (alpha). Default 1.
    risk_premium : str
        Form of the risk premium in the mean equation.
        'variance' (default): f(sigma^2) = sigma^2
        'volatility': f(sigma^2) = sigma
        'log_variance': f(sigma^2) = log(sigma^2)
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution.
    """

    volatility_process = "GARCH-M"

    def __init__(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        args = [endog, p, q, risk_premium, mean, dist]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁ__init____mutmut_orig(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_1(
        self,
        endog: Any,
        p: int = 2,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_2(
        self,
        endog: Any,
        p: int = 1,
        q: int = 2,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_3(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "XXvarianceXX",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_4(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "VARIANCE",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_5(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "XXconstantXX",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_6(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "CONSTANT",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_7(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "XXnormalXX",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_8(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "NORMAL",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_9(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = None
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_10(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = None
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_11(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_12(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("XXvarianceXX", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_13(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("VARIANCE", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_14(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "XXvolatilityXX", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_15(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "VOLATILITY", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_16(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "XXlog_varianceXX"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_17(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "LOG_VARIANCE"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_18(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = None
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_19(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "XXUse 'variance', 'volatility', or 'log_variance'.XX"
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_20(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_21(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "USE 'VARIANCE', 'VOLATILITY', OR 'LOG_VARIANCE'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_22(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(None)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_23(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = None
        super().__init__(endog, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_24(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(None, mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_25(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=None, dist=dist)

    def xǁGARCHMǁ__init____mutmut_26(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, mean=mean, dist=None)

    def xǁGARCHMǁ__init____mutmut_27(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(mean=mean, dist=dist)

    def xǁGARCHMǁ__init____mutmut_28(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(endog, dist=dist)

    def xǁGARCHMǁ__init____mutmut_29(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        risk_premium: str = "variance",
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH-M model with lag orders and risk premium type."""
        self.p = p
        self.q = q
        if risk_premium not in ("variance", "volatility", "log_variance"):
            msg = (
                f"Unknown risk_premium: {risk_premium}. "
                "Use 'variance', 'volatility', or 'log_variance'."
            )
            raise ValueError(msg)
        self.risk_premium = risk_premium
        super().__init__(
            endog,
            mean=mean,
        )

    xǁGARCHMǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁ__init____mutmut_1": xǁGARCHMǁ__init____mutmut_1,
        "xǁGARCHMǁ__init____mutmut_2": xǁGARCHMǁ__init____mutmut_2,
        "xǁGARCHMǁ__init____mutmut_3": xǁGARCHMǁ__init____mutmut_3,
        "xǁGARCHMǁ__init____mutmut_4": xǁGARCHMǁ__init____mutmut_4,
        "xǁGARCHMǁ__init____mutmut_5": xǁGARCHMǁ__init____mutmut_5,
        "xǁGARCHMǁ__init____mutmut_6": xǁGARCHMǁ__init____mutmut_6,
        "xǁGARCHMǁ__init____mutmut_7": xǁGARCHMǁ__init____mutmut_7,
        "xǁGARCHMǁ__init____mutmut_8": xǁGARCHMǁ__init____mutmut_8,
        "xǁGARCHMǁ__init____mutmut_9": xǁGARCHMǁ__init____mutmut_9,
        "xǁGARCHMǁ__init____mutmut_10": xǁGARCHMǁ__init____mutmut_10,
        "xǁGARCHMǁ__init____mutmut_11": xǁGARCHMǁ__init____mutmut_11,
        "xǁGARCHMǁ__init____mutmut_12": xǁGARCHMǁ__init____mutmut_12,
        "xǁGARCHMǁ__init____mutmut_13": xǁGARCHMǁ__init____mutmut_13,
        "xǁGARCHMǁ__init____mutmut_14": xǁGARCHMǁ__init____mutmut_14,
        "xǁGARCHMǁ__init____mutmut_15": xǁGARCHMǁ__init____mutmut_15,
        "xǁGARCHMǁ__init____mutmut_16": xǁGARCHMǁ__init____mutmut_16,
        "xǁGARCHMǁ__init____mutmut_17": xǁGARCHMǁ__init____mutmut_17,
        "xǁGARCHMǁ__init____mutmut_18": xǁGARCHMǁ__init____mutmut_18,
        "xǁGARCHMǁ__init____mutmut_19": xǁGARCHMǁ__init____mutmut_19,
        "xǁGARCHMǁ__init____mutmut_20": xǁGARCHMǁ__init____mutmut_20,
        "xǁGARCHMǁ__init____mutmut_21": xǁGARCHMǁ__init____mutmut_21,
        "xǁGARCHMǁ__init____mutmut_22": xǁGARCHMǁ__init____mutmut_22,
        "xǁGARCHMǁ__init____mutmut_23": xǁGARCHMǁ__init____mutmut_23,
        "xǁGARCHMǁ__init____mutmut_24": xǁGARCHMǁ__init____mutmut_24,
        "xǁGARCHMǁ__init____mutmut_25": xǁGARCHMǁ__init____mutmut_25,
        "xǁGARCHMǁ__init____mutmut_26": xǁGARCHMǁ__init____mutmut_26,
        "xǁGARCHMǁ__init____mutmut_27": xǁGARCHMǁ__init____mutmut_27,
        "xǁGARCHMǁ__init____mutmut_28": xǁGARCHMǁ__init____mutmut_28,
        "xǁGARCHMǁ__init____mutmut_29": xǁGARCHMǁ__init____mutmut_29,
    }
    xǁGARCHMǁ__init____mutmut_orig.__name__ = "xǁGARCHMǁ__init__"

    def _risk_premium_function(self, sigma2: float) -> float:
        args = [sigma2]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁ_risk_premium_function__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁ_risk_premium_function__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁ_risk_premium_function__mutmut_orig(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_1(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium != "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_2(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "XXvarianceXX":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_3(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "VARIANCE":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_4(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium != "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_5(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "XXvolatilityXX":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_6(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "VOLATILITY":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_7(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(None)
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_8(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(None, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_9(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, None))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_10(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_11(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(
                max(
                    sigma2,
                )
            )
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_12(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1.000000000001))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_13(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium != "log_variance":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_14(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "XXlog_varianceXX":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_15(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "LOG_VARIANCE":
            return np.log(max(sigma2, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_16(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(None)
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_17(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(None, 1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_18(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, None))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_19(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(1e-12))
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_20(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(
                max(
                    sigma2,
                )
            )
        return sigma2

    def xǁGARCHMǁ_risk_premium_function__mutmut_21(self, sigma2: float) -> float:
        """Compute the risk premium term f(sigma^2)."""
        if self.risk_premium == "variance":
            return sigma2
        elif self.risk_premium == "volatility":
            return np.sqrt(max(sigma2, 1e-12))
        elif self.risk_premium == "log_variance":
            return np.log(max(sigma2, 1.000000000001))
        return sigma2

    xǁGARCHMǁ_risk_premium_function__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁ_risk_premium_function__mutmut_1": xǁGARCHMǁ_risk_premium_function__mutmut_1,
        "xǁGARCHMǁ_risk_premium_function__mutmut_2": xǁGARCHMǁ_risk_premium_function__mutmut_2,
        "xǁGARCHMǁ_risk_premium_function__mutmut_3": xǁGARCHMǁ_risk_premium_function__mutmut_3,
        "xǁGARCHMǁ_risk_premium_function__mutmut_4": xǁGARCHMǁ_risk_premium_function__mutmut_4,
        "xǁGARCHMǁ_risk_premium_function__mutmut_5": xǁGARCHMǁ_risk_premium_function__mutmut_5,
        "xǁGARCHMǁ_risk_premium_function__mutmut_6": xǁGARCHMǁ_risk_premium_function__mutmut_6,
        "xǁGARCHMǁ_risk_premium_function__mutmut_7": xǁGARCHMǁ_risk_premium_function__mutmut_7,
        "xǁGARCHMǁ_risk_premium_function__mutmut_8": xǁGARCHMǁ_risk_premium_function__mutmut_8,
        "xǁGARCHMǁ_risk_premium_function__mutmut_9": xǁGARCHMǁ_risk_premium_function__mutmut_9,
        "xǁGARCHMǁ_risk_premium_function__mutmut_10": xǁGARCHMǁ_risk_premium_function__mutmut_10,
        "xǁGARCHMǁ_risk_premium_function__mutmut_11": xǁGARCHMǁ_risk_premium_function__mutmut_11,
        "xǁGARCHMǁ_risk_premium_function__mutmut_12": xǁGARCHMǁ_risk_premium_function__mutmut_12,
        "xǁGARCHMǁ_risk_premium_function__mutmut_13": xǁGARCHMǁ_risk_premium_function__mutmut_13,
        "xǁGARCHMǁ_risk_premium_function__mutmut_14": xǁGARCHMǁ_risk_premium_function__mutmut_14,
        "xǁGARCHMǁ_risk_premium_function__mutmut_15": xǁGARCHMǁ_risk_premium_function__mutmut_15,
        "xǁGARCHMǁ_risk_premium_function__mutmut_16": xǁGARCHMǁ_risk_premium_function__mutmut_16,
        "xǁGARCHMǁ_risk_premium_function__mutmut_17": xǁGARCHMǁ_risk_premium_function__mutmut_17,
        "xǁGARCHMǁ_risk_premium_function__mutmut_18": xǁGARCHMǁ_risk_premium_function__mutmut_18,
        "xǁGARCHMǁ_risk_premium_function__mutmut_19": xǁGARCHMǁ_risk_premium_function__mutmut_19,
        "xǁGARCHMǁ_risk_premium_function__mutmut_20": xǁGARCHMǁ_risk_premium_function__mutmut_20,
        "xǁGARCHMǁ_risk_premium_function__mutmut_21": xǁGARCHMǁ_risk_premium_function__mutmut_21,
    }
    xǁGARCHMǁ_risk_premium_function__mutmut_orig.__name__ = "xǁGARCHMǁ_risk_premium_function"

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [params, resids, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁ_variance_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁ_variance_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁ_variance_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = None

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 - self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[2 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q - self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 - self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 2 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = None
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = None

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(None)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(None):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = None
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(None):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = None
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 + i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t + 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 2 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag > 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 1:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] = alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] -= alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] / resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] * 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 3
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] = alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] -= alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] / backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(None):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = None
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 + j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t + 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 2 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] = betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] -= betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] / (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag > 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 1 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = None

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(None, 1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], None)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(1e-12)

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(
                sigma2[t],
            )

        return sigma2

    def xǁGARCHMǁ_variance_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance via standard GARCH recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p, lambda]
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
        betas = params[1 + self.q : 1 + self.q + self.p]

        nobs = len(resids)
        sigma2 = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1.000000000001)

        return sigma2

    xǁGARCHMǁ_variance_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁ_variance_recursion__mutmut_1": xǁGARCHMǁ_variance_recursion__mutmut_1,
        "xǁGARCHMǁ_variance_recursion__mutmut_2": xǁGARCHMǁ_variance_recursion__mutmut_2,
        "xǁGARCHMǁ_variance_recursion__mutmut_3": xǁGARCHMǁ_variance_recursion__mutmut_3,
        "xǁGARCHMǁ_variance_recursion__mutmut_4": xǁGARCHMǁ_variance_recursion__mutmut_4,
        "xǁGARCHMǁ_variance_recursion__mutmut_5": xǁGARCHMǁ_variance_recursion__mutmut_5,
        "xǁGARCHMǁ_variance_recursion__mutmut_6": xǁGARCHMǁ_variance_recursion__mutmut_6,
        "xǁGARCHMǁ_variance_recursion__mutmut_7": xǁGARCHMǁ_variance_recursion__mutmut_7,
        "xǁGARCHMǁ_variance_recursion__mutmut_8": xǁGARCHMǁ_variance_recursion__mutmut_8,
        "xǁGARCHMǁ_variance_recursion__mutmut_9": xǁGARCHMǁ_variance_recursion__mutmut_9,
        "xǁGARCHMǁ_variance_recursion__mutmut_10": xǁGARCHMǁ_variance_recursion__mutmut_10,
        "xǁGARCHMǁ_variance_recursion__mutmut_11": xǁGARCHMǁ_variance_recursion__mutmut_11,
        "xǁGARCHMǁ_variance_recursion__mutmut_12": xǁGARCHMǁ_variance_recursion__mutmut_12,
        "xǁGARCHMǁ_variance_recursion__mutmut_13": xǁGARCHMǁ_variance_recursion__mutmut_13,
        "xǁGARCHMǁ_variance_recursion__mutmut_14": xǁGARCHMǁ_variance_recursion__mutmut_14,
        "xǁGARCHMǁ_variance_recursion__mutmut_15": xǁGARCHMǁ_variance_recursion__mutmut_15,
        "xǁGARCHMǁ_variance_recursion__mutmut_16": xǁGARCHMǁ_variance_recursion__mutmut_16,
        "xǁGARCHMǁ_variance_recursion__mutmut_17": xǁGARCHMǁ_variance_recursion__mutmut_17,
        "xǁGARCHMǁ_variance_recursion__mutmut_18": xǁGARCHMǁ_variance_recursion__mutmut_18,
        "xǁGARCHMǁ_variance_recursion__mutmut_19": xǁGARCHMǁ_variance_recursion__mutmut_19,
        "xǁGARCHMǁ_variance_recursion__mutmut_20": xǁGARCHMǁ_variance_recursion__mutmut_20,
        "xǁGARCHMǁ_variance_recursion__mutmut_21": xǁGARCHMǁ_variance_recursion__mutmut_21,
        "xǁGARCHMǁ_variance_recursion__mutmut_22": xǁGARCHMǁ_variance_recursion__mutmut_22,
        "xǁGARCHMǁ_variance_recursion__mutmut_23": xǁGARCHMǁ_variance_recursion__mutmut_23,
        "xǁGARCHMǁ_variance_recursion__mutmut_24": xǁGARCHMǁ_variance_recursion__mutmut_24,
        "xǁGARCHMǁ_variance_recursion__mutmut_25": xǁGARCHMǁ_variance_recursion__mutmut_25,
        "xǁGARCHMǁ_variance_recursion__mutmut_26": xǁGARCHMǁ_variance_recursion__mutmut_26,
        "xǁGARCHMǁ_variance_recursion__mutmut_27": xǁGARCHMǁ_variance_recursion__mutmut_27,
        "xǁGARCHMǁ_variance_recursion__mutmut_28": xǁGARCHMǁ_variance_recursion__mutmut_28,
        "xǁGARCHMǁ_variance_recursion__mutmut_29": xǁGARCHMǁ_variance_recursion__mutmut_29,
        "xǁGARCHMǁ_variance_recursion__mutmut_30": xǁGARCHMǁ_variance_recursion__mutmut_30,
        "xǁGARCHMǁ_variance_recursion__mutmut_31": xǁGARCHMǁ_variance_recursion__mutmut_31,
        "xǁGARCHMǁ_variance_recursion__mutmut_32": xǁGARCHMǁ_variance_recursion__mutmut_32,
        "xǁGARCHMǁ_variance_recursion__mutmut_33": xǁGARCHMǁ_variance_recursion__mutmut_33,
        "xǁGARCHMǁ_variance_recursion__mutmut_34": xǁGARCHMǁ_variance_recursion__mutmut_34,
        "xǁGARCHMǁ_variance_recursion__mutmut_35": xǁGARCHMǁ_variance_recursion__mutmut_35,
        "xǁGARCHMǁ_variance_recursion__mutmut_36": xǁGARCHMǁ_variance_recursion__mutmut_36,
        "xǁGARCHMǁ_variance_recursion__mutmut_37": xǁGARCHMǁ_variance_recursion__mutmut_37,
        "xǁGARCHMǁ_variance_recursion__mutmut_38": xǁGARCHMǁ_variance_recursion__mutmut_38,
        "xǁGARCHMǁ_variance_recursion__mutmut_39": xǁGARCHMǁ_variance_recursion__mutmut_39,
        "xǁGARCHMǁ_variance_recursion__mutmut_40": xǁGARCHMǁ_variance_recursion__mutmut_40,
        "xǁGARCHMǁ_variance_recursion__mutmut_41": xǁGARCHMǁ_variance_recursion__mutmut_41,
        "xǁGARCHMǁ_variance_recursion__mutmut_42": xǁGARCHMǁ_variance_recursion__mutmut_42,
        "xǁGARCHMǁ_variance_recursion__mutmut_43": xǁGARCHMǁ_variance_recursion__mutmut_43,
        "xǁGARCHMǁ_variance_recursion__mutmut_44": xǁGARCHMǁ_variance_recursion__mutmut_44,
        "xǁGARCHMǁ_variance_recursion__mutmut_45": xǁGARCHMǁ_variance_recursion__mutmut_45,
        "xǁGARCHMǁ_variance_recursion__mutmut_46": xǁGARCHMǁ_variance_recursion__mutmut_46,
        "xǁGARCHMǁ_variance_recursion__mutmut_47": xǁGARCHMǁ_variance_recursion__mutmut_47,
        "xǁGARCHMǁ_variance_recursion__mutmut_48": xǁGARCHMǁ_variance_recursion__mutmut_48,
    }
    xǁGARCHMǁ_variance_recursion__mutmut_orig.__name__ = "xǁGARCHMǁ_variance_recursion"

    def _garchm_joint_recursion(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        args = [params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁ_garchm_joint_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁ_garchm_joint_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = None
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[1]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = None
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[2 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 - self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 2 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = None
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 - self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[2 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q - self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 - self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 2 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = None

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[+1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-2]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = None
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = None
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(None)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = None

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(None)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(None):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = None
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(None):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = None
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 + i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t + 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 2 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag > 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 1:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] = alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] -= alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] / adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] * 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 3
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] = alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] -= alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] / backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(None):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = None
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 + j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t + 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 2 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] = betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] -= betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] / (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag > 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 1 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = None
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(None, 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], None)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(
                sigma2[t],
            )
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1.000000000001)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = None

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] + lam * self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam / self._risk_premium_function(sigma2[t])

        return sigma2, adj_resids

    def xǁGARCHMǁ_garchm_joint_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Joint forward pass computing sigma2 and adjusted residuals.

        In GARCH-M, eps_t = r_t - lambda*f(sigma2_t), and sigma2_t
        depends on eps_{t-1}. This computes both jointly.

        Returns
        -------
        tuple
            (sigma2, adjusted_resids)
        """
        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]
        lam = params[-1]

        nobs = len(self.endog)
        sigma2 = np.empty(nobs)
        adj_resids = np.empty(nobs)

        for t in range(nobs):
            sigma2[t] = omega
            for i in range(self.q):
                lag = t - 1 - i
                if lag >= 0:
                    sigma2[t] += alphas[i] * adj_resids[lag] ** 2
                else:
                    sigma2[t] += alphas[i] * backcast
            for j in range(self.p):
                lag = t - 1 - j
                sigma2[t] += betas[j] * (sigma2[lag] if lag >= 0 else backcast)
            sigma2[t] = max(sigma2[t], 1e-12)
            adj_resids[t] = self.endog[t] - lam * self._risk_premium_function(None)

        return sigma2, adj_resids

    xǁGARCHMǁ_garchm_joint_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_1": xǁGARCHMǁ_garchm_joint_recursion__mutmut_1,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_2": xǁGARCHMǁ_garchm_joint_recursion__mutmut_2,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_3": xǁGARCHMǁ_garchm_joint_recursion__mutmut_3,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_4": xǁGARCHMǁ_garchm_joint_recursion__mutmut_4,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_5": xǁGARCHMǁ_garchm_joint_recursion__mutmut_5,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_6": xǁGARCHMǁ_garchm_joint_recursion__mutmut_6,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_7": xǁGARCHMǁ_garchm_joint_recursion__mutmut_7,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_8": xǁGARCHMǁ_garchm_joint_recursion__mutmut_8,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_9": xǁGARCHMǁ_garchm_joint_recursion__mutmut_9,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_10": xǁGARCHMǁ_garchm_joint_recursion__mutmut_10,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_11": xǁGARCHMǁ_garchm_joint_recursion__mutmut_11,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_12": xǁGARCHMǁ_garchm_joint_recursion__mutmut_12,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_13": xǁGARCHMǁ_garchm_joint_recursion__mutmut_13,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_14": xǁGARCHMǁ_garchm_joint_recursion__mutmut_14,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_15": xǁGARCHMǁ_garchm_joint_recursion__mutmut_15,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_16": xǁGARCHMǁ_garchm_joint_recursion__mutmut_16,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_17": xǁGARCHMǁ_garchm_joint_recursion__mutmut_17,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_18": xǁGARCHMǁ_garchm_joint_recursion__mutmut_18,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_19": xǁGARCHMǁ_garchm_joint_recursion__mutmut_19,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_20": xǁGARCHMǁ_garchm_joint_recursion__mutmut_20,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_21": xǁGARCHMǁ_garchm_joint_recursion__mutmut_21,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_22": xǁGARCHMǁ_garchm_joint_recursion__mutmut_22,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_23": xǁGARCHMǁ_garchm_joint_recursion__mutmut_23,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_24": xǁGARCHMǁ_garchm_joint_recursion__mutmut_24,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_25": xǁGARCHMǁ_garchm_joint_recursion__mutmut_25,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_26": xǁGARCHMǁ_garchm_joint_recursion__mutmut_26,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_27": xǁGARCHMǁ_garchm_joint_recursion__mutmut_27,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_28": xǁGARCHMǁ_garchm_joint_recursion__mutmut_28,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_29": xǁGARCHMǁ_garchm_joint_recursion__mutmut_29,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_30": xǁGARCHMǁ_garchm_joint_recursion__mutmut_30,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_31": xǁGARCHMǁ_garchm_joint_recursion__mutmut_31,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_32": xǁGARCHMǁ_garchm_joint_recursion__mutmut_32,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_33": xǁGARCHMǁ_garchm_joint_recursion__mutmut_33,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_34": xǁGARCHMǁ_garchm_joint_recursion__mutmut_34,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_35": xǁGARCHMǁ_garchm_joint_recursion__mutmut_35,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_36": xǁGARCHMǁ_garchm_joint_recursion__mutmut_36,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_37": xǁGARCHMǁ_garchm_joint_recursion__mutmut_37,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_38": xǁGARCHMǁ_garchm_joint_recursion__mutmut_38,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_39": xǁGARCHMǁ_garchm_joint_recursion__mutmut_39,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_40": xǁGARCHMǁ_garchm_joint_recursion__mutmut_40,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_41": xǁGARCHMǁ_garchm_joint_recursion__mutmut_41,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_42": xǁGARCHMǁ_garchm_joint_recursion__mutmut_42,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_43": xǁGARCHMǁ_garchm_joint_recursion__mutmut_43,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_44": xǁGARCHMǁ_garchm_joint_recursion__mutmut_44,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_45": xǁGARCHMǁ_garchm_joint_recursion__mutmut_45,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_46": xǁGARCHMǁ_garchm_joint_recursion__mutmut_46,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_47": xǁGARCHMǁ_garchm_joint_recursion__mutmut_47,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_48": xǁGARCHMǁ_garchm_joint_recursion__mutmut_48,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_49": xǁGARCHMǁ_garchm_joint_recursion__mutmut_49,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_50": xǁGARCHMǁ_garchm_joint_recursion__mutmut_50,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_51": xǁGARCHMǁ_garchm_joint_recursion__mutmut_51,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_52": xǁGARCHMǁ_garchm_joint_recursion__mutmut_52,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_53": xǁGARCHMǁ_garchm_joint_recursion__mutmut_53,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_54": xǁGARCHMǁ_garchm_joint_recursion__mutmut_54,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_55": xǁGARCHMǁ_garchm_joint_recursion__mutmut_55,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_56": xǁGARCHMǁ_garchm_joint_recursion__mutmut_56,
        "xǁGARCHMǁ_garchm_joint_recursion__mutmut_57": xǁGARCHMǁ_garchm_joint_recursion__mutmut_57,
    }
    xǁGARCHMǁ_garchm_joint_recursion__mutmut_orig.__name__ = "xǁGARCHMǁ_garchm_joint_recursion"

    def loglike(self, params: NDArray[np.float64], backcast: float | None = None) -> float:
        args = [params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁloglike__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁloglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁloglike__mutmut_orig(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_1(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is not None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_2(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = None

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_3(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(None)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_4(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = None
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_5(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(None, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_6(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, None)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_7(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_8(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(
            params,
        )
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_9(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = None

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_10(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(None, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_11(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, None)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_12(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_13(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(
            sigma2,
        )

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_14(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1.000000000001)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_15(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_16(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(None):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_17(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(None)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_18(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return +1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_19(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -10000000001.0

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_20(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = None
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_21(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(None, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_22(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, None)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_23(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_24(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(
            adj_resids,
        )
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_25(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = None
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_26(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(None)
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_27(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(None))
        return total if np.isfinite(total) else -1e10

    def xǁGARCHMǁloglike__mutmut_28(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(None) else -1e10

    def xǁGARCHMǁloglike__mutmut_29(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else +1e10

    def xǁGARCHMǁloglike__mutmut_30(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> float:
        """Compute log-likelihood for GARCH-M.

        Uses joint forward pass where eps_t = r_t - lambda * f(sigma2_t).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        if not np.all(np.isfinite(sigma2)):
            return -1e10

        ll_per_obs = self.dist.loglikelihood(adj_resids, sigma2)
        total = float(np.sum(ll_per_obs))
        return total if np.isfinite(total) else -10000000001.0

    xǁGARCHMǁloglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁloglike__mutmut_1": xǁGARCHMǁloglike__mutmut_1,
        "xǁGARCHMǁloglike__mutmut_2": xǁGARCHMǁloglike__mutmut_2,
        "xǁGARCHMǁloglike__mutmut_3": xǁGARCHMǁloglike__mutmut_3,
        "xǁGARCHMǁloglike__mutmut_4": xǁGARCHMǁloglike__mutmut_4,
        "xǁGARCHMǁloglike__mutmut_5": xǁGARCHMǁloglike__mutmut_5,
        "xǁGARCHMǁloglike__mutmut_6": xǁGARCHMǁloglike__mutmut_6,
        "xǁGARCHMǁloglike__mutmut_7": xǁGARCHMǁloglike__mutmut_7,
        "xǁGARCHMǁloglike__mutmut_8": xǁGARCHMǁloglike__mutmut_8,
        "xǁGARCHMǁloglike__mutmut_9": xǁGARCHMǁloglike__mutmut_9,
        "xǁGARCHMǁloglike__mutmut_10": xǁGARCHMǁloglike__mutmut_10,
        "xǁGARCHMǁloglike__mutmut_11": xǁGARCHMǁloglike__mutmut_11,
        "xǁGARCHMǁloglike__mutmut_12": xǁGARCHMǁloglike__mutmut_12,
        "xǁGARCHMǁloglike__mutmut_13": xǁGARCHMǁloglike__mutmut_13,
        "xǁGARCHMǁloglike__mutmut_14": xǁGARCHMǁloglike__mutmut_14,
        "xǁGARCHMǁloglike__mutmut_15": xǁGARCHMǁloglike__mutmut_15,
        "xǁGARCHMǁloglike__mutmut_16": xǁGARCHMǁloglike__mutmut_16,
        "xǁGARCHMǁloglike__mutmut_17": xǁGARCHMǁloglike__mutmut_17,
        "xǁGARCHMǁloglike__mutmut_18": xǁGARCHMǁloglike__mutmut_18,
        "xǁGARCHMǁloglike__mutmut_19": xǁGARCHMǁloglike__mutmut_19,
        "xǁGARCHMǁloglike__mutmut_20": xǁGARCHMǁloglike__mutmut_20,
        "xǁGARCHMǁloglike__mutmut_21": xǁGARCHMǁloglike__mutmut_21,
        "xǁGARCHMǁloglike__mutmut_22": xǁGARCHMǁloglike__mutmut_22,
        "xǁGARCHMǁloglike__mutmut_23": xǁGARCHMǁloglike__mutmut_23,
        "xǁGARCHMǁloglike__mutmut_24": xǁGARCHMǁloglike__mutmut_24,
        "xǁGARCHMǁloglike__mutmut_25": xǁGARCHMǁloglike__mutmut_25,
        "xǁGARCHMǁloglike__mutmut_26": xǁGARCHMǁloglike__mutmut_26,
        "xǁGARCHMǁloglike__mutmut_27": xǁGARCHMǁloglike__mutmut_27,
        "xǁGARCHMǁloglike__mutmut_28": xǁGARCHMǁloglike__mutmut_28,
        "xǁGARCHMǁloglike__mutmut_29": xǁGARCHMǁloglike__mutmut_29,
        "xǁGARCHMǁloglike__mutmut_30": xǁGARCHMǁloglike__mutmut_30,
    }
    xǁGARCHMǁloglike__mutmut_orig.__name__ = "xǁGARCHMǁloglike"

    def loglike_per_obs(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        args = [params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁloglike_per_obs__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁloglike_per_obs__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁloglike_per_obs__mutmut_orig(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_1(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is not None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_2(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = None

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_3(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(None)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_4(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = None
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_5(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(None, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_6(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, None)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_7(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_8(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(
            params,
        )
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_9(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = None

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_10(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(None, 1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_11(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, None)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_12(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(1e-12)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_13(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(
            sigma2,
        )

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_14(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1.000000000001)

        return self.dist.loglikelihood(adj_resids, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_15(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(None, sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_16(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(adj_resids, None)

    def xǁGARCHMǁloglike_per_obs__mutmut_17(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(sigma2)

    def xǁGARCHMǁloglike_per_obs__mutmut_18(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood for GARCH-M."""
        if backcast is None:
            backcast = self._backcast(self.endog)

        sigma2, adj_resids = self._garchm_joint_recursion(params, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        return self.dist.loglikelihood(
            adj_resids,
        )

    xǁGARCHMǁloglike_per_obs__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁloglike_per_obs__mutmut_1": xǁGARCHMǁloglike_per_obs__mutmut_1,
        "xǁGARCHMǁloglike_per_obs__mutmut_2": xǁGARCHMǁloglike_per_obs__mutmut_2,
        "xǁGARCHMǁloglike_per_obs__mutmut_3": xǁGARCHMǁloglike_per_obs__mutmut_3,
        "xǁGARCHMǁloglike_per_obs__mutmut_4": xǁGARCHMǁloglike_per_obs__mutmut_4,
        "xǁGARCHMǁloglike_per_obs__mutmut_5": xǁGARCHMǁloglike_per_obs__mutmut_5,
        "xǁGARCHMǁloglike_per_obs__mutmut_6": xǁGARCHMǁloglike_per_obs__mutmut_6,
        "xǁGARCHMǁloglike_per_obs__mutmut_7": xǁGARCHMǁloglike_per_obs__mutmut_7,
        "xǁGARCHMǁloglike_per_obs__mutmut_8": xǁGARCHMǁloglike_per_obs__mutmut_8,
        "xǁGARCHMǁloglike_per_obs__mutmut_9": xǁGARCHMǁloglike_per_obs__mutmut_9,
        "xǁGARCHMǁloglike_per_obs__mutmut_10": xǁGARCHMǁloglike_per_obs__mutmut_10,
        "xǁGARCHMǁloglike_per_obs__mutmut_11": xǁGARCHMǁloglike_per_obs__mutmut_11,
        "xǁGARCHMǁloglike_per_obs__mutmut_12": xǁGARCHMǁloglike_per_obs__mutmut_12,
        "xǁGARCHMǁloglike_per_obs__mutmut_13": xǁGARCHMǁloglike_per_obs__mutmut_13,
        "xǁGARCHMǁloglike_per_obs__mutmut_14": xǁGARCHMǁloglike_per_obs__mutmut_14,
        "xǁGARCHMǁloglike_per_obs__mutmut_15": xǁGARCHMǁloglike_per_obs__mutmut_15,
        "xǁGARCHMǁloglike_per_obs__mutmut_16": xǁGARCHMǁloglike_per_obs__mutmut_16,
        "xǁGARCHMǁloglike_per_obs__mutmut_17": xǁGARCHMǁloglike_per_obs__mutmut_17,
        "xǁGARCHMǁloglike_per_obs__mutmut_18": xǁGARCHMǁloglike_per_obs__mutmut_18,
    }
    xǁGARCHMǁloglike_per_obs__mutmut_orig.__name__ = "xǁGARCHMǁloglike_per_obs"

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        args = [eps, sigma2_prev, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁ_one_step_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁ_one_step_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁ_one_step_variance__mutmut_orig(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_1(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = None
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_2(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[1]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_3(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = None
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_4(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[2]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_5(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = None
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_6(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 - self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_7(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[2 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_8(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = None
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_9(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 - beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_10(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega - alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_11(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha / eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_12(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps * 2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_13(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**3 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_14(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta / sigma2_prev
        return float(max(sigma2, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_15(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(None)

    def xǁGARCHMǁ_one_step_variance__mutmut_16(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(None, 1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_17(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, None))

    def xǁGARCHMǁ_one_step_variance__mutmut_18(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(1e-12))

    def xǁGARCHMǁ_one_step_variance__mutmut_19(
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

    def xǁGARCHMǁ_one_step_variance__mutmut_20(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1.000000000001))

    xǁGARCHMǁ_one_step_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁ_one_step_variance__mutmut_1": xǁGARCHMǁ_one_step_variance__mutmut_1,
        "xǁGARCHMǁ_one_step_variance__mutmut_2": xǁGARCHMǁ_one_step_variance__mutmut_2,
        "xǁGARCHMǁ_one_step_variance__mutmut_3": xǁGARCHMǁ_one_step_variance__mutmut_3,
        "xǁGARCHMǁ_one_step_variance__mutmut_4": xǁGARCHMǁ_one_step_variance__mutmut_4,
        "xǁGARCHMǁ_one_step_variance__mutmut_5": xǁGARCHMǁ_one_step_variance__mutmut_5,
        "xǁGARCHMǁ_one_step_variance__mutmut_6": xǁGARCHMǁ_one_step_variance__mutmut_6,
        "xǁGARCHMǁ_one_step_variance__mutmut_7": xǁGARCHMǁ_one_step_variance__mutmut_7,
        "xǁGARCHMǁ_one_step_variance__mutmut_8": xǁGARCHMǁ_one_step_variance__mutmut_8,
        "xǁGARCHMǁ_one_step_variance__mutmut_9": xǁGARCHMǁ_one_step_variance__mutmut_9,
        "xǁGARCHMǁ_one_step_variance__mutmut_10": xǁGARCHMǁ_one_step_variance__mutmut_10,
        "xǁGARCHMǁ_one_step_variance__mutmut_11": xǁGARCHMǁ_one_step_variance__mutmut_11,
        "xǁGARCHMǁ_one_step_variance__mutmut_12": xǁGARCHMǁ_one_step_variance__mutmut_12,
        "xǁGARCHMǁ_one_step_variance__mutmut_13": xǁGARCHMǁ_one_step_variance__mutmut_13,
        "xǁGARCHMǁ_one_step_variance__mutmut_14": xǁGARCHMǁ_one_step_variance__mutmut_14,
        "xǁGARCHMǁ_one_step_variance__mutmut_15": xǁGARCHMǁ_one_step_variance__mutmut_15,
        "xǁGARCHMǁ_one_step_variance__mutmut_16": xǁGARCHMǁ_one_step_variance__mutmut_16,
        "xǁGARCHMǁ_one_step_variance__mutmut_17": xǁGARCHMǁ_one_step_variance__mutmut_17,
        "xǁGARCHMǁ_one_step_variance__mutmut_18": xǁGARCHMǁ_one_step_variance__mutmut_18,
        "xǁGARCHMǁ_one_step_variance__mutmut_19": xǁGARCHMǁ_one_step_variance__mutmut_19,
        "xǁGARCHMǁ_one_step_variance__mutmut_20": xǁGARCHMǁ_one_step_variance__mutmut_20,
    }
    xǁGARCHMǁ_one_step_variance__mutmut_orig.__name__ = "xǁGARCHMǁ_one_step_variance"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: [omega, alpha_1..q, beta_1..p, lambda]."""
        var = np.var(self.endog)
        omega = var * 0.01
        alphas = np.full(self.q, 0.05)
        betas = np.full(self.p, 0.90)
        lam = np.array([0.01])
        return np.concatenate([[omega], alphas, betas, lam])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["omega"]
        names += [f"alpha[{i + 1}]" for i in range(self.q)]
        names += [f"beta[{i + 1}]" for i in range(self.p)]
        names += ["lambda"]
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [unconstrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁtransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁtransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁtransform_params__mutmut_orig(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_1(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = None
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_2(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = None
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_3(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[1] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_4(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(None)
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_5(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(None, -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_6(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], None, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_7(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, None))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_8(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(-50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_9(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_10(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(
            np.clip(
                unconstrained[0],
                -50,
            )
        )
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_11(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[1], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_12(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], +50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_13(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -51, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_14(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 51))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_15(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(None):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_16(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = None
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_17(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 - i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_18(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[2 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_19(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(None)
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_20(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(None, -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_21(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], None, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_22(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, None))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_23(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(-50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_24(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_25(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(
                np.clip(
                    unconstrained[1 + i],
                    -50,
                )
            )
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_26(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 - i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_27(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[2 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_28(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], +50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_29(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -51, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_30(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 51))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_31(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(None):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_32(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = None
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_33(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q - j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_34(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 - self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_35(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 2 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_36(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = None
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_37(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(None)
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_38(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(None, -50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_39(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], None, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_40(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, None))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_41(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(-50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_42(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_43(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(
                np.clip(
                    unconstrained[idx],
                    -50,
                )
            )
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_44(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], +50, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_45(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -51, 50))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    def xǁGARCHMǁtransform_params__mutmut_46(
        self, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained."""
        constrained = unconstrained.copy()
        # omega > 0 (clip to prevent overflow)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50, 50))
        # alphas >= 0
        for i in range(self.q):
            constrained[1 + i] = np.exp(np.clip(unconstrained[1 + i], -50, 50))
        # betas >= 0
        for j in range(self.p):
            idx = 1 + self.q + j
            constrained[idx] = np.exp(np.clip(unconstrained[idx], -50, 51))
        # lambda: unconstrained (can be positive or negative)
        return constrained

    xǁGARCHMǁtransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁtransform_params__mutmut_1": xǁGARCHMǁtransform_params__mutmut_1,
        "xǁGARCHMǁtransform_params__mutmut_2": xǁGARCHMǁtransform_params__mutmut_2,
        "xǁGARCHMǁtransform_params__mutmut_3": xǁGARCHMǁtransform_params__mutmut_3,
        "xǁGARCHMǁtransform_params__mutmut_4": xǁGARCHMǁtransform_params__mutmut_4,
        "xǁGARCHMǁtransform_params__mutmut_5": xǁGARCHMǁtransform_params__mutmut_5,
        "xǁGARCHMǁtransform_params__mutmut_6": xǁGARCHMǁtransform_params__mutmut_6,
        "xǁGARCHMǁtransform_params__mutmut_7": xǁGARCHMǁtransform_params__mutmut_7,
        "xǁGARCHMǁtransform_params__mutmut_8": xǁGARCHMǁtransform_params__mutmut_8,
        "xǁGARCHMǁtransform_params__mutmut_9": xǁGARCHMǁtransform_params__mutmut_9,
        "xǁGARCHMǁtransform_params__mutmut_10": xǁGARCHMǁtransform_params__mutmut_10,
        "xǁGARCHMǁtransform_params__mutmut_11": xǁGARCHMǁtransform_params__mutmut_11,
        "xǁGARCHMǁtransform_params__mutmut_12": xǁGARCHMǁtransform_params__mutmut_12,
        "xǁGARCHMǁtransform_params__mutmut_13": xǁGARCHMǁtransform_params__mutmut_13,
        "xǁGARCHMǁtransform_params__mutmut_14": xǁGARCHMǁtransform_params__mutmut_14,
        "xǁGARCHMǁtransform_params__mutmut_15": xǁGARCHMǁtransform_params__mutmut_15,
        "xǁGARCHMǁtransform_params__mutmut_16": xǁGARCHMǁtransform_params__mutmut_16,
        "xǁGARCHMǁtransform_params__mutmut_17": xǁGARCHMǁtransform_params__mutmut_17,
        "xǁGARCHMǁtransform_params__mutmut_18": xǁGARCHMǁtransform_params__mutmut_18,
        "xǁGARCHMǁtransform_params__mutmut_19": xǁGARCHMǁtransform_params__mutmut_19,
        "xǁGARCHMǁtransform_params__mutmut_20": xǁGARCHMǁtransform_params__mutmut_20,
        "xǁGARCHMǁtransform_params__mutmut_21": xǁGARCHMǁtransform_params__mutmut_21,
        "xǁGARCHMǁtransform_params__mutmut_22": xǁGARCHMǁtransform_params__mutmut_22,
        "xǁGARCHMǁtransform_params__mutmut_23": xǁGARCHMǁtransform_params__mutmut_23,
        "xǁGARCHMǁtransform_params__mutmut_24": xǁGARCHMǁtransform_params__mutmut_24,
        "xǁGARCHMǁtransform_params__mutmut_25": xǁGARCHMǁtransform_params__mutmut_25,
        "xǁGARCHMǁtransform_params__mutmut_26": xǁGARCHMǁtransform_params__mutmut_26,
        "xǁGARCHMǁtransform_params__mutmut_27": xǁGARCHMǁtransform_params__mutmut_27,
        "xǁGARCHMǁtransform_params__mutmut_28": xǁGARCHMǁtransform_params__mutmut_28,
        "xǁGARCHMǁtransform_params__mutmut_29": xǁGARCHMǁtransform_params__mutmut_29,
        "xǁGARCHMǁtransform_params__mutmut_30": xǁGARCHMǁtransform_params__mutmut_30,
        "xǁGARCHMǁtransform_params__mutmut_31": xǁGARCHMǁtransform_params__mutmut_31,
        "xǁGARCHMǁtransform_params__mutmut_32": xǁGARCHMǁtransform_params__mutmut_32,
        "xǁGARCHMǁtransform_params__mutmut_33": xǁGARCHMǁtransform_params__mutmut_33,
        "xǁGARCHMǁtransform_params__mutmut_34": xǁGARCHMǁtransform_params__mutmut_34,
        "xǁGARCHMǁtransform_params__mutmut_35": xǁGARCHMǁtransform_params__mutmut_35,
        "xǁGARCHMǁtransform_params__mutmut_36": xǁGARCHMǁtransform_params__mutmut_36,
        "xǁGARCHMǁtransform_params__mutmut_37": xǁGARCHMǁtransform_params__mutmut_37,
        "xǁGARCHMǁtransform_params__mutmut_38": xǁGARCHMǁtransform_params__mutmut_38,
        "xǁGARCHMǁtransform_params__mutmut_39": xǁGARCHMǁtransform_params__mutmut_39,
        "xǁGARCHMǁtransform_params__mutmut_40": xǁGARCHMǁtransform_params__mutmut_40,
        "xǁGARCHMǁtransform_params__mutmut_41": xǁGARCHMǁtransform_params__mutmut_41,
        "xǁGARCHMǁtransform_params__mutmut_42": xǁGARCHMǁtransform_params__mutmut_42,
        "xǁGARCHMǁtransform_params__mutmut_43": xǁGARCHMǁtransform_params__mutmut_43,
        "xǁGARCHMǁtransform_params__mutmut_44": xǁGARCHMǁtransform_params__mutmut_44,
        "xǁGARCHMǁtransform_params__mutmut_45": xǁGARCHMǁtransform_params__mutmut_45,
        "xǁGARCHMǁtransform_params__mutmut_46": xǁGARCHMǁtransform_params__mutmut_46,
    }
    xǁGARCHMǁtransform_params__mutmut_orig.__name__ = "xǁGARCHMǁtransform_params"

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        args = [constrained]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁuntransform_params__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁuntransform_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁuntransform_params__mutmut_orig(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_1(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = None
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_2(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = None
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_3(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[1] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_4(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(None)
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_5(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(None, 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_6(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], None))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_7(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_8(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(
            max(
                constrained[0],
            )
        )
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_9(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[1], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_10(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1.000000000001))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_11(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(None):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_12(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = None
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_13(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 - i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_14(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[2 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_15(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(None)
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_16(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(None, 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_17(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], None))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_18(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_19(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(
                max(
                    constrained[1 + i],
                )
            )
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_20(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 - i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_21(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[2 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_22(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1.000000000001))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_23(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(None):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_24(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = None
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_25(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q - j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_26(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 - self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_27(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 2 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_28(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = None
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_29(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(None)
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_30(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(None, 1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_31(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], None))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_32(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(1e-12))
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_33(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(
                max(
                    constrained[idx],
                )
            )
        # lambda stays as-is
        return unconstrained

    def xǁGARCHMǁuntransform_params__mutmut_34(
        self, constrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained."""
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-12))
        for i in range(self.q):
            unconstrained[1 + i] = np.log(max(constrained[1 + i], 1e-12))
        for j in range(self.p):
            idx = 1 + self.q + j
            unconstrained[idx] = np.log(max(constrained[idx], 1.000000000001))
        # lambda stays as-is
        return unconstrained

    xǁGARCHMǁuntransform_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁuntransform_params__mutmut_1": xǁGARCHMǁuntransform_params__mutmut_1,
        "xǁGARCHMǁuntransform_params__mutmut_2": xǁGARCHMǁuntransform_params__mutmut_2,
        "xǁGARCHMǁuntransform_params__mutmut_3": xǁGARCHMǁuntransform_params__mutmut_3,
        "xǁGARCHMǁuntransform_params__mutmut_4": xǁGARCHMǁuntransform_params__mutmut_4,
        "xǁGARCHMǁuntransform_params__mutmut_5": xǁGARCHMǁuntransform_params__mutmut_5,
        "xǁGARCHMǁuntransform_params__mutmut_6": xǁGARCHMǁuntransform_params__mutmut_6,
        "xǁGARCHMǁuntransform_params__mutmut_7": xǁGARCHMǁuntransform_params__mutmut_7,
        "xǁGARCHMǁuntransform_params__mutmut_8": xǁGARCHMǁuntransform_params__mutmut_8,
        "xǁGARCHMǁuntransform_params__mutmut_9": xǁGARCHMǁuntransform_params__mutmut_9,
        "xǁGARCHMǁuntransform_params__mutmut_10": xǁGARCHMǁuntransform_params__mutmut_10,
        "xǁGARCHMǁuntransform_params__mutmut_11": xǁGARCHMǁuntransform_params__mutmut_11,
        "xǁGARCHMǁuntransform_params__mutmut_12": xǁGARCHMǁuntransform_params__mutmut_12,
        "xǁGARCHMǁuntransform_params__mutmut_13": xǁGARCHMǁuntransform_params__mutmut_13,
        "xǁGARCHMǁuntransform_params__mutmut_14": xǁGARCHMǁuntransform_params__mutmut_14,
        "xǁGARCHMǁuntransform_params__mutmut_15": xǁGARCHMǁuntransform_params__mutmut_15,
        "xǁGARCHMǁuntransform_params__mutmut_16": xǁGARCHMǁuntransform_params__mutmut_16,
        "xǁGARCHMǁuntransform_params__mutmut_17": xǁGARCHMǁuntransform_params__mutmut_17,
        "xǁGARCHMǁuntransform_params__mutmut_18": xǁGARCHMǁuntransform_params__mutmut_18,
        "xǁGARCHMǁuntransform_params__mutmut_19": xǁGARCHMǁuntransform_params__mutmut_19,
        "xǁGARCHMǁuntransform_params__mutmut_20": xǁGARCHMǁuntransform_params__mutmut_20,
        "xǁGARCHMǁuntransform_params__mutmut_21": xǁGARCHMǁuntransform_params__mutmut_21,
        "xǁGARCHMǁuntransform_params__mutmut_22": xǁGARCHMǁuntransform_params__mutmut_22,
        "xǁGARCHMǁuntransform_params__mutmut_23": xǁGARCHMǁuntransform_params__mutmut_23,
        "xǁGARCHMǁuntransform_params__mutmut_24": xǁGARCHMǁuntransform_params__mutmut_24,
        "xǁGARCHMǁuntransform_params__mutmut_25": xǁGARCHMǁuntransform_params__mutmut_25,
        "xǁGARCHMǁuntransform_params__mutmut_26": xǁGARCHMǁuntransform_params__mutmut_26,
        "xǁGARCHMǁuntransform_params__mutmut_27": xǁGARCHMǁuntransform_params__mutmut_27,
        "xǁGARCHMǁuntransform_params__mutmut_28": xǁGARCHMǁuntransform_params__mutmut_28,
        "xǁGARCHMǁuntransform_params__mutmut_29": xǁGARCHMǁuntransform_params__mutmut_29,
        "xǁGARCHMǁuntransform_params__mutmut_30": xǁGARCHMǁuntransform_params__mutmut_30,
        "xǁGARCHMǁuntransform_params__mutmut_31": xǁGARCHMǁuntransform_params__mutmut_31,
        "xǁGARCHMǁuntransform_params__mutmut_32": xǁGARCHMǁuntransform_params__mutmut_32,
        "xǁGARCHMǁuntransform_params__mutmut_33": xǁGARCHMǁuntransform_params__mutmut_33,
        "xǁGARCHMǁuntransform_params__mutmut_34": xǁGARCHMǁuntransform_params__mutmut_34,
    }
    xǁGARCHMǁuntransform_params__mutmut_orig.__name__ = "xǁGARCHMǁuntransform_params"

    def bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHMǁbounds__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHMǁbounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHMǁbounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = None
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append(None)  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1.000000000001, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(None):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_5(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append(None)  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_6(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((1.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_7(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(None):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_8(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append(None)  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_9(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((1.0, np.inf))  # betas
        bnds.append((-np.inf, np.inf))  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_10(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append(None)  # lambda
        return bnds

    def xǁGARCHMǁbounds__mutmut_11(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        bnds.append((1e-12, np.inf))  # omega
        for _ in range(self.q):
            bnds.append((0.0, np.inf))  # alphas
        for _ in range(self.p):
            bnds.append((0.0, np.inf))  # betas
        bnds.append((+np.inf, np.inf))  # lambda
        return bnds

    xǁGARCHMǁbounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHMǁbounds__mutmut_1": xǁGARCHMǁbounds__mutmut_1,
        "xǁGARCHMǁbounds__mutmut_2": xǁGARCHMǁbounds__mutmut_2,
        "xǁGARCHMǁbounds__mutmut_3": xǁGARCHMǁbounds__mutmut_3,
        "xǁGARCHMǁbounds__mutmut_4": xǁGARCHMǁbounds__mutmut_4,
        "xǁGARCHMǁbounds__mutmut_5": xǁGARCHMǁbounds__mutmut_5,
        "xǁGARCHMǁbounds__mutmut_6": xǁGARCHMǁbounds__mutmut_6,
        "xǁGARCHMǁbounds__mutmut_7": xǁGARCHMǁbounds__mutmut_7,
        "xǁGARCHMǁbounds__mutmut_8": xǁGARCHMǁbounds__mutmut_8,
        "xǁGARCHMǁbounds__mutmut_9": xǁGARCHMǁbounds__mutmut_9,
        "xǁGARCHMǁbounds__mutmut_10": xǁGARCHMǁbounds__mutmut_10,
        "xǁGARCHMǁbounds__mutmut_11": xǁGARCHMǁbounds__mutmut_11,
    }
    xǁGARCHMǁbounds__mutmut_orig.__name__ = "xǁGARCHMǁbounds"

    @property
    def num_params(self) -> int:
        """Number of parameters: omega + q alphas + p betas + lambda."""
        return 1 + self.q + self.p + 1
