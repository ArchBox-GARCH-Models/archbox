"""EWMA / RiskMetrics volatility model.

The Exponentially Weighted Moving Average model from JP Morgan's
RiskMetrics (1996). Equivalent to IGARCH(1,1) with omega=0.

Parameters:
    lambda = 0.94 (daily) or 0.97 (monthly)

References
----------
- JP Morgan (1996). RiskMetrics Technical Document. 4th ed.
- Francq, C. & Zakoian, J.-M. (2019). GARCH Models. 2nd ed. Wiley. Cap. 2.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Annotated, ClassVar

import numpy as np
from numpy.typing import NDArray

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


@dataclass
class EWMAResult:
    """Container for EWMA fit results.

    Attributes
    ----------
    conditional_volatility : NDArray[np.float64]
        Conditional volatility series sigma_t.
    conditional_variance : NDArray[np.float64]
        Conditional variance series sigma^2_t.
    returns : NDArray[np.float64]
        The input return series.
    lam : float
        The decay factor lambda.
    resids : NDArray[np.float64]
        Residuals (same as returns for zero-mean model).
    mu : float
        Mean (always 0 for EWMA).
    params : NDArray[np.float64]
        Parameters [omega=0, alpha=1-lambda, beta=lambda].
    p : int
        GARCH order (always 1).
    q : int
        ARCH order (always 1).
    """

    conditional_volatility: NDArray[np.float64]
    conditional_variance: NDArray[np.float64]
    returns: NDArray[np.float64]
    lam: float
    resids: NDArray[np.float64] = field(init=False)
    mu: float = 0.0
    params: NDArray[np.float64] = field(init=False)
    p: int = 1
    q: int = 1

    def __post_init__(self) -> None:
        """Compute derived attributes after dataclass initialization."""
        self.resids = self.returns.copy()
        self.params = np.array([0.0, 1.0 - self.lam, self.lam])


class EWMA:
    """EWMA / RiskMetrics volatility model.

    Parameters
    ----------
    returns : array-like
        Time series of returns (1D).
    lam : float
        Decay factor lambda. Default is 0.94 (daily).
        Use 0.97 for monthly data.

    Attributes
    ----------
    returns : NDArray[np.float64]
        Returns array.
    lam : float
        Decay factor.
    """

    def __init__(self, returns: object, lam: float = 0.94) -> None:
        args = [returns, lam]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEWMAǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁEWMAǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEWMAǁ__init____mutmut_orig(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_1(self, returns: object, lam: float = 1.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_2(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = None
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_3(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(None, dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_4(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=None).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_5(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_6(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(
            returns,
        ).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_7(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_8(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 1 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_9(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 <= lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_10(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam <= 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_11(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam < 2:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_12(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = None
            raise ValueError(msg)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_13(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(None)
        self.lam = lam

    def xǁEWMAǁ__init____mutmut_14(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = None

    xǁEWMAǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEWMAǁ__init____mutmut_1": xǁEWMAǁ__init____mutmut_1,
        "xǁEWMAǁ__init____mutmut_2": xǁEWMAǁ__init____mutmut_2,
        "xǁEWMAǁ__init____mutmut_3": xǁEWMAǁ__init____mutmut_3,
        "xǁEWMAǁ__init____mutmut_4": xǁEWMAǁ__init____mutmut_4,
        "xǁEWMAǁ__init____mutmut_5": xǁEWMAǁ__init____mutmut_5,
        "xǁEWMAǁ__init____mutmut_6": xǁEWMAǁ__init____mutmut_6,
        "xǁEWMAǁ__init____mutmut_7": xǁEWMAǁ__init____mutmut_7,
        "xǁEWMAǁ__init____mutmut_8": xǁEWMAǁ__init____mutmut_8,
        "xǁEWMAǁ__init____mutmut_9": xǁEWMAǁ__init____mutmut_9,
        "xǁEWMAǁ__init____mutmut_10": xǁEWMAǁ__init____mutmut_10,
        "xǁEWMAǁ__init____mutmut_11": xǁEWMAǁ__init____mutmut_11,
        "xǁEWMAǁ__init____mutmut_12": xǁEWMAǁ__init____mutmut_12,
        "xǁEWMAǁ__init____mutmut_13": xǁEWMAǁ__init____mutmut_13,
        "xǁEWMAǁ__init____mutmut_14": xǁEWMAǁ__init____mutmut_14,
    }
    xǁEWMAǁ__init____mutmut_orig.__name__ = "xǁEWMAǁ__init__"

    def fit(self) -> EWMAResult:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEWMAǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁEWMAǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEWMAǁfit__mutmut_orig(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_1(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = None
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_2(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = None

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_3(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(None)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_4(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = None
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_5(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(None, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_6(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, None)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_7(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_8(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(
            25,
        )
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_9(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(26, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_10(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = None
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_11(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[1] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_12(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(None)
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_13(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[1] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_14(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] <= 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_15(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1.000000000001:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_16(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = None

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_17(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[1] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_18(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1.000001

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_19(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(None, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_20(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, None):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_21(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_22(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(
            1,
        ):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_23(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(2, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_24(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = None

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_25(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] - (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_26(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam / sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_27(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t + 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_28(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 2] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_29(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) / self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_30(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 + self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_31(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (2 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_32(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] * 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_33(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t + 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_34(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 2] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_35(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 3

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_36(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = None

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_37(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(None)

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_38(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(None, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_39(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, None))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_40(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_41(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(
            np.maximum(
                sigma2,
            )
        )

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_42(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1.000000000001))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_43(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=None,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_44(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=None,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_45(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=None,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_46(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=None,
        )

    def xǁEWMAǁfit__mutmut_47(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_48(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            returns=self.returns,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_49(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            lam=self.lam,
        )

    def xǁEWMAǁfit__mutmut_50(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
        )

    xǁEWMAǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEWMAǁfit__mutmut_1": xǁEWMAǁfit__mutmut_1,
        "xǁEWMAǁfit__mutmut_2": xǁEWMAǁfit__mutmut_2,
        "xǁEWMAǁfit__mutmut_3": xǁEWMAǁfit__mutmut_3,
        "xǁEWMAǁfit__mutmut_4": xǁEWMAǁfit__mutmut_4,
        "xǁEWMAǁfit__mutmut_5": xǁEWMAǁfit__mutmut_5,
        "xǁEWMAǁfit__mutmut_6": xǁEWMAǁfit__mutmut_6,
        "xǁEWMAǁfit__mutmut_7": xǁEWMAǁfit__mutmut_7,
        "xǁEWMAǁfit__mutmut_8": xǁEWMAǁfit__mutmut_8,
        "xǁEWMAǁfit__mutmut_9": xǁEWMAǁfit__mutmut_9,
        "xǁEWMAǁfit__mutmut_10": xǁEWMAǁfit__mutmut_10,
        "xǁEWMAǁfit__mutmut_11": xǁEWMAǁfit__mutmut_11,
        "xǁEWMAǁfit__mutmut_12": xǁEWMAǁfit__mutmut_12,
        "xǁEWMAǁfit__mutmut_13": xǁEWMAǁfit__mutmut_13,
        "xǁEWMAǁfit__mutmut_14": xǁEWMAǁfit__mutmut_14,
        "xǁEWMAǁfit__mutmut_15": xǁEWMAǁfit__mutmut_15,
        "xǁEWMAǁfit__mutmut_16": xǁEWMAǁfit__mutmut_16,
        "xǁEWMAǁfit__mutmut_17": xǁEWMAǁfit__mutmut_17,
        "xǁEWMAǁfit__mutmut_18": xǁEWMAǁfit__mutmut_18,
        "xǁEWMAǁfit__mutmut_19": xǁEWMAǁfit__mutmut_19,
        "xǁEWMAǁfit__mutmut_20": xǁEWMAǁfit__mutmut_20,
        "xǁEWMAǁfit__mutmut_21": xǁEWMAǁfit__mutmut_21,
        "xǁEWMAǁfit__mutmut_22": xǁEWMAǁfit__mutmut_22,
        "xǁEWMAǁfit__mutmut_23": xǁEWMAǁfit__mutmut_23,
        "xǁEWMAǁfit__mutmut_24": xǁEWMAǁfit__mutmut_24,
        "xǁEWMAǁfit__mutmut_25": xǁEWMAǁfit__mutmut_25,
        "xǁEWMAǁfit__mutmut_26": xǁEWMAǁfit__mutmut_26,
        "xǁEWMAǁfit__mutmut_27": xǁEWMAǁfit__mutmut_27,
        "xǁEWMAǁfit__mutmut_28": xǁEWMAǁfit__mutmut_28,
        "xǁEWMAǁfit__mutmut_29": xǁEWMAǁfit__mutmut_29,
        "xǁEWMAǁfit__mutmut_30": xǁEWMAǁfit__mutmut_30,
        "xǁEWMAǁfit__mutmut_31": xǁEWMAǁfit__mutmut_31,
        "xǁEWMAǁfit__mutmut_32": xǁEWMAǁfit__mutmut_32,
        "xǁEWMAǁfit__mutmut_33": xǁEWMAǁfit__mutmut_33,
        "xǁEWMAǁfit__mutmut_34": xǁEWMAǁfit__mutmut_34,
        "xǁEWMAǁfit__mutmut_35": xǁEWMAǁfit__mutmut_35,
        "xǁEWMAǁfit__mutmut_36": xǁEWMAǁfit__mutmut_36,
        "xǁEWMAǁfit__mutmut_37": xǁEWMAǁfit__mutmut_37,
        "xǁEWMAǁfit__mutmut_38": xǁEWMAǁfit__mutmut_38,
        "xǁEWMAǁfit__mutmut_39": xǁEWMAǁfit__mutmut_39,
        "xǁEWMAǁfit__mutmut_40": xǁEWMAǁfit__mutmut_40,
        "xǁEWMAǁfit__mutmut_41": xǁEWMAǁfit__mutmut_41,
        "xǁEWMAǁfit__mutmut_42": xǁEWMAǁfit__mutmut_42,
        "xǁEWMAǁfit__mutmut_43": xǁEWMAǁfit__mutmut_43,
        "xǁEWMAǁfit__mutmut_44": xǁEWMAǁfit__mutmut_44,
        "xǁEWMAǁfit__mutmut_45": xǁEWMAǁfit__mutmut_45,
        "xǁEWMAǁfit__mutmut_46": xǁEWMAǁfit__mutmut_46,
        "xǁEWMAǁfit__mutmut_47": xǁEWMAǁfit__mutmut_47,
        "xǁEWMAǁfit__mutmut_48": xǁEWMAǁfit__mutmut_48,
        "xǁEWMAǁfit__mutmut_49": xǁEWMAǁfit__mutmut_49,
        "xǁEWMAǁfit__mutmut_50": xǁEWMAǁfit__mutmut_50,
    }
    xǁEWMAǁfit__mutmut_orig.__name__ = "xǁEWMAǁfit"

    def covariance(self, returns_matrix: object) -> NDArray[np.float64]:
        args = [returns_matrix]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁEWMAǁcovariance__mutmut_orig"),
            object.__getattribute__(self, "xǁEWMAǁcovariance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁEWMAǁcovariance__mutmut_orig(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_1(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = None
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_2(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(None, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_3(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=None)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_4(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_5(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(
            returns_matrix,
        )
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_6(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim == 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_7(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 3:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_8(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = None
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_9(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(None)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_10(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = None
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_11(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = None

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_12(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty(None)

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_13(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = None
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_14(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(None, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_15(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, None)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_16(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_17(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(
            25,
        )
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_18(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(26, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_19(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = None
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_20(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[1] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_21(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(None)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_22(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(None):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_23(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(None)):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_24(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[1])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_25(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = None

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_26(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[1] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_27(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) / np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_28(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(None) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_29(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(None)

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_30(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(None, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_31(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, None):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_32(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_33(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(
            1,
        ):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_34(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(2, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_35(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = None  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_36(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t + 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_37(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 2 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_38(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = None  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_39(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = None

        return h_cov

    def xǁEWMAǁcovariance__mutmut_40(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] - (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_41(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam / h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_42(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t + 1] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_43(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 2] + (1 - self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_44(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) / outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_45(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 + self.lam) * outer

        return h_cov

    def xǁEWMAǁcovariance__mutmut_46(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (2 - self.lam) * outer

        return h_cov

    xǁEWMAǁcovariance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁEWMAǁcovariance__mutmut_1": xǁEWMAǁcovariance__mutmut_1,
        "xǁEWMAǁcovariance__mutmut_2": xǁEWMAǁcovariance__mutmut_2,
        "xǁEWMAǁcovariance__mutmut_3": xǁEWMAǁcovariance__mutmut_3,
        "xǁEWMAǁcovariance__mutmut_4": xǁEWMAǁcovariance__mutmut_4,
        "xǁEWMAǁcovariance__mutmut_5": xǁEWMAǁcovariance__mutmut_5,
        "xǁEWMAǁcovariance__mutmut_6": xǁEWMAǁcovariance__mutmut_6,
        "xǁEWMAǁcovariance__mutmut_7": xǁEWMAǁcovariance__mutmut_7,
        "xǁEWMAǁcovariance__mutmut_8": xǁEWMAǁcovariance__mutmut_8,
        "xǁEWMAǁcovariance__mutmut_9": xǁEWMAǁcovariance__mutmut_9,
        "xǁEWMAǁcovariance__mutmut_10": xǁEWMAǁcovariance__mutmut_10,
        "xǁEWMAǁcovariance__mutmut_11": xǁEWMAǁcovariance__mutmut_11,
        "xǁEWMAǁcovariance__mutmut_12": xǁEWMAǁcovariance__mutmut_12,
        "xǁEWMAǁcovariance__mutmut_13": xǁEWMAǁcovariance__mutmut_13,
        "xǁEWMAǁcovariance__mutmut_14": xǁEWMAǁcovariance__mutmut_14,
        "xǁEWMAǁcovariance__mutmut_15": xǁEWMAǁcovariance__mutmut_15,
        "xǁEWMAǁcovariance__mutmut_16": xǁEWMAǁcovariance__mutmut_16,
        "xǁEWMAǁcovariance__mutmut_17": xǁEWMAǁcovariance__mutmut_17,
        "xǁEWMAǁcovariance__mutmut_18": xǁEWMAǁcovariance__mutmut_18,
        "xǁEWMAǁcovariance__mutmut_19": xǁEWMAǁcovariance__mutmut_19,
        "xǁEWMAǁcovariance__mutmut_20": xǁEWMAǁcovariance__mutmut_20,
        "xǁEWMAǁcovariance__mutmut_21": xǁEWMAǁcovariance__mutmut_21,
        "xǁEWMAǁcovariance__mutmut_22": xǁEWMAǁcovariance__mutmut_22,
        "xǁEWMAǁcovariance__mutmut_23": xǁEWMAǁcovariance__mutmut_23,
        "xǁEWMAǁcovariance__mutmut_24": xǁEWMAǁcovariance__mutmut_24,
        "xǁEWMAǁcovariance__mutmut_25": xǁEWMAǁcovariance__mutmut_25,
        "xǁEWMAǁcovariance__mutmut_26": xǁEWMAǁcovariance__mutmut_26,
        "xǁEWMAǁcovariance__mutmut_27": xǁEWMAǁcovariance__mutmut_27,
        "xǁEWMAǁcovariance__mutmut_28": xǁEWMAǁcovariance__mutmut_28,
        "xǁEWMAǁcovariance__mutmut_29": xǁEWMAǁcovariance__mutmut_29,
        "xǁEWMAǁcovariance__mutmut_30": xǁEWMAǁcovariance__mutmut_30,
        "xǁEWMAǁcovariance__mutmut_31": xǁEWMAǁcovariance__mutmut_31,
        "xǁEWMAǁcovariance__mutmut_32": xǁEWMAǁcovariance__mutmut_32,
        "xǁEWMAǁcovariance__mutmut_33": xǁEWMAǁcovariance__mutmut_33,
        "xǁEWMAǁcovariance__mutmut_34": xǁEWMAǁcovariance__mutmut_34,
        "xǁEWMAǁcovariance__mutmut_35": xǁEWMAǁcovariance__mutmut_35,
        "xǁEWMAǁcovariance__mutmut_36": xǁEWMAǁcovariance__mutmut_36,
        "xǁEWMAǁcovariance__mutmut_37": xǁEWMAǁcovariance__mutmut_37,
        "xǁEWMAǁcovariance__mutmut_38": xǁEWMAǁcovariance__mutmut_38,
        "xǁEWMAǁcovariance__mutmut_39": xǁEWMAǁcovariance__mutmut_39,
        "xǁEWMAǁcovariance__mutmut_40": xǁEWMAǁcovariance__mutmut_40,
        "xǁEWMAǁcovariance__mutmut_41": xǁEWMAǁcovariance__mutmut_41,
        "xǁEWMAǁcovariance__mutmut_42": xǁEWMAǁcovariance__mutmut_42,
        "xǁEWMAǁcovariance__mutmut_43": xǁEWMAǁcovariance__mutmut_43,
        "xǁEWMAǁcovariance__mutmut_44": xǁEWMAǁcovariance__mutmut_44,
        "xǁEWMAǁcovariance__mutmut_45": xǁEWMAǁcovariance__mutmut_45,
        "xǁEWMAǁcovariance__mutmut_46": xǁEWMAǁcovariance__mutmut_46,
    }
    xǁEWMAǁcovariance__mutmut_orig.__name__ = "xǁEWMAǁcovariance"
