"""Markov-Switching VAR model (Krolzig, 1997).

Implements VAR(p) with regime-dependent parameters using EM estimation.

References
----------
Krolzig, H.-M. (1997). Markov-Switching Vector Autoregressions. Springer.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from archbox.regime.base import MarkovSwitchingModel

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


class MarkovSwitchingVAR(MarkovSwitchingModel):
    """Markov-Switching VAR(p) model (Krolzig, 1997).

    y_t = mu_{S_t} + Phi_1(S_t) * y_{t-1} + ... + Phi_p(S_t) * y_{t-p} + eps_t
    eps_t ~ N(0, Sigma_{S_t})

    Parameters
    ----------
    endog : array-like
        Multivariate time series, shape (T, n).
    k_regimes : int
        Number of regimes. Default is 2.
    order : int
        VAR order (number of lags). Default is 1.
    switching_mean : bool
        If True, intercept switches. Default True.
    switching_variance : bool
        If True, covariance matrix switches. Default True.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_var import MarkovSwitchingVAR
    >>> y = np.random.randn(200, 2)
    >>> model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-VAR"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        args = [endog, k_regimes, order, switching_mean, switching_variance]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingVARǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingVARǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingVARǁ__init____mutmut_orig(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_1(
        self,
        endog: Any,
        k_regimes: int = 3,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_2(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 2,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_3(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = False,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_4(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = False,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_5(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = None
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_6(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(None, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_7(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=None)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_8(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_9(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(
            endog,
        )
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_10(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim != 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_11(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 2:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_12(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = None

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_13(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(None, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_14(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, None)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_15(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_16(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(
                -1,
            )

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_17(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(+1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_18(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-2, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_19(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 2)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_20(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            None,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_21(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=None,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_22(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=None,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_23(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=None,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_24(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=None,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_25(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=None,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_26(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_27(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_28(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_29(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_30(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_31(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_32(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=False,
        )

        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingVARǁ__init____mutmut_33(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = None

    def xǁMarkovSwitchingVARǁ__init____mutmut_34(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 1,
        switching_mean: bool = True,
        switching_variance: bool = True,
    ) -> None:
        """Initialize Markov-Switching VAR model."""
        endog_arr = np.asarray(endog, dtype=np.float64)
        if endog_arr.ndim == 1:
            endog_arr = endog_arr.reshape(-1, 1)

        super().__init__(
            endog_arr,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=True,
        )

        self._effective_nobs = self.nobs + self.order

    xǁMarkovSwitchingVARǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingVARǁ__init____mutmut_1": xǁMarkovSwitchingVARǁ__init____mutmut_1,
        "xǁMarkovSwitchingVARǁ__init____mutmut_2": xǁMarkovSwitchingVARǁ__init____mutmut_2,
        "xǁMarkovSwitchingVARǁ__init____mutmut_3": xǁMarkovSwitchingVARǁ__init____mutmut_3,
        "xǁMarkovSwitchingVARǁ__init____mutmut_4": xǁMarkovSwitchingVARǁ__init____mutmut_4,
        "xǁMarkovSwitchingVARǁ__init____mutmut_5": xǁMarkovSwitchingVARǁ__init____mutmut_5,
        "xǁMarkovSwitchingVARǁ__init____mutmut_6": xǁMarkovSwitchingVARǁ__init____mutmut_6,
        "xǁMarkovSwitchingVARǁ__init____mutmut_7": xǁMarkovSwitchingVARǁ__init____mutmut_7,
        "xǁMarkovSwitchingVARǁ__init____mutmut_8": xǁMarkovSwitchingVARǁ__init____mutmut_8,
        "xǁMarkovSwitchingVARǁ__init____mutmut_9": xǁMarkovSwitchingVARǁ__init____mutmut_9,
        "xǁMarkovSwitchingVARǁ__init____mutmut_10": xǁMarkovSwitchingVARǁ__init____mutmut_10,
        "xǁMarkovSwitchingVARǁ__init____mutmut_11": xǁMarkovSwitchingVARǁ__init____mutmut_11,
        "xǁMarkovSwitchingVARǁ__init____mutmut_12": xǁMarkovSwitchingVARǁ__init____mutmut_12,
        "xǁMarkovSwitchingVARǁ__init____mutmut_13": xǁMarkovSwitchingVARǁ__init____mutmut_13,
        "xǁMarkovSwitchingVARǁ__init____mutmut_14": xǁMarkovSwitchingVARǁ__init____mutmut_14,
        "xǁMarkovSwitchingVARǁ__init____mutmut_15": xǁMarkovSwitchingVARǁ__init____mutmut_15,
        "xǁMarkovSwitchingVARǁ__init____mutmut_16": xǁMarkovSwitchingVARǁ__init____mutmut_16,
        "xǁMarkovSwitchingVARǁ__init____mutmut_17": xǁMarkovSwitchingVARǁ__init____mutmut_17,
        "xǁMarkovSwitchingVARǁ__init____mutmut_18": xǁMarkovSwitchingVARǁ__init____mutmut_18,
        "xǁMarkovSwitchingVARǁ__init____mutmut_19": xǁMarkovSwitchingVARǁ__init____mutmut_19,
        "xǁMarkovSwitchingVARǁ__init____mutmut_20": xǁMarkovSwitchingVARǁ__init____mutmut_20,
        "xǁMarkovSwitchingVARǁ__init____mutmut_21": xǁMarkovSwitchingVARǁ__init____mutmut_21,
        "xǁMarkovSwitchingVARǁ__init____mutmut_22": xǁMarkovSwitchingVARǁ__init____mutmut_22,
        "xǁMarkovSwitchingVARǁ__init____mutmut_23": xǁMarkovSwitchingVARǁ__init____mutmut_23,
        "xǁMarkovSwitchingVARǁ__init____mutmut_24": xǁMarkovSwitchingVARǁ__init____mutmut_24,
        "xǁMarkovSwitchingVARǁ__init____mutmut_25": xǁMarkovSwitchingVARǁ__init____mutmut_25,
        "xǁMarkovSwitchingVARǁ__init____mutmut_26": xǁMarkovSwitchingVARǁ__init____mutmut_26,
        "xǁMarkovSwitchingVARǁ__init____mutmut_27": xǁMarkovSwitchingVARǁ__init____mutmut_27,
        "xǁMarkovSwitchingVARǁ__init____mutmut_28": xǁMarkovSwitchingVARǁ__init____mutmut_28,
        "xǁMarkovSwitchingVARǁ__init____mutmut_29": xǁMarkovSwitchingVARǁ__init____mutmut_29,
        "xǁMarkovSwitchingVARǁ__init____mutmut_30": xǁMarkovSwitchingVARǁ__init____mutmut_30,
        "xǁMarkovSwitchingVARǁ__init____mutmut_31": xǁMarkovSwitchingVARǁ__init____mutmut_31,
        "xǁMarkovSwitchingVARǁ__init____mutmut_32": xǁMarkovSwitchingVARǁ__init____mutmut_32,
        "xǁMarkovSwitchingVARǁ__init____mutmut_33": xǁMarkovSwitchingVARǁ__init____mutmut_33,
        "xǁMarkovSwitchingVARǁ__init____mutmut_34": xǁMarkovSwitchingVARǁ__init____mutmut_34,
    }
    xǁMarkovSwitchingVARǁ__init____mutmut_orig.__name__ = "xǁMarkovSwitchingVARǁ__init__"

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = None
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = None
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = None
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = None

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = None

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(None, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, None)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(
            params,
        )

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = None

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(None, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, None)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(-1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(
            n_obs,
        )

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, +1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -10000000001.0)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = None

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma - 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 / np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1.000001 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(None)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = None
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(None)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = None
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 / np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 3.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_27(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(None)
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_28(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(None))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_29(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(None)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_30(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = None
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_31(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(None)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_32(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = None
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_33(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(None, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_34(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, None)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_35(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_36(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(
                eigvals,
            )
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_37(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1.0000000001)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_38(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = None
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_39(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(None)
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_40(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(None))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_41(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(None)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_42(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = None

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_43(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma - max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_44(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) / np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_45(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(None, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_46(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, None) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_47(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_48(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(
                -float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6,
            ) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_49(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) - 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_50(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(+float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_51(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(None) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_52(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(None)) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_53(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(None))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_54(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1.000001, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_55(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 1) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_56(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(None)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_57(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = None
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_58(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(None)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_59(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = None

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_60(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) + 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_61(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n / np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_62(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 / n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_63(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = +0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_64(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -1.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_65(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(None) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_66(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 / np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_67(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(3.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_68(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 / log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_69(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 1.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_70(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(None, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_71(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, None):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_72(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_73(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(
            p,
        ):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_74(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = None
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_75(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] + mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_76(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(None):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_77(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = None
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_78(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag / n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_79(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) / n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_80(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag - 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_81(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 2) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_82(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = None

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_83(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid + phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_84(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag + 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_85(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t + lag - 1]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_86(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 2]

            ll[t] = const - 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_87(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = None

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_88(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const + 0.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_89(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 / float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_90(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 1.5 * float(resid @ sigma_inv @ resid)

        return ll

    def xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_91(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        n_obs = self.nobs
        n = self.n_vars
        p = self.order
        y = self.endog

        # Extract regime parameters
        mu, phi, sigma = self._unpack_var_params(params, regime)

        ll = np.full(n_obs, -1e10)

        # Ensure Sigma is positive definite
        sigma = sigma + 1e-6 * np.eye(n)

        try:
            chol = np.linalg.cholesky(sigma)
            log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        except np.linalg.LinAlgError:
            eigvals = np.linalg.eigvalsh(sigma)
            eigvals = np.maximum(eigvals, 1e-10)
            log_det = float(np.sum(np.log(eigvals)))
            sigma = sigma + max(-float(np.min(np.linalg.eigvalsh(sigma))) + 1e-6, 0) * np.eye(n)

        sigma_inv = np.linalg.inv(sigma)
        const = -0.5 * n * np.log(2.0 * np.pi) - 0.5 * log_det

        for t in range(p, n_obs):
            resid = y[t] - mu
            for lag in range(p):
                phi_l = phi[:, lag * n : (lag + 1) * n]
                resid = resid - phi_l @ y[t - lag - 1]

            ll[t] = const - 0.5 * float(None)

        return ll

    xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_1": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_1,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_2": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_2,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_3": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_3,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_4": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_4,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_5": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_5,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_6": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_6,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_7": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_7,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_8": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_8,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_9": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_9,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_10": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_10,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_11": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_11,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_12": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_12,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_13": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_13,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_14": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_14,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_15": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_15,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_16": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_16,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_17": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_17,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_18": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_18,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_19": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_19,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_20": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_20,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_21": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_21,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_22": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_22,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_23": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_23,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_24": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_24,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_25": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_25,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_26": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_26,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_27": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_27,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_28": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_28,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_29": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_29,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_30": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_30,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_31": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_31,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_32": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_32,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_33": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_33,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_34": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_34,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_35": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_35,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_36": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_36,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_37": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_37,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_38": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_38,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_39": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_39,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_40": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_40,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_41": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_41,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_42": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_42,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_43": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_43,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_44": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_44,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_45": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_45,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_46": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_46,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_47": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_47,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_48": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_48,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_49": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_49,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_50": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_50,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_51": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_51,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_52": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_52,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_53": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_53,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_54": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_54,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_55": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_55,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_56": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_56,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_57": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_57,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_58": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_58,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_59": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_59,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_60": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_60,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_61": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_61,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_62": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_62,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_63": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_63,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_64": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_64,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_65": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_65,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_66": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_66,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_67": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_67,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_68": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_68,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_69": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_69,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_70": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_70,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_71": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_71,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_72": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_72,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_73": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_73,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_74": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_74,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_75": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_75,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_76": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_76,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_77": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_77,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_78": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_78,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_79": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_79,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_80": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_80,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_81": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_81,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_82": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_82,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_83": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_83,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_84": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_84,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_85": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_85,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_86": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_86,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_87": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_87,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_88": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_88,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_89": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_89,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_90": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_90,
        "xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_91": xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_91,
    }
    xǁMarkovSwitchingVARǁ_regime_loglike__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingVARǁ_regime_loglike"
    )

    def _unpack_var_params(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_orig"),
            object.__getattribute__(
                self, "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = None
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = None
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = None
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = None

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 1

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = None
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime / n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = None
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx - mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start - n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx - mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx = k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx -= k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k / n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = None
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n / p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n / n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = None
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime / phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = None
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx - phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start - phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx - phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = None
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(None, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, None)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_27(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_28(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(
            n,
        )
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_29(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n / p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_30(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx = k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_31(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx -= k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_32(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k / phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_33(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = None
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_34(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) / 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_35(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n / (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_36(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n - 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_37(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 2) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_38(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 3
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_39(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = None
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_40(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime / cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_41(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = None

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_42(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx - cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_43(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start - cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_44(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx - cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_45(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = None
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_46(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros(None)
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_47(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = None
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_48(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 1
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_49(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(None):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_50(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(None):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_51(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i - 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_52(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 2):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_53(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = None
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_54(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx = 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_55(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx -= 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_56(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 2
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_57(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(None, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_58(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, None)
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_59(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_60(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(
            chol,
        )
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_61(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(None, 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_62(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), None))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_63(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_64(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(
            chol,
            np.maximum(
                np.abs(np.diag(chol)),
            ),
        )
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_65(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(None), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_66(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(None)), 1e-4))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_67(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1.0001))
        sigma = chol @ chol.T

        return mu, phi, sigma

    def xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_68(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack VAR parameters for a specific regime.

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, Phi, Sigma) where:
            - mu: intercept, shape (n,)
            - Phi: VAR coefficients, shape (n, n*p)
            - Sigma: covariance matrix, shape (n, n)
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        idx = 0

        # Intercepts: k * n params
        mu_start = regime * n
        mu = params[idx + mu_start : idx + mu_start + n].copy()
        idx += k * n

        # VAR coefficients: k * n * n * p params
        phi_size = n * n * p
        phi_start = regime * phi_size
        phi_flat = params[idx + phi_start : idx + phi_start + phi_size]
        phi = phi_flat.reshape(n, n * p)
        idx += k * phi_size

        # Covariance: k * n * (n+1) / 2 params (lower triangular)
        cov_size = n * (n + 1) // 2
        cov_start = regime * cov_size
        l_flat = params[idx + cov_start : idx + cov_start + cov_size]

        # Reconstruct lower triangular matrix
        chol = np.zeros((n, n))
        l_idx = 0
        for i in range(n):
            for j in range(i + 1):
                chol[i, j] = l_flat[l_idx]
                l_idx += 1
        # Ensure positive diagonal
        np.fill_diagonal(chol, np.maximum(np.abs(np.diag(chol)), 1e-4))
        sigma = None

        return mu, phi, sigma

    xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_1": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_1,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_2": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_2,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_3": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_3,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_4": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_4,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_5": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_5,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_6": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_6,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_7": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_7,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_8": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_8,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_9": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_9,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_10": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_10,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_11": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_11,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_12": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_12,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_13": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_13,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_14": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_14,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_15": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_15,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_16": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_16,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_17": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_17,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_18": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_18,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_19": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_19,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_20": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_20,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_21": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_21,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_22": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_22,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_23": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_23,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_24": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_24,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_25": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_25,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_26": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_26,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_27": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_27,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_28": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_28,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_29": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_29,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_30": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_30,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_31": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_31,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_32": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_32,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_33": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_33,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_34": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_34,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_35": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_35,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_36": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_36,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_37": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_37,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_38": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_38,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_39": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_39,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_40": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_40,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_41": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_41,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_42": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_42,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_43": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_43,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_44": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_44,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_45": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_45,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_46": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_46,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_47": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_47,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_48": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_48,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_49": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_49,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_50": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_50,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_51": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_51,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_52": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_52,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_53": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_53,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_54": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_54,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_55": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_55,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_56": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_56,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_57": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_57,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_58": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_58,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_59": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_59,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_60": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_60,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_61": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_61,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_62": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_62,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_63": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_63,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_64": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_64,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_65": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_65,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_66": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_66,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_67": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_67,
        "xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_68": xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_68,
    }
    xǁMarkovSwitchingVARǁ_unpack_var_params__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingVARǁ_unpack_var_params"
    )

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values."""
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        params_list: list[float] = []

        # Intercepts (k * n)
        y_mean = np.mean(y, axis=0)
        for s in range(k):
            spread = (s - (k - 1) / 2.0) * 0.5
            mu_s = y_mean + spread
            params_list.extend(mu_s.tolist())

        # VAR coefficients (k * n * n * p): small values
        for _s in range(k):
            for _l in range(p):
                phi_l = 0.1 * np.eye(n)
                params_list.extend(phi_l.flatten().tolist())

        # Covariance (k * n*(n+1)/2): from sample covariance
        sample_cov = np.cov(y.T)
        if sample_cov.ndim == 0:
            sample_cov = np.array([[float(sample_cov)]])
        try:
            l_sample = np.linalg.cholesky(sample_cov)
        except np.linalg.LinAlgError:
            l_sample = np.eye(n) * np.sqrt(float(np.var(y)))

        for s in range(k):
            scale = 0.5 + s * 1.0
            l_s = l_sample * np.sqrt(scale)
            for i in range(n):
                for j in range(i + 1):
                    params_list.append(float(l_s[i, j]))

        # Transition params
        n_trans = k * (k - 1)
        params_list.extend([0.0] * n_trans)

        return np.array(params_list)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        names: list[str] = []

        # Intercepts
        for s in range(k):
            names.extend([f"mu_{s}_{v}" for v in range(n)])

        # VAR coefficients
        for s in range(k):
            for lag in range(p):
                for i in range(n):
                    for j in range(n):
                        names.append(f"Phi_{lag + 1}_{i}{j}(S={s})")

        # Covariance
        for s in range(k):
            for i in range(n):
                for j in range(i + 1):
                    names.append(f"L_{i}{j}(S={s})")

        # Transition
        names.extend([f"p_{i}{j}" for i in range(k) for j in range(k) if i != j])

        return names

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, smoothed, joint_smoothed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_orig(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_1(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = None
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_2(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = None
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_3(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = None
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_4(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = None
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_5(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = None
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_6(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = None

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_7(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = None

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_8(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 1

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_9(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(None):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_10(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = None
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_11(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = None

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_12(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(None)

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_13(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum <= 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_14(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1.000000000001:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_15(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                break

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_16(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = None
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_17(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(None)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_18(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(None):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_19(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = None

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_20(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) * w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_21(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(None) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_22(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(None)) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_23(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights / y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_24(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = None
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_25(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx - s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_26(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s / n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_27(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = None

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_28(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start - n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_29(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx = k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_30(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx -= k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_31(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k / n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_32(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx = k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_33(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx -= k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_34(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n / p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_35(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n / n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_36(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k / n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_37(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(None):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_38(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = None
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_39(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(None, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_40(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, None)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_41(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_42(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(
                new_params,
            )
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_43(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = None
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_44(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = None

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_45(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(None)

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_46(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum >= 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_47(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1.000000000001:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_48(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = None
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_49(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros(None)
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_50(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs + p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_51(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(None):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_52(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs + p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_53(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = None
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_54(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx - p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_55(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = None
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_56(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] + mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_57(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(None):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_58(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = None
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_59(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag / n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_60(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) / n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_61(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag - 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_62(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 2) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_63(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = None
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_64(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid + phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_65(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag + 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_66(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t + lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_67(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 2]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_68(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = None

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_69(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = None
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_70(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros(None)
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_71(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(None):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_72(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs + p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_73(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s = weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_74(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s -= weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_75(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] / np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_76(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(None, residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_77(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], None)
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_78(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_79(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(
                        residuals[t_idx],
                    )
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_80(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s = w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_81(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s *= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_82(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s = 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_83(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s -= 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_84(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 / np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_85(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1.000001 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_86(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(None)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_87(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = None
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_88(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(None)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_89(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = None
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_90(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) / 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_91(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n / (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_92(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n - 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_93(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 2) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_94(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 3
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_95(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = None
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_96(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) - s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_97(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n - k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_98(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k / n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_99(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n / p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_100(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n / n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_101(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k / n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_102(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s / cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_103(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = None
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_104(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 1
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_105(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(None):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_106(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(None):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_107(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i - 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_108(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 2):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_109(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = None
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_110(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start - l_idx] = l_s[i, j]
                            l_idx += 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_111(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx = 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_112(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx -= 1
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingVARǁ_m_step_update__mutmut_113(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-VAR.

        Uses weighted OLS for each regime.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        n = self.n_vars
        p = self.order
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        idx = 0

        # Update intercepts
        for s in range(k):
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum < 1e-12:
                continue

            mu_s = np.zeros(n)
            for v in range(n):
                mu_s[v] = float(np.sum(weights * y[p:, v])) / w_sum

            mu_start = idx + s * n
            new_params[mu_start : mu_start + n] = mu_s

        idx += k * n

        # VAR coefficients: keep current for stability
        idx += k * n * n * p

        # Covariance update
        for s in range(k):
            mu_s, phi_s, _ = self._unpack_var_params(new_params, s)
            weights = smoothed[p:, s]
            w_sum = float(weights.sum())

            if w_sum > 1e-12:
                # Compute residuals
                residuals = np.zeros((n_obs - p, n))
                for t_idx in range(n_obs - p):
                    t = t_idx + p
                    resid = y[t] - mu_s
                    for lag in range(p):
                        phi_l = phi_s[:, lag * n : (lag + 1) * n]
                        resid = resid - phi_l @ y[t - lag - 1]
                    residuals[t_idx] = resid

                # Weighted covariance
                sigma_s = np.zeros((n, n))
                for t_idx in range(n_obs - p):
                    sigma_s += weights[t_idx] * np.outer(residuals[t_idx], residuals[t_idx])
                sigma_s /= w_sum
                sigma_s += 1e-6 * np.eye(n)

                # Cholesky for parameterization
                try:
                    l_s = np.linalg.cholesky(sigma_s)
                    cov_size = n * (n + 1) // 2
                    cov_start = (k * n + k * n * n * p) + s * cov_size
                    l_idx = 0
                    for i in range(n):
                        for j in range(i + 1):
                            new_params[cov_start + l_idx] = l_s[i, j]
                            l_idx += 2
                except np.linalg.LinAlgError:
                    pass

        return new_params

    xǁMarkovSwitchingVARǁ_m_step_update__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_1": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_1,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_2": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_2,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_3": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_3,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_4": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_4,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_5": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_5,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_6": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_6,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_7": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_7,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_8": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_8,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_9": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_9,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_10": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_10,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_11": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_11,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_12": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_12,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_13": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_13,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_14": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_14,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_15": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_15,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_16": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_16,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_17": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_17,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_18": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_18,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_19": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_19,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_20": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_20,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_21": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_21,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_22": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_22,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_23": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_23,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_24": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_24,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_25": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_25,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_26": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_26,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_27": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_27,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_28": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_28,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_29": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_29,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_30": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_30,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_31": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_31,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_32": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_32,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_33": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_33,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_34": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_34,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_35": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_35,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_36": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_36,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_37": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_37,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_38": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_38,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_39": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_39,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_40": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_40,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_41": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_41,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_42": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_42,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_43": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_43,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_44": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_44,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_45": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_45,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_46": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_46,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_47": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_47,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_48": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_48,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_49": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_49,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_50": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_50,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_51": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_51,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_52": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_52,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_53": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_53,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_54": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_54,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_55": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_55,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_56": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_56,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_57": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_57,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_58": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_58,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_59": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_59,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_60": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_60,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_61": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_61,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_62": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_62,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_63": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_63,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_64": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_64,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_65": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_65,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_66": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_66,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_67": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_67,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_68": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_68,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_69": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_69,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_70": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_70,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_71": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_71,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_72": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_72,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_73": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_73,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_74": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_74,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_75": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_75,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_76": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_76,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_77": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_77,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_78": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_78,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_79": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_79,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_80": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_80,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_81": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_81,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_82": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_82,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_83": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_83,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_84": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_84,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_85": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_85,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_86": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_86,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_87": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_87,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_88": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_88,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_89": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_89,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_90": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_90,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_91": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_91,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_92": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_92,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_93": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_93,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_94": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_94,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_95": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_95,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_96": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_96,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_97": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_97,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_98": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_98,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_99": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_99,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_100": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_100,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_101": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_101,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_102": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_102,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_103": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_103,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_104": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_104,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_105": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_105,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_106": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_106,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_107": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_107,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_108": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_108,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_109": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_109,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_110": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_110,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_111": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_111,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_112": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_112,
        "xǁMarkovSwitchingVARǁ_m_step_update__mutmut_113": xǁMarkovSwitchingVARǁ_m_step_update__mutmut_113,
    }
    xǁMarkovSwitchingVARǁ_m_step_update__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingVARǁ_m_step_update"
    )

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_orig(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_1(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = None
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_2(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = None
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_3(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = None
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_4(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(None):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_5(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = None
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_6(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(None, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_7(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, None)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_8(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_9(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(
                params,
            )
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_10(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = None
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_11(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(None):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_12(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = None
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_13(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(None)
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_14(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = None
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_15(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(None)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_16(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(None):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_17(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = None
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_18(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(None)
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_19(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific VAR parameters."""
        k = self.k_regimes
        n = self.n_vars
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            mu, _phi, sigma = self._unpack_var_params(params, s)
            rp: dict[str, float] = {}
            for v in range(n):
                rp[f"mu_{v}"] = float(mu[v])
            sigma_diag = np.diag(sigma)
            for v in range(n):
                rp[f"Sigma_{v}{v}"] = float(sigma_diag[v])
            regime_params[s] = None
        return regime_params

    xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_1": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_1,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_2": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_2,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_3": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_3,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_4": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_4,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_5": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_5,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_6": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_6,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_7": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_7,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_8": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_8,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_9": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_9,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_10": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_10,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_11": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_11,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_12": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_12,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_13": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_13,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_14": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_14,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_15": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_15,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_16": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_16,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_17": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_17,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_18": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_18,
        "xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_19": xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_19,
    }
    xǁMarkovSwitchingVARǁ_extract_regime_params__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingVARǁ_extract_regime_params"
    )
