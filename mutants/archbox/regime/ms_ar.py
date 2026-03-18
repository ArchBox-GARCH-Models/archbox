"""Markov-Switching Autoregressive model (Hamilton, 1989).

Implements the classic MS(k)-AR(p) model where the mean, variance,
and optionally AR coefficients switch between regimes.

References
----------
Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle.
Econometrica, 57(2), 357-384.

Hamilton, J.D. (1994). Time Series Analysis. Princeton University Press.
Chapter 22.
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


class MarkovSwitchingAR(MarkovSwitchingModel):
    """Markov-Switching AR(p) model (Hamilton, 1989).

    y_t - mu_{S_t} = phi_1 * (y_{t-1} - mu_{S_{t-1}}) + ... + eps_t
    eps_t ~ N(0, sigma^2_{S_t})

    Parameters
    ----------
    endog : array-like
        Time series of observations, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.
    order : int
        AR order (number of lags). Default is 4.
    switching_mean : bool
        If True, the mean switches between regimes. Default True.
    switching_variance : bool
        If True, the variance switches between regimes. Default True.
    switching_ar : bool
        If True, AR coefficients switch between regimes. Default False.

    Examples
    --------
    >>> from archbox.regime.ms_ar import MarkovSwitchingAR
    >>> from archbox.datasets import load_dataset
    >>> gdp = load_dataset('us_gdp_quarterly')
    >>> growth = gdp['growth'].to_numpy()
    >>> model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-AR"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        args = [endog, k_regimes, order, switching_mean, switching_variance, switching_ar]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ__init____mutmut_orig(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_1(
        self,
        endog: Any,
        k_regimes: int = 3,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_2(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 5,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_3(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = False,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_4(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = False,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_5(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = True,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_6(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            None,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_7(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=None,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_8(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=None,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_9(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=None,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_10(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=None,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_11(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=None,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_12(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_13(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_14(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_15(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_16(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_17(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
        )
        self._effective_nobs = self.nobs - self.order

    def xǁMarkovSwitchingARǁ__init____mutmut_18(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = None

    def xǁMarkovSwitchingARǁ__init____mutmut_19(
        self,
        endog: Any,
        k_regimes: int = 2,
        order: int = 4,
        switching_mean: bool = True,
        switching_variance: bool = True,
        switching_ar: bool = False,
    ) -> None:
        """Initialize Markov-Switching AR model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=order,
            switching_mean=switching_mean,
            switching_variance=switching_variance,
            switching_ar=switching_ar,
        )
        self._effective_nobs = self.nobs + self.order

    xǁMarkovSwitchingARǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ__init____mutmut_1": xǁMarkovSwitchingARǁ__init____mutmut_1,
        "xǁMarkovSwitchingARǁ__init____mutmut_2": xǁMarkovSwitchingARǁ__init____mutmut_2,
        "xǁMarkovSwitchingARǁ__init____mutmut_3": xǁMarkovSwitchingARǁ__init____mutmut_3,
        "xǁMarkovSwitchingARǁ__init____mutmut_4": xǁMarkovSwitchingARǁ__init____mutmut_4,
        "xǁMarkovSwitchingARǁ__init____mutmut_5": xǁMarkovSwitchingARǁ__init____mutmut_5,
        "xǁMarkovSwitchingARǁ__init____mutmut_6": xǁMarkovSwitchingARǁ__init____mutmut_6,
        "xǁMarkovSwitchingARǁ__init____mutmut_7": xǁMarkovSwitchingARǁ__init____mutmut_7,
        "xǁMarkovSwitchingARǁ__init____mutmut_8": xǁMarkovSwitchingARǁ__init____mutmut_8,
        "xǁMarkovSwitchingARǁ__init____mutmut_9": xǁMarkovSwitchingARǁ__init____mutmut_9,
        "xǁMarkovSwitchingARǁ__init____mutmut_10": xǁMarkovSwitchingARǁ__init____mutmut_10,
        "xǁMarkovSwitchingARǁ__init____mutmut_11": xǁMarkovSwitchingARǁ__init____mutmut_11,
        "xǁMarkovSwitchingARǁ__init____mutmut_12": xǁMarkovSwitchingARǁ__init____mutmut_12,
        "xǁMarkovSwitchingARǁ__init____mutmut_13": xǁMarkovSwitchingARǁ__init____mutmut_13,
        "xǁMarkovSwitchingARǁ__init____mutmut_14": xǁMarkovSwitchingARǁ__init____mutmut_14,
        "xǁMarkovSwitchingARǁ__init____mutmut_15": xǁMarkovSwitchingARǁ__init____mutmut_15,
        "xǁMarkovSwitchingARǁ__init____mutmut_16": xǁMarkovSwitchingARǁ__init____mutmut_16,
        "xǁMarkovSwitchingARǁ__init____mutmut_17": xǁMarkovSwitchingARǁ__init____mutmut_17,
        "xǁMarkovSwitchingARǁ__init____mutmut_18": xǁMarkovSwitchingARǁ__init____mutmut_18,
        "xǁMarkovSwitchingARǁ__init____mutmut_19": xǁMarkovSwitchingARǁ__init____mutmut_19,
    }
    xǁMarkovSwitchingARǁ__init____mutmut_orig.__name__ = "xǁMarkovSwitchingARǁ__init__"

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = None
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = None
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = None

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = None

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(None, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, None)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(
            params,
        )

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = None

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(None, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, None)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(-1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(
            n,
        )

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, +1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -10000000001.0)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p != 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 1:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = None
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y + mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = None
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) + 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) + np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 / np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = +0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -1.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(None) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_27(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 / np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_28(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(3.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_29(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(None) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_30(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 / (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_31(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 1.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_32(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) * 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_33(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid * sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_34(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 3
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_35(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p <= n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_36(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = None

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_37(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y + mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_38(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = None
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_39(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(None, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_40(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, None):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_41(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_42(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(
                1,
            ):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_43(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(2, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_44(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p - 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_45(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 2):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_46(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = None

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_47(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid + phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_48(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] / y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_49(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag + 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_50(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 2] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_51(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p + lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_52(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n + lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_53(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = None

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_54(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) + 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_55(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) + np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_56(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 / np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_57(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = +0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_58(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -1.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_59(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(None) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_60(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 / np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_61(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(3.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_62(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(None) - 0.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_63(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 / (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_64(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 1.5 * (resid / sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_65(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) * 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_66(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid * sigma) ** 2

        return ll

    def xǁMarkovSwitchingARǁ_regime_loglike__mutmut_67(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the simplified approximation where mu_{S_{t-1}} is replaced
        by the weighted average of regime means (Kim, 1994 approximation).

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
        p = self.order
        y = self.endog
        n = self.nobs

        mu, phi, sigma = self._unpack_params(params, regime)

        ll = np.full(n, -1e10)

        if p == 0:
            # No AR component - simple normal log-likelihood
            resid = y - mu
            ll[:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 2
            return ll

        if p < n:
            # Demean
            y_demean = y - mu

            # Residuals for t >= p
            resid = y_demean[p:].copy()
            for lag in range(1, p + 1):
                resid = resid - phi[lag - 1] * y_demean[p - lag : n - lag]

            ll[p:] = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * (resid / sigma) ** 3

        return ll

    xǁMarkovSwitchingARǁ_regime_loglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_1": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_1,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_2": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_2,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_3": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_3,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_4": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_4,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_5": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_5,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_6": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_6,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_7": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_7,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_8": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_8,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_9": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_9,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_10": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_10,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_11": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_11,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_12": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_12,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_13": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_13,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_14": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_14,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_15": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_15,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_16": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_16,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_17": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_17,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_18": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_18,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_19": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_19,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_20": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_20,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_21": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_21,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_22": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_22,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_23": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_23,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_24": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_24,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_25": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_25,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_26": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_26,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_27": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_27,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_28": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_28,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_29": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_29,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_30": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_30,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_31": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_31,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_32": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_32,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_33": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_33,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_34": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_34,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_35": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_35,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_36": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_36,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_37": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_37,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_38": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_38,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_39": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_39,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_40": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_40,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_41": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_41,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_42": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_42,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_43": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_43,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_44": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_44,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_45": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_45,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_46": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_46,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_47": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_47,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_48": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_48,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_49": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_49,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_50": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_50,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_51": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_51,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_52": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_52,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_53": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_53,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_54": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_54,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_55": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_55,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_56": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_56,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_57": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_57,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_58": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_58,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_59": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_59,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_60": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_60,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_61": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_61,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_62": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_62,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_63": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_63,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_64": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_64,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_65": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_65,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_66": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_66,
        "xǁMarkovSwitchingARǁ_regime_loglike__mutmut_67": xǁMarkovSwitchingARǁ_regime_loglike__mutmut_67,
    }
    xǁMarkovSwitchingARǁ_regime_loglike__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingARǁ_regime_loglike"
    )

    def _unpack_params(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_unpack_params__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_unpack_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = None
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = None
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = None

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 1

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = None
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(None)
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx - regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx = k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx -= k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = None
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(None)
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx = 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx -= 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 2

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = None
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx - regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime / p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx - (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) / p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime - 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 2) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx = k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx -= k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k / p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = None
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx - p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_27(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx = p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_28(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx -= p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_29(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = None
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_30(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(None, 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_31(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), None)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_32(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_33(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(
                abs(float(params[idx + regime])),
            )
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_34(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(None), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_35(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(None)), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_36(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx - regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_37(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1.000001)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_38(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx = k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_39(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx -= k
        else:
            sigma = max(abs(float(params[idx])), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_40(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = None

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_41(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(None, 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_42(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), None)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_43(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_44(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(
                abs(float(params[idx])),
            )

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_45(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(None), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_46(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(None)), 1e-6)

        return mu, phi, sigma

    def xǁMarkovSwitchingARǁ_unpack_params__mutmut_47(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, NDArray[np.float64], float]:
        """Unpack regime-specific parameters from the vector.

        Parameter layout:
        - If switching_mean: [mu_0, ..., mu_{k-1}] (k params)
        - If not switching_mean: [mu] (1 param)
        - If switching_ar: [phi_1(0), ..., phi_p(0), ..., phi_1(k-1), ..., phi_p(k-1)] (k*p params)
        - If not switching_ar: [phi_1, ..., phi_p] (p params)
        - If switching_variance: [sigma_0, ..., sigma_{k-1}] (k params)
        - If not switching_variance: [sigma] (1 param)
        - Transition params: [trans_0, ..., trans_{k*(k-1)-1}]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (mu, phi, sigma) for the specified regime.
        """
        k = self.k_regimes
        p = self.order
        idx = 0

        # Mean
        if self.switching_mean:
            mu = float(params[idx + regime])
            idx += k
        else:
            mu = float(params[idx])
            idx += 1

        # AR coefficients
        if self.switching_ar:
            phi = params[idx + regime * p : idx + (regime + 1) * p].copy()
            idx += k * p
        else:
            phi = params[idx : idx + p].copy()
            idx += p

        # Variance
        if self.switching_variance:
            sigma = max(abs(float(params[idx + regime])), 1e-6)
            idx += k
        else:
            sigma = max(abs(float(params[idx])), 1.000001)

        return mu, phi, sigma

    xǁMarkovSwitchingARǁ_unpack_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_1": xǁMarkovSwitchingARǁ_unpack_params__mutmut_1,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_2": xǁMarkovSwitchingARǁ_unpack_params__mutmut_2,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_3": xǁMarkovSwitchingARǁ_unpack_params__mutmut_3,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_4": xǁMarkovSwitchingARǁ_unpack_params__mutmut_4,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_5": xǁMarkovSwitchingARǁ_unpack_params__mutmut_5,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_6": xǁMarkovSwitchingARǁ_unpack_params__mutmut_6,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_7": xǁMarkovSwitchingARǁ_unpack_params__mutmut_7,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_8": xǁMarkovSwitchingARǁ_unpack_params__mutmut_8,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_9": xǁMarkovSwitchingARǁ_unpack_params__mutmut_9,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_10": xǁMarkovSwitchingARǁ_unpack_params__mutmut_10,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_11": xǁMarkovSwitchingARǁ_unpack_params__mutmut_11,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_12": xǁMarkovSwitchingARǁ_unpack_params__mutmut_12,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_13": xǁMarkovSwitchingARǁ_unpack_params__mutmut_13,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_14": xǁMarkovSwitchingARǁ_unpack_params__mutmut_14,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_15": xǁMarkovSwitchingARǁ_unpack_params__mutmut_15,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_16": xǁMarkovSwitchingARǁ_unpack_params__mutmut_16,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_17": xǁMarkovSwitchingARǁ_unpack_params__mutmut_17,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_18": xǁMarkovSwitchingARǁ_unpack_params__mutmut_18,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_19": xǁMarkovSwitchingARǁ_unpack_params__mutmut_19,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_20": xǁMarkovSwitchingARǁ_unpack_params__mutmut_20,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_21": xǁMarkovSwitchingARǁ_unpack_params__mutmut_21,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_22": xǁMarkovSwitchingARǁ_unpack_params__mutmut_22,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_23": xǁMarkovSwitchingARǁ_unpack_params__mutmut_23,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_24": xǁMarkovSwitchingARǁ_unpack_params__mutmut_24,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_25": xǁMarkovSwitchingARǁ_unpack_params__mutmut_25,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_26": xǁMarkovSwitchingARǁ_unpack_params__mutmut_26,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_27": xǁMarkovSwitchingARǁ_unpack_params__mutmut_27,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_28": xǁMarkovSwitchingARǁ_unpack_params__mutmut_28,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_29": xǁMarkovSwitchingARǁ_unpack_params__mutmut_29,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_30": xǁMarkovSwitchingARǁ_unpack_params__mutmut_30,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_31": xǁMarkovSwitchingARǁ_unpack_params__mutmut_31,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_32": xǁMarkovSwitchingARǁ_unpack_params__mutmut_32,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_33": xǁMarkovSwitchingARǁ_unpack_params__mutmut_33,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_34": xǁMarkovSwitchingARǁ_unpack_params__mutmut_34,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_35": xǁMarkovSwitchingARǁ_unpack_params__mutmut_35,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_36": xǁMarkovSwitchingARǁ_unpack_params__mutmut_36,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_37": xǁMarkovSwitchingARǁ_unpack_params__mutmut_37,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_38": xǁMarkovSwitchingARǁ_unpack_params__mutmut_38,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_39": xǁMarkovSwitchingARǁ_unpack_params__mutmut_39,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_40": xǁMarkovSwitchingARǁ_unpack_params__mutmut_40,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_41": xǁMarkovSwitchingARǁ_unpack_params__mutmut_41,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_42": xǁMarkovSwitchingARǁ_unpack_params__mutmut_42,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_43": xǁMarkovSwitchingARǁ_unpack_params__mutmut_43,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_44": xǁMarkovSwitchingARǁ_unpack_params__mutmut_44,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_45": xǁMarkovSwitchingARǁ_unpack_params__mutmut_45,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_46": xǁMarkovSwitchingARǁ_unpack_params__mutmut_46,
        "xǁMarkovSwitchingARǁ_unpack_params__mutmut_47": xǁMarkovSwitchingARǁ_unpack_params__mutmut_47,
    }
    xǁMarkovSwitchingARǁ_unpack_params__mutmut_orig.__name__ = "xǁMarkovSwitchingARǁ_unpack_params"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            Initial parameters.
        """
        k = self.k_regimes
        p = self.order
        y = self.endog
        params_list: list[float] = []

        # Means: spread across data range
        if self.switching_mean:
            quantiles = np.linspace(0.2, 0.8, k)
            mus = [float(np.quantile(y, q)) for q in quantiles]
            params_list.extend(mus)
        else:
            params_list.append(float(np.mean(y)))

        # AR coefficients: start near zero
        if self.switching_ar:
            for _s in range(k):
                ar_init = [0.1 / (lag + 1) for lag in range(p)]
                params_list.extend(ar_init)
        else:
            ar_init = [0.1 / (lag + 1) for lag in range(p)]
            params_list.extend(ar_init)

        # Sigmas
        std_y = float(np.std(y))
        if self.switching_variance:
            sigmas = [std_y * (0.5 + s * 0.5) for s in range(k)]
            params_list.extend(sigmas)
        else:
            params_list.append(std_y)

        # Transition params
        n_trans = k * (k - 1)
        params_list.extend([0.0] * n_trans)

        return np.array(params_list)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        p = self.order
        names: list[str] = []

        # Means
        if self.switching_mean:
            names.extend([f"mu_{s}" for s in range(k)])
        else:
            names.append("mu")

        # AR coefficients
        if self.switching_ar:
            for s in range(k):
                names.extend([f"phi_{lag + 1}(S={s})" for lag in range(p)])
        else:
            names.extend([f"phi_{lag + 1}" for lag in range(p)])

        # Sigmas
        if self.switching_variance:
            names.extend([f"sigma_{s}" for s in range(k)])
        else:
            names.append("sigma")

        # Transition
        names.extend([f"p_{i}{j}" for i in range(k) for j in range(k) if i != j])

        return names

    def _update_means(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        args = [new_params, smoothed, idx]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_update_means__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_update_means__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_update_means__mutmut_orig(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_1(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = None
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_2(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = None
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_3(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = None

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_4(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(None):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_5(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = None
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_6(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = None
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_7(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum >= 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_8(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1.000000000001:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_9(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = None
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_10(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx - s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_11(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) * w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_12(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(None) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_13(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights / y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_14(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx - k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_15(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = None
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_16(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum >= 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_17(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1.000000000001:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_18(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = None
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_19(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) * w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_20(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(None) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_21(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) / y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_22(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=None) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_23(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=2) * y[p:]) / w_sum
        return idx + 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_24(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx - 1

    def xǁMarkovSwitchingARǁ_update_means__mutmut_25(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update mean parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_mean:
            for s in range(k):
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    new_params[idx + s] = np.sum(weights * y[p:]) / w_sum
            return idx + k

        w_sum = smoothed[p:].sum()
        if w_sum > 1e-12:
            new_params[idx] = np.sum(smoothed[p:].sum(axis=1) * y[p:]) / w_sum
        return idx + 2

    xǁMarkovSwitchingARǁ_update_means__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_update_means__mutmut_1": xǁMarkovSwitchingARǁ_update_means__mutmut_1,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_2": xǁMarkovSwitchingARǁ_update_means__mutmut_2,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_3": xǁMarkovSwitchingARǁ_update_means__mutmut_3,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_4": xǁMarkovSwitchingARǁ_update_means__mutmut_4,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_5": xǁMarkovSwitchingARǁ_update_means__mutmut_5,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_6": xǁMarkovSwitchingARǁ_update_means__mutmut_6,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_7": xǁMarkovSwitchingARǁ_update_means__mutmut_7,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_8": xǁMarkovSwitchingARǁ_update_means__mutmut_8,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_9": xǁMarkovSwitchingARǁ_update_means__mutmut_9,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_10": xǁMarkovSwitchingARǁ_update_means__mutmut_10,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_11": xǁMarkovSwitchingARǁ_update_means__mutmut_11,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_12": xǁMarkovSwitchingARǁ_update_means__mutmut_12,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_13": xǁMarkovSwitchingARǁ_update_means__mutmut_13,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_14": xǁMarkovSwitchingARǁ_update_means__mutmut_14,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_15": xǁMarkovSwitchingARǁ_update_means__mutmut_15,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_16": xǁMarkovSwitchingARǁ_update_means__mutmut_16,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_17": xǁMarkovSwitchingARǁ_update_means__mutmut_17,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_18": xǁMarkovSwitchingARǁ_update_means__mutmut_18,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_19": xǁMarkovSwitchingARǁ_update_means__mutmut_19,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_20": xǁMarkovSwitchingARǁ_update_means__mutmut_20,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_21": xǁMarkovSwitchingARǁ_update_means__mutmut_21,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_22": xǁMarkovSwitchingARǁ_update_means__mutmut_22,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_23": xǁMarkovSwitchingARǁ_update_means__mutmut_23,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_24": xǁMarkovSwitchingARǁ_update_means__mutmut_24,
        "xǁMarkovSwitchingARǁ_update_means__mutmut_25": xǁMarkovSwitchingARǁ_update_means__mutmut_25,
    }
    xǁMarkovSwitchingARǁ_update_means__mutmut_orig.__name__ = "xǁMarkovSwitchingARǁ_update_means"

    def _wls_ar_coeffs(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        args = [y_demean, weights]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_orig(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_1(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = None
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_2(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = None
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_3(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = None
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_4(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros(None)
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_5(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n + p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_6(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(None):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_7(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = None
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_8(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag + 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_9(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p + lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_10(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 2 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_11(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag + 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_12(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n + lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_13(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 2]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_14(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = None

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_15(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = None
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_16(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(None)
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_17(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(None, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_18(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, None))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_19(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_20(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(
            np.maximum(
                weights,
            )
        )
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_21(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1.000000000001))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_22(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = None
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_23(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = None
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_24(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(None, xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_25(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(p), None)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_26(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_27(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(
                xwx + 1e-8 * np.eye(p),
            )
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_28(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx - 1e-8 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_29(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 / np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_30(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1.00000001 * np.eye(p), xwy)
        except np.linalg.LinAlgError:
            return None

    def xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_31(
        self,
        y_demean: NDArray[np.float64],
        weights: NDArray[np.float64],
    ) -> NDArray[np.float64] | None:
        """Estimate AR coefficients via weighted least squares."""
        p = self.order
        n = self.nobs
        x_mat = np.zeros((n - p, p))
        for lag in range(p):
            x_mat[:, lag] = y_demean[p - lag - 1 : n - lag - 1]
        y_dep = y_demean[p:]

        w_mat = np.diag(np.maximum(weights, 1e-12))
        try:
            xwx = x_mat.T @ w_mat @ x_mat
            xwy = x_mat.T @ w_mat @ y_dep
            return np.linalg.solve(xwx + 1e-8 * np.eye(None), xwy)
        except np.linalg.LinAlgError:
            return None

    xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_1": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_1,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_2": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_2,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_3": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_3,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_4": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_4,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_5": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_5,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_6": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_6,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_7": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_7,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_8": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_8,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_9": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_9,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_10": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_10,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_11": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_11,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_12": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_12,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_13": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_13,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_14": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_14,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_15": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_15,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_16": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_16,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_17": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_17,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_18": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_18,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_19": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_19,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_20": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_20,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_21": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_21,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_22": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_22,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_23": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_23,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_24": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_24,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_25": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_25,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_26": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_26,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_27": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_27,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_28": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_28,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_29": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_29,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_30": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_30,
        "xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_31": xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_31,
    }
    xǁMarkovSwitchingARǁ_wls_ar_coeffs__mutmut_orig.__name__ = "xǁMarkovSwitchingARǁ_wls_ar_coeffs"

    def _update_ar_coeffs(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        args = [new_params, smoothed, idx]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_orig(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_1(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = None
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_2(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = None
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_3(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = None

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_4(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_5(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p >= 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_6(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 1:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_7(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = None
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_8(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(None)
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_9(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(None))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_10(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[1]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_11(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = None
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_12(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=None)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_13(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=2)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_14(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = None
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_15(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(None, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_16(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, None)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_17(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_18(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(
                    y - mu_avg,
                )
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_19(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y + mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_20(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_21(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = None
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_22(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx - p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_23(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx - p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_24(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(None):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_25(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = None
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_26(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(None, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_27(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, None)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_28(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_29(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(
                new_params,
            )
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_30(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = None
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_31(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(None, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_32(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, None)
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_33(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_34(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(
                y - mu_s,
            )
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_35(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y + mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_36(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_37(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = None
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_38(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx - s * p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_39(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s / p : idx + (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_40(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx - (s + 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_41(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) / p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_42(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s - 1) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_43(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 2) * p] = phi_new
        return idx + k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_44(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx - k * p

    def xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_45(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> int:
        """Update AR coefficient parameters in M-step."""
        k = self.k_regimes
        p = self.order
        y = self.endog

        if not self.switching_ar:
            if p > 0:
                mu_avg = float(np.mean(new_params[:k] if self.switching_mean else [new_params[0]]))
                w_total = smoothed[p:].sum(axis=1)
                phi_new = self._wls_ar_coeffs(y - mu_avg, w_total)
                if phi_new is not None:
                    new_params[idx : idx + p] = phi_new
            return idx + p

        for s in range(k):
            mu_s, _, _ = self._unpack_params(new_params, s)
            phi_new = self._wls_ar_coeffs(y - mu_s, smoothed[p:, s])
            if phi_new is not None:
                new_params[idx + s * p : idx + (s + 1) * p] = phi_new
        return idx + k / p

    xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_1": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_1,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_2": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_2,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_3": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_3,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_4": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_4,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_5": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_5,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_6": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_6,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_7": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_7,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_8": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_8,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_9": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_9,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_10": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_10,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_11": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_11,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_12": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_12,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_13": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_13,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_14": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_14,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_15": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_15,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_16": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_16,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_17": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_17,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_18": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_18,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_19": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_19,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_20": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_20,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_21": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_21,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_22": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_22,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_23": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_23,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_24": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_24,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_25": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_25,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_26": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_26,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_27": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_27,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_28": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_28,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_29": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_29,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_30": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_30,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_31": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_31,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_32": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_32,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_33": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_33,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_34": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_34,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_35": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_35,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_36": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_36,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_37": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_37,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_38": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_38,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_39": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_39,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_40": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_40,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_41": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_41,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_42": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_42,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_43": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_43,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_44": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_44,
        "xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_45": xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_45,
    }
    xǁMarkovSwitchingARǁ_update_ar_coeffs__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingARǁ_update_ar_coeffs"
    )

    def _compute_regime_residuals(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        args = [new_params, s]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_orig(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_1(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = None
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_2(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = None
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_3(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = None
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_4(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = None
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_5(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(None, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_6(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, None)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_7(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_8(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(
            new_params,
        )
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_9(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = None
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_10(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y + mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_11(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = None
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_12(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(None):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_13(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = None
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_14(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid + phi_s[lag] * y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_15(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] / y_demean[p - lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_16(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag + 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_17(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p + lag - 1 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_18(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 2 : n - lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_19(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag + 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_20(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n + lag - 1]
        return resid

    def xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_21(
        self,
        new_params: NDArray[np.float64],
        s: int,
    ) -> NDArray[np.float64]:
        """Compute residuals for regime s."""
        p = self.order
        n = self.nobs
        y = self.endog
        mu_s, phi_s, _ = self._unpack_params(new_params, s)
        y_demean = y - mu_s
        resid = y_demean[p:].copy()
        for lag in range(p):
            resid = resid - phi_s[lag] * y_demean[p - lag - 1 : n - lag - 2]
        return resid

    xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_1": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_1,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_2": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_2,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_3": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_3,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_4": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_4,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_5": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_5,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_6": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_6,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_7": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_7,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_8": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_8,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_9": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_9,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_10": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_10,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_11": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_11,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_12": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_12,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_13": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_13,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_14": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_14,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_15": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_15,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_16": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_16,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_17": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_17,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_18": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_18,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_19": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_19,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_20": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_20,
        "xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_21": xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_21,
    }
    xǁMarkovSwitchingARǁ_compute_regime_residuals__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingARǁ_compute_regime_residuals"
    )

    def _update_variances(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        args = [new_params, smoothed, idx]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_update_variances__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_update_variances__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_orig(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_1(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = None
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_2(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = None

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_3(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(None):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_4(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = None
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_5(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(None, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_6(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, None)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_7(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_8(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(
                    new_params,
                )
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_9(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = None
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_10(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = None
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_11(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum >= 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_12(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1.000000000001:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_13(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = None
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_14(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) * w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_15(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(None) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_16(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights / resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_17(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid * 2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_18(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**3) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_19(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = None
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_20(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx - s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_21(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(None, 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_22(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), None)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_23(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_24(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(
                        np.sqrt(var_s),
                    )
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_25(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(None), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_26(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1.000001)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_27(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = None
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_28(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 1.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_29(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = None
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_30(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 1.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_31(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(None):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_32(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = None
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_33(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(None, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_34(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, None)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_35(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_36(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(
                    new_params,
                )
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_37(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = None
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_38(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = None
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_39(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum >= 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_40(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1.000000000001:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_41(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var = np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_42(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var -= np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_43(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(None)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_44(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights / resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_45(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid * 2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_46(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**3)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_47(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight = w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_48(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight -= w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_49(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight >= 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_50(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1.000000000001:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_51(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = None

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_52(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(None, 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_53(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), None)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_54(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_55(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(
                    np.sqrt(total_var / total_weight),
                )

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_56(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(None), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_57(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var * total_weight), 1e-6)

    def xǁMarkovSwitchingARǁ_update_variances__mutmut_58(
        self,
        new_params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        idx: int,
    ) -> None:
        """Update variance parameters in M-step."""
        k = self.k_regimes
        p = self.order

        if self.switching_variance:
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    var_s = np.sum(weights * resid**2) / w_sum
                    new_params[idx + s] = max(np.sqrt(var_s), 1e-6)
        else:
            total_var = 0.0
            total_weight = 0.0
            for s in range(k):
                resid = self._compute_regime_residuals(new_params, s)
                weights = smoothed[p:, s]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    total_var += np.sum(weights * resid**2)
                    total_weight += w_sum
            if total_weight > 1e-12:
                new_params[idx] = max(np.sqrt(total_var / total_weight), 1.000001)

    xǁMarkovSwitchingARǁ_update_variances__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_1": xǁMarkovSwitchingARǁ_update_variances__mutmut_1,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_2": xǁMarkovSwitchingARǁ_update_variances__mutmut_2,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_3": xǁMarkovSwitchingARǁ_update_variances__mutmut_3,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_4": xǁMarkovSwitchingARǁ_update_variances__mutmut_4,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_5": xǁMarkovSwitchingARǁ_update_variances__mutmut_5,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_6": xǁMarkovSwitchingARǁ_update_variances__mutmut_6,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_7": xǁMarkovSwitchingARǁ_update_variances__mutmut_7,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_8": xǁMarkovSwitchingARǁ_update_variances__mutmut_8,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_9": xǁMarkovSwitchingARǁ_update_variances__mutmut_9,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_10": xǁMarkovSwitchingARǁ_update_variances__mutmut_10,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_11": xǁMarkovSwitchingARǁ_update_variances__mutmut_11,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_12": xǁMarkovSwitchingARǁ_update_variances__mutmut_12,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_13": xǁMarkovSwitchingARǁ_update_variances__mutmut_13,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_14": xǁMarkovSwitchingARǁ_update_variances__mutmut_14,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_15": xǁMarkovSwitchingARǁ_update_variances__mutmut_15,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_16": xǁMarkovSwitchingARǁ_update_variances__mutmut_16,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_17": xǁMarkovSwitchingARǁ_update_variances__mutmut_17,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_18": xǁMarkovSwitchingARǁ_update_variances__mutmut_18,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_19": xǁMarkovSwitchingARǁ_update_variances__mutmut_19,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_20": xǁMarkovSwitchingARǁ_update_variances__mutmut_20,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_21": xǁMarkovSwitchingARǁ_update_variances__mutmut_21,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_22": xǁMarkovSwitchingARǁ_update_variances__mutmut_22,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_23": xǁMarkovSwitchingARǁ_update_variances__mutmut_23,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_24": xǁMarkovSwitchingARǁ_update_variances__mutmut_24,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_25": xǁMarkovSwitchingARǁ_update_variances__mutmut_25,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_26": xǁMarkovSwitchingARǁ_update_variances__mutmut_26,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_27": xǁMarkovSwitchingARǁ_update_variances__mutmut_27,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_28": xǁMarkovSwitchingARǁ_update_variances__mutmut_28,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_29": xǁMarkovSwitchingARǁ_update_variances__mutmut_29,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_30": xǁMarkovSwitchingARǁ_update_variances__mutmut_30,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_31": xǁMarkovSwitchingARǁ_update_variances__mutmut_31,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_32": xǁMarkovSwitchingARǁ_update_variances__mutmut_32,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_33": xǁMarkovSwitchingARǁ_update_variances__mutmut_33,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_34": xǁMarkovSwitchingARǁ_update_variances__mutmut_34,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_35": xǁMarkovSwitchingARǁ_update_variances__mutmut_35,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_36": xǁMarkovSwitchingARǁ_update_variances__mutmut_36,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_37": xǁMarkovSwitchingARǁ_update_variances__mutmut_37,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_38": xǁMarkovSwitchingARǁ_update_variances__mutmut_38,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_39": xǁMarkovSwitchingARǁ_update_variances__mutmut_39,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_40": xǁMarkovSwitchingARǁ_update_variances__mutmut_40,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_41": xǁMarkovSwitchingARǁ_update_variances__mutmut_41,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_42": xǁMarkovSwitchingARǁ_update_variances__mutmut_42,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_43": xǁMarkovSwitchingARǁ_update_variances__mutmut_43,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_44": xǁMarkovSwitchingARǁ_update_variances__mutmut_44,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_45": xǁMarkovSwitchingARǁ_update_variances__mutmut_45,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_46": xǁMarkovSwitchingARǁ_update_variances__mutmut_46,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_47": xǁMarkovSwitchingARǁ_update_variances__mutmut_47,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_48": xǁMarkovSwitchingARǁ_update_variances__mutmut_48,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_49": xǁMarkovSwitchingARǁ_update_variances__mutmut_49,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_50": xǁMarkovSwitchingARǁ_update_variances__mutmut_50,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_51": xǁMarkovSwitchingARǁ_update_variances__mutmut_51,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_52": xǁMarkovSwitchingARǁ_update_variances__mutmut_52,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_53": xǁMarkovSwitchingARǁ_update_variances__mutmut_53,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_54": xǁMarkovSwitchingARǁ_update_variances__mutmut_54,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_55": xǁMarkovSwitchingARǁ_update_variances__mutmut_55,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_56": xǁMarkovSwitchingARǁ_update_variances__mutmut_56,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_57": xǁMarkovSwitchingARǁ_update_variances__mutmut_57,
        "xǁMarkovSwitchingARǁ_update_variances__mutmut_58": xǁMarkovSwitchingARǁ_update_variances__mutmut_58,
    }
    xǁMarkovSwitchingARǁ_update_variances__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingARǁ_update_variances"
    )

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, smoothed, joint_smoothed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_m_step_update__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingARǁ_m_step_update__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_orig(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_1(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = None
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_2(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = None
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_3(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(None, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_4(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, None, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_5(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, None)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_6(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_7(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_8(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(
            new_params,
            smoothed,
        )
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_9(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 1)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_10(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = None
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_11(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(None, smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_12(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, None, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_13(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, None)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_14(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(smoothed, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_15(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, idx)
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_16(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(
            new_params,
            smoothed,
        )
        self._update_variances(new_params, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_17(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(None, smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_18(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, None, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_19(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, smoothed, None)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_20(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(smoothed, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_21(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(new_params, idx)
        return new_params

    def xǁMarkovSwitchingARǁ_m_step_update__mutmut_22(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-AR.

        Updates means, AR coefficients, and variances using weighted
        regression with smoothed probabilities.

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
        new_params = params.copy()
        idx = self._update_means(new_params, smoothed, 0)
        idx = self._update_ar_coeffs(new_params, smoothed, idx)
        self._update_variances(
            new_params,
            smoothed,
        )
        return new_params

    xǁMarkovSwitchingARǁ_m_step_update__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_1": xǁMarkovSwitchingARǁ_m_step_update__mutmut_1,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_2": xǁMarkovSwitchingARǁ_m_step_update__mutmut_2,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_3": xǁMarkovSwitchingARǁ_m_step_update__mutmut_3,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_4": xǁMarkovSwitchingARǁ_m_step_update__mutmut_4,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_5": xǁMarkovSwitchingARǁ_m_step_update__mutmut_5,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_6": xǁMarkovSwitchingARǁ_m_step_update__mutmut_6,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_7": xǁMarkovSwitchingARǁ_m_step_update__mutmut_7,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_8": xǁMarkovSwitchingARǁ_m_step_update__mutmut_8,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_9": xǁMarkovSwitchingARǁ_m_step_update__mutmut_9,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_10": xǁMarkovSwitchingARǁ_m_step_update__mutmut_10,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_11": xǁMarkovSwitchingARǁ_m_step_update__mutmut_11,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_12": xǁMarkovSwitchingARǁ_m_step_update__mutmut_12,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_13": xǁMarkovSwitchingARǁ_m_step_update__mutmut_13,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_14": xǁMarkovSwitchingARǁ_m_step_update__mutmut_14,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_15": xǁMarkovSwitchingARǁ_m_step_update__mutmut_15,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_16": xǁMarkovSwitchingARǁ_m_step_update__mutmut_16,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_17": xǁMarkovSwitchingARǁ_m_step_update__mutmut_17,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_18": xǁMarkovSwitchingARǁ_m_step_update__mutmut_18,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_19": xǁMarkovSwitchingARǁ_m_step_update__mutmut_19,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_20": xǁMarkovSwitchingARǁ_m_step_update__mutmut_20,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_21": xǁMarkovSwitchingARǁ_m_step_update__mutmut_21,
        "xǁMarkovSwitchingARǁ_m_step_update__mutmut_22": xǁMarkovSwitchingARǁ_m_step_update__mutmut_22,
    }
    xǁMarkovSwitchingARǁ_m_step_update__mutmut_orig.__name__ = "xǁMarkovSwitchingARǁ_m_step_update"

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, Any]]:
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_orig(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_1(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = None
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_2(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = None
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_3(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(None):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_4(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = None
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_5(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(None, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_6(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, None)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_7(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_8(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(
                params,
            )
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_9(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = None
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_10(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"XXmuXX": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_11(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"MU": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_12(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "XXsigmaXX": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_13(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "SIGMA": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_14(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(None):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_15(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = None
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_16(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag - 1}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_17(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 2}"] = float(phi[lag])
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_18(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(None)
            regime_params[s] = rp
        return regime_params

    def xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_19(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, Any]]:
        """Extract regime-specific parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, Any]] = {}
        for s in range(k):
            mu, phi, sigma = self._unpack_params(params, s)
            rp: dict[str, Any] = {"mu": mu, "sigma": sigma}
            for lag in range(self.order):
                rp[f"phi_{lag + 1}"] = float(phi[lag])
            regime_params[s] = None
        return regime_params

    xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_1": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_1,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_2": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_2,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_3": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_3,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_4": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_4,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_5": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_5,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_6": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_6,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_7": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_7,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_8": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_8,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_9": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_9,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_10": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_10,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_11": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_11,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_12": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_12,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_13": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_13,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_14": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_14,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_15": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_15,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_16": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_16,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_17": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_17,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_18": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_18,
        "xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_19": xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_19,
    }
    xǁMarkovSwitchingARǁ_extract_regime_params__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingARǁ_extract_regime_params"
    )
